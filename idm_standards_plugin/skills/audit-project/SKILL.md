---
name: audit-project
description: The Audit-Project skill runs IDM code and/or documentation audits on a project with a single set of questions, and summarizes the results in project_audit.md. Use this skill when the user asks to "audit my project", "audit everything", "check code and docs", "run a full audit", or invokes /idm-standards:audit-project. For code-only or docs-only audits requested explicitly, use audit-code or audit-docs directly instead.
argument-hint: "[project_path_or_github_url] [tier] [strictness]"
allowed-tools: Read, Glob, Grep, Bash, Write, Agent, WebFetch, AskUserQuestion, Skill
---

Run the IDM code and/or documentation audits on a project, asking the user's preferences once, and write a combined `project_audit.md` summary.

Skill version: 2.0_2026.06.10

## Step 1: Parse arguments and resolve the project

The user provides up to three arguments: **project** (local path or GitHub URL; default current directory), **tier** (1–3), and **strictness** (1–2). Tier definitions and strictness semantics are the same as in `audit-code`.

**If a GitHub URL is given**: clone it **once** with `gh repo clone <url> /tmp/audit-project-$(date +%s)` and use that local path for every sub-audit (the docs audit has no URL support of its own).

**Discover the user config once**, following `$CLAUDE_PLUGIN_ROOT/reference/user-config.md` (read it now), against the resolved local path. Hold its directives (and any frontmatter `tier`/`strictness`) to pass into every sub-audit in Step 3, so they aren't re-discovered three times. If the project came from a GitHub URL or a path the user didn't author, surface the directives for confirmation in Step 2 before applying.

## Step 2: Ask the user once

Use a **single AskUserQuestion call** covering (omit any already supplied as arguments or by invocation instructions):

1. **Which audits to run?** (multiSelect)
   - "Code audit (Recommended)" — engineering quality scoring (`audit-code`, or `audit-r-code` for R projects)
   - "Docs audit (Recommended)" — documentation completeness, structure, audience fit (`audit-docs`)
   - "Exhaustive code review" — per-file review of the whole codebase (`audit-code-exhaustive`); note: much slower
   The default is code + docs ("both").
2. **Tier**: the three tier options, with an inferred tier as the recommended option (infer as in `audit-code` Step 2). **Tier 1 is the strictest (large reusable library / DPG); Tier 3 is the loosest (one-off / exploratory).** Keep each tier number glued to its definition: when the recommended option is moved to the top, its number moves with it — never relabel a definition with a different tier number. A published/packaged library is **Tier 1**, not Tier 3.
3. **Strictness**: 1 (strict — everything) or 2 (material only).

If the config (Step 1) set `tier`/`strictness` in frontmatter, use them as the recommended values (explicit arguments still win). If the project was cloned from a URL or otherwise not user-authored and config directives were found, list them in this same question and confirm before applying. In non-interactive contexts, run code + docs audits with the config's (or inferred) tier and strictness 1, applying the directives but quoting them in the summary.

## Step 3: Run the selected audits

Invoke each selected skill via the Skill tool, passing the **local project path** and the confirmed **tier** and **strictness**, with the instruction: *"tier and strictness already confirmed — do not re-ask, and do not offer to fix at the end (audit-project will handle that)"*. Also append the config directives (Step 1) to that instruction — e.g. *"user config directives already discovered and confirmed; apply these and do not re-read the config: <directives>"* — so each sub-audit applies them without re-discovering the file.

- **Code audit**: invoke `audit-code` (it routes to `audit-r-code` automatically if the project is R). Output: `code_audit.md`.
- **Docs audit**: invoke `audit-docs`. Output: `docs_audit.md`.
- **Exhaustive review** (if selected): invoke `audit-code-exhaustive`. Output: `code_audit_exhaustive.md`.

## Step 4: Write the combined summary

Write `project_audit.md` to the project directory:

```markdown
# Project audit

- **Project**: `<project_path>`
- **Tier**: <tier>
- **Strictness**: <strictness>
- **Config**: <config file(s) and directive counts, or "none">
- **Audits run**: <list>
- **Date**: <YYYY-MM-DD>
- **Version**: idm-standards:audit-project <skill version>

## Results

| Audit | Headline result | Report |
| -- | -- | -- |
| Code | <overall score>/100 (<PASS/FAIL>) | [code_audit.md](code_audit.md) |
| Docs | <one-line health summary> | [docs_audit.md](docs_audit.md) |
| Exhaustive review | <N findings, M critical> | [code_audit_exhaustive.md](code_audit_exhaustive.md) |

## Top recommendations

<The 5–10 highest-impact recommendations across all reports, deduplicated. Where the code and
docs audits overlap (both check README, LICENSE, docstrings, changelog), merge into a single
entry and cross-reference both reports rather than repeating the finding twice. The sub-audits
already applied the config directives, so suppressed items won't appear here; if config was
active, add one line noting it (e.g. "Config: 5 directives applied — see per-audit reports").>

## Notes

<Anything the user should know: inferred vs confirmed tier, audits skipped, reports that
ended in FAIL, etc.>
```

Keep the summary short — the detail lives in the per-audit reports.

## Step 5: Offer to fix

If running interactively, finish with a single AskUserQuestion: **"Apply the fixes now?"** — options: "Yes — run fix-project now (Recommended)" / "No — I'll review the reports first". If yes, invoke the `fix-project` skill via the Skill tool with the project path. In non-interactive contexts, skip this question.
