---
name: audit-docs
description: Comprehensive documentation audit for IDM projects. Checks docs completeness against IDM standards (README, tutorials, API reference, changelog, etc.), then applies the audit-docs-structure, audit-personas, and audit-docstrings skills to evaluate structure, audience fit, and docstring quality. Produces a unified docs_audit.md report with strengths, weaknesses, and prioritized recommendations. Use when reviewing, auditing, or scoring project documentation quality, or when the user invokes /idm-standards:audit-docs.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, Agent, Skill, AskUserQuestion
---

# Documentation audit

Skill version: 2.1_2026.07.21

This skill performs a comprehensive documentation audit for an IDM project. It checks general completeness against the IDM documentation standards, then delegates to three specialized skills for deeper analysis, and assembles everything into a single prioritized report.

## Workflow

### Step 1: Identify the project and its documentation

Determine which project to audit. If the user specified a project, use that. Otherwise, use the current working directory.

The invocation may also supply a **tier** (1–3, per the IDM code tiers: 1 = library/DPG, 2 = small shared project, 3 = one-off) and a **strictness** (1 = report everything, the default; 2 = only findings that materially affect users — skip purely stylistic findings, e.g. report Vale errors but not suggestions). These are typically passed by the `audit-project` skill, which has already confirmed them with the user — do not re-ask in that case. If the tier is not supplied, infer it from the project (published package + CI → 1; tests + README → 2; scripts only → 3) and note the inferred tier in the report. Tier-conditional checks below ("for Tier 1/2 only") use this tier.

If the user provided any specific instructions when invoking this skill, integrate them into the workflow. For example, if they said "focus on the API reference" or "pay special attention to the README", make sure to emphasize those areas in your audit.

**Discover the user config** following `$CLAUDE_PLUGIN_ROOT/reference/user-config.md` (read it now), unless the invoking context (e.g. `audit-project`) already passed the directives in. Apply directives scoped to docs (`audit-docs`, `audit-docs-structure`, `audit-personas`, `audit-docstrings`, or untagged "all audits" directives) — a suppressed item is neither flagged as a weakness nor recommended. Directives can never waive a license violation or other hard-floor finding (see the reference). Exclude any config file and `.claude/` from the docs being audited.

Scan for documentation artifacts:

- `README.md` at the repo root
- `LICENSE` file
- `CHANGELOG.md`, `CHANGES.md`, or `WHATSNEW.md` (or equivalent)
- `CONTRIBUTING.md` or equivalent
- `CODE_OF_CONDUCT.md` or equivalent
- `docs/` folder (or equivalent documentation directory)
- `mkdocs.yml` or `_quarto.yml` (documentation build config)
- Folder-level `README.md` files in major directories
- Jupyter notebooks (`.ipynb`) or Quarto notebooks (`.qmd`) used as tutorials
- Python source files with docstrings

Record what exists and what is missing.

### Step 2: Check general completeness

Evaluate the project's documentation against the IDM documentation standards in [`eng_guidance/4_documentation.md`](https://github.com/InstituteforDiseaseModeling/idm_standards/blob/main/eng_guidance/4_documentation.md). Check for:

**README.md contents:**
- What the package does (clear, concise description)
- Installation instructions (`pip install`, `uv add`, and local/dev install)
- Quick usage example (minimal "hello world" in under 10 lines)
- Project structure (one-line description of each submodule/folder)
- Links to full docs site, contributing guide, and issue tracker

**Required repo-level files:**
- LICENSE (MIT)
- Changelog / what's new (for tier 1 / tier 2 projects only)
- Contributing guide (for tier 1)
- Code of conduct (for tier 1)

**Folder-level READMEs:**
- Check whether major directories have `README.md` files explaining their purpose (not necessary if explained in top-level README)

**Documentation site / docs folder:**
- For Tier 1 / Tier 2 projects only
- Tutorials (at minimum: a getting started or hello word tutorial and a slightly more advanced one)
- User guide sections consisting of how-to and explanation topics or other similar explanations of functionality (for complex projects where tutorials + API reference aren't enough)
- API reference (auto-generated from docstrings via quartodoc, mkdocstrings, or the R equivalents)
- Documentation build configuration (`mkdocs.yml`, `_quarto.yml`, or `_pkgdown.yml`)

**API reference setup:**
- Interlinks configured for cross-references to standard libraries
- Auto-generation from docstrings (not hand-written API docs)

Score each item as: **Present** / **Partial** / **Missing** / **N/A**

### Step 3: Run specialized audits

Apply each of the three sub-skills by invoking them. For each, follow the skill's workflow against the project's documentation. You do not need to produce separate reports for each -- collect findings to merge into the final report. When invoking each sub-skill, restate any config directives relevant to it in the invocation text (these in-session sub-skills don't otherwise know about the config), and drop their suppressed findings when merging.

#### 3a: Doc structure audit

Invoke the `audit-docs-structure` skill. Evaluate:
- Whether the major documentation types are represented (API reference, tutorials, and for complex projects, user guides grouping how-to and explanation topics by subject matter)
- Whether existing docs are correctly categorized (e.g., a "tutorial" that is actually a how-to)
- Whether there is cross-contamination between types (e.g., reference material embedded in tutorials)
- How well the table of contents / navigation organizes content — tutorials and reference at top level, how-to and explanation grouped into user guides (IDM's divergence from Diátaxis)
- Whether related topics that live in *separate* TOC locations (not grouped into a shared user guide) still cross-reference each other. TOC grouping and cross-referencing are independent checks — flag missing links even when the grouping itself is reasonable (e.g., a how-to in a user guide and related explanation in an overview section that never link to one another or tutorials containing code examples that do not link to the relevant API reference topics).

#### 3b: Persona audit

Invoke the `audit-personas` skill. Evaluate:
- Whether documentation sections are written for their target personas
- Whether the landing page / top of README gives policy-maker and policy-influencer personas at least one or two plain-language sentences of real-world policy relevance (for policy-relevant projects, e.g. Tier 1 projects) — this is a light-touch check; do not recommend a dedicated section, case studies, or a full landing-page reframe for these two personas
- Whether tutorials serve model-user, model-extender, and model-builder personas
- Whether technical depth matches audience expectations
- Whether LMIC context is acknowledged where appropriate

#### 3c: Python docstrings audit

Invoke the `audit-docstrings` skill. Read all public modules, classes, and functions and evaluate:
- Whether public objects have docstrings (small/private objects can be ignored)
- Whether docstrings follow Google style
- Whether docstrings include: one-line summary, parameter descriptions, return values, usage examples
- Whether docstrings provide researcher workflow context
- Whether cross-references to related objects are present
- Overall docstring coverage (rough percentage of public objects with adequate docstrings)

#### 3d: Template audit

Evaluate the `mkdocs.yml`, `_quarto.yml`, or `_pkgdown.yml` configuration file against the reference templates bundled with this skill at `$CLAUDE_PLUGIN_ROOT/skills/audit-docs/assets/docs_templates/` (use `mkdocs_template/mkdocs.yml` for MkDocs projects and `quarto_template/` for Quarto projects), and note divergences. If Jupyter notebooks are not set to execute during the doc build or if errors are allowed to pass, this is a high priority to fix. Check the .github/workflows files--it is acceptable for Jupyter notebook execution to be run only on some workflows and not for all documentation builds.

### 3e: Grammar and style audit

Run the Vale linter to evaluate how well the documentation follows the style and grammar rules, particularly where violated rules are considered errors.

- If the target project ships its own `vale.ini`/`.vale.ini` and `.github/styles`, lint with that — it reflects the project's chosen rules.
- Otherwise, fall back to the bundled IDM config at `$CLAUDE_PLUGIN_ROOT/skills/audit-docs/assets/vale.ini` (its `StylesPath` already points at the co-located `styles/` directory): `vale --config "$CLAUDE_PLUGIN_ROOT/skills/audit-docs/assets/vale.ini" <docs paths>`.
- State in the report which config was used (the project's own or the bundled IDM default). If the `vale` binary is not installed, note that the style pass could not run rather than failing the audit.

If a config directive names a Vale rule to skip (e.g. "Skip Vale rule Google.Passive"), omit violations of that rule from the findings.

### Step 4: Assemble the report

Produce a single structured report and write it to `docs_audit.md` **in the project directory** (not the current working directory if different). Start with a brief header:

```markdown
# Documentation audit

- **Project**: `<project_path>`
- **Tier**: <tier> (<supplied or inferred>)
- **Strictness**: <strictness>
- **Config**: <config file(s) and directive counts, or "none">
- **Date**: <YYYY-MM-DD>
- **Version**: idm-standards:audit-docs <skill version>
```

Apply config directives when assembling the Weaknesses and Recommendations sections: drop any item a directive suppresses (never a hard-floor item). If a config file was found, add a short **Suppressed by config** note listing each active directive and what it matched (or "nothing matched this run"); never drop an item silently.

Then these sections:

**1. Summary**

A 2-3 sentence overview of the project's documentation health. State clearly whether documentation is in good shape, has notable gaps, or needs significant work.

**2. Strengths**

Bullet list of what the documentation does well. Be specific -- cite actual docs, sections, or patterns that are effective. Only include genuine strengths; do not pad this section.

**3. Weaknesses**

Bullet list of significant gaps or issues, organized by severity. For each weakness:
- What the issue is
- Why it matters (which users are affected, what they can't do)
- Where in the docs the issue occurs (file/section reference)

**4. Recommendations**

A numbered list of concrete, actionable improvements, **ranked by importance**. Importance is determined by:

1. **Impact on users** -- how many personas are affected, how severely
2. **Effort to fix** -- quick wins rank higher than large rewrites (at equal impact)
3. **Standards compliance** -- items required by IDM standards rank higher than nice-to-haves

For each recommendation:
- What to do (specific and actionable)
- Why it matters (brief justification)
- Estimated effort: **Low** (< 1 hour), **Medium** (1-4 hours), **High** (> 4 hours)

**5. Completeness checklist**

A compact table summarizing the presence/absence of each expected documentation component:

```
| Component                  | Status  | Notes |
|----------------------------|---------|-------|
| README.md                  | ...     | ...   |
| LICENSE                    | ...     | ...   |
| Changelog                  | ...     | ...   |
| Contributing guide         | ...     | ...   |
| Code of conduct            | ...     | ...   |
| Folder-level READMEs       | ...     | ...   |
| Docs site config           | ...     | ...   |
| Hello-world tutorial       | ...     | ...   |
| Advanced tutorial(s)       | ...     | ...   |
| User guide                 | ...     | ...   |
| API reference              | ...     | ...   |
| Doc structure coverage     | ...     | ...   |
| Persona targeting          | ...     | ...   |
| Docstring quality          | ...     | ...   |
```

### Step 5: Offer to fix

If running interactively and this skill was invoked directly (not by `audit-project` or another skill), finish with a single AskUserQuestion: **"Apply the documentation fixes now?"** — options: "Yes — run fix-project on the docs report now (Recommended)" / "No — I'll review the report first". If yes, invoke the `fix-project` skill via the Skill tool, telling it to act on `docs_audit.md` only. In non-interactive contexts, skip this question.

## Guidelines

- **Be concrete, not generic.** Cite specific files, sections, and examples. "The README lacks installation instructions" is useful; "documentation could be improved" is not.
- **Calibrate to the project's size and maturity.** A small utility package does not need a full user guide. A large modeling framework does. Judge what is appropriate and flag missing items accordingly.
- **Don't penalize for N/A items.** If a project has no Python code, skip the docstrings audit. If a project is a pure library with no policy audience, note that the persona audit is limited.
- **Acknowledge good work.** If documentation is genuinely well done in some area, say so clearly. The report should be balanced, not just a list of complaints.
- **Keep the report concise.** Aim for a report that can be read in 5-10 minutes. Use brief bullets, not paragraphs. The goal is actionable insight, not exhaustive analysis.
