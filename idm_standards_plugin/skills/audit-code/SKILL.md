---
name: audit-code
description: The Audit-Code skill scores a software project against IDM engineering quality tiers (1–3) across quality, usability, and safety metrics, and writes a code_audit.md report. Use this skill when the user asks to "audit my code", "score my project", "check engineering quality", "evaluate code quality", "assess tier compliance", or invokes /idm-standards:audit-code. Also use proactively when the user says "how good is this code?" or "what improvements does this project need?". For R projects, this skill routes to audit-r-code.
argument-hint: "[project_path_or_github_url] [tier] [strictness]"
allowed-tools: Read, Glob, Grep, Bash, Write, Agent, WebFetch, AskUserQuestion, Skill
---

Score a software project against the IDM engineering quality guidelines and write a `code_audit.md` report.

Skill version: 2.0_2026.06.10

## Step 0: Record start time

Before doing anything else, run the following bash command and save the result as `START_EPOCH`:

```bash
date +%s
```

This will be used in Step 9 to compute elapsed time.

## Step 1: Parse arguments and detect language

The user provides up to three arguments:
- **project**: path to a local directory OR a GitHub URL (e.g., `https://github.com/org/repo`). Default: current working directory.
- **tier**: integer 1, 2, or 3. If supplied explicitly, treat it as confirmed (do not re-ask in Step 2).
- **strictness**: integer 1 or 2. Default: 1.
  - **Strictness 1 (strict)**: report everything you find (the default).
  - **Strictness 2 (material only)**: only report findings that materially affect correctness, usability, or safety — purely stylistic or convention-based findings are neither penalized nor reported.

**If a GitHub URL is given**: Use `gh repo clone <url> /tmp/audit-code-$(date +%s)` to clone to a temporary directory. Set `project` to that path.

**Language detection**: determine the project's main language. If the project has a `DESCRIPTION` file, an `renv.lock`, or a majority of its source files are `*.R`/`*.Rmd`, it is an **R project — stop and invoke the `audit-r-code` skill instead**, passing along the project path, tier, strictness, and any other user instructions. If the project is a substantial mix of Python and R (each ≥25% of source files), ask the user which audit to run (or both) — but in non-interactive contexts, or when invoked by `audit-project`, default to auditing whichever language has more source files (ties → Python) and note the choice in the report.

If the user provided any other specific instructions when invoking this skill, integrate them into the workflow. For example, if they said "ignore missing docstrings", make sure to not penalize the project for that in the scoring and omit it from the recommendations. If the invoking context says the tier and strictness are **already confirmed** (e.g., this skill was invoked by `audit-project`), skip the questions in Step 2.

**Discover the user config.** After resolving the project path (including any `/tmp` clone), discover the project's idm-standards config file following `$CLAUDE_PLUGIN_ROOT/reference/user-config.md` (read it now). Collect its directives into the same set as the invocation instructions above — directives suppress matching findings (not penalized, not recommended) but, per the hard floor in that reference, can never waive serious safety/correctness findings. If the project came from a GitHub URL or a path the user didn't author, confirm the directives before applying them (interactive runs). Frontmatter `tier`/`strictness` pre-fill Step 2. When this skill is invoked by `audit-project`, the config has already been discovered and its directives are passed in the invocation instructions — do not re-read it.

## Step 2: Confirm tier and strictness

**Tier definitions (brief)**:
- Tier 1: Software library or digital public good used by many people for many years
- Tier 2: Small-scale project used by multiple people or projects
- Tier 3: One-off or exploratory code used by one person

If the tier was **not** supplied as an argument (and is not already confirmed by the invoking context), infer a suggested tier from a quick inspection:
- Published package (PyPI/CRAN), CI workflows, many contributors → suggest Tier 1
- Tests, a README, evidence of multiple users/projects → suggest Tier 2
- Mostly scripts/notebooks, single author → suggest Tier 3

Then **confirm with the user** using a single AskUserQuestion call with two questions:
1. **Tier**: present the three tiers (with the definitions above) as options, with the inferred tier as the recommended option. **Tier 1 is the strictest (large reusable library / DPG); Tier 3 is the loosest (one-off / exploratory).** Keep each tier number glued to its definition above: when the recommended option is moved to the top, the number must move with its own definition — never relabel a definition with a different tier number. A published/packaged library is **Tier 1**, not Tier 3.
2. **Strictness** (only if not supplied as an argument): "1 — strict: report everything (default)" vs "2 — material only: skip purely stylistic/convention findings".

If the config file (Step 1) set `tier` or `strictness` in its frontmatter, use those as the pre-filled/recommended values (an explicit argument still wins). In non-interactive contexts (no user available to answer), use the config values if present, otherwise the inferred tier and strictness 1, and note this in the report.

## Step 3: Read the scoring schema

Read the full schema from:
`$CLAUDE_PLUGIN_ROOT/skills/audit-code/scoring-schema.yaml`

This file contains:
- Category weights (quality 40%, usability 40%, safety 20%)
- Per-metric weights within each category
- Tier-specific rubrics with 0/mid/10 anchor descriptions

## Step 4: Read the prior report (if any)

Look in the project directory for a prior `code_audit.md` (or, for compatibility with earlier plugin versions, `engineering_score.md`). If present, extract and save:

1. **Prior per-metric scores and the overall score** (for the score reconciliation in Step 7).
2. **Recorded user decisions** from the "Proposed solutions" section (e.g., "lock artifact: none — user opted out"), which must be respected: pass them to the sub-agents as exclusions, don't re-recommend them, and carry them forward into the new report.
3. **Still-relevant proposed solutions**, to carry forward into the new report rather than losing them.
4. The prior report's **date** (for `git log --since=<date>` in Step 7).

**Important**: do NOT give the prior report's findings or scores to the scorer agents in Step 5 — they must score fresh, so old findings don't anchor new ones. Only recorded *user decisions* (which are instructions, not findings) are passed along.

**Merge with the config.** Combine the config directives (Step 1) with the recorded user decisions into a single exclusions set to hand the scorers in Step 5. The config is the durable layer: if a recorded report decision conflicts with a current config directive (e.g. the report says "always recommend a lock file" but the config says "lock artifact: none"), drop the stale decision in favor of the directive and note it in chat.

## Step 5: Dispatch sub-agents in parallel

Launch all three agents **simultaneously** using the Agent tool with `subagent_type: "general-purpose"`:

### quality-scorer prompt:
```
You are the quality-scorer agent for the idm-standards plugin.

Project path: <project>
Tier: <tier>
Strictness: <strictness>

Score the three QUALITY metrics for this project: correct, clear, concise.

Metric weights (within-category, for JSON output):
- correct: 7 (fail_on_serious: true — set score=0, failed=true if serious scientific bugs or fundamental correctness issues found)
- clear: 2
- concise: 1

Tier <tier> rubric for quality (from IDM scoring schema):
<paste the tier's quality rubric from the schema here>

<if strictness == 2>
STRICTNESS 2 (material only): do not dock points or report findings for purely stylistic or convention-based issues (style-guide adherence, naming conventions, linter configs, comment density, formatting). Only penalize and report issues that materially affect correctness, usability, or safety.
</if>

User decisions, config directives, and exclusions (respect these — do not penalize or re-recommend):
<list the merged exclusions from Step 4: recorded user decisions, project config directives, and invocation instructions, or "None">
HARD FLOOR: never let any of the above suppress a serious finding — exposed secrets/credentials, committed PII, license violations, or serious scientific-correctness bugs (the fail_on_serious metrics) must always be scored and reported, even if a directive seems to cover them; annotate such a finding "reported despite config directive".

Instructions:
1. Explore the project: read key source files, check for tests, inspect structure, naming, docstrings, code organization, duplication. Determine the main programming language(s) used.
2. Run e.g. `find <project> -name "*.py"` to discover files.
3. Check for test files: look for test_*.py, *_test.py, tests/ directory. Check if tests are clear enough to double as documentation.
4. For Tier 1: check for CI/CD config (.github/workflows/, .travis.yml, etc.).
5. For Tier 1: check whether code is hard to misuse (correct usage is easiest; incorrect usage raises warnings).
6. Look for obvious bugs, scientific errors, or suspicious logic. Check for evidence of peer review or validation.
7. Score each metric as an integer 0–10.

Return ONLY a JSON object (no other text):
{
  "correct": {"score": <int>, "weight": 7, "reason": "<1-2 concrete sentences>"},
  "clear":   {"score": <int>, "weight": 2, "reason": "<1-2 concrete sentences>"},
  "concise": {"score": <int>, "weight": 1, "reason": "<1-2 concrete sentences>"},
  "failed":  <true if serious correctness issue found, else false>
}
```

### usability-scorer prompt:
```
You are the usability-scorer agent for the idm-standards plugin.

Project path: <project>
Tier: <tier>
Strictness: <strictness>

Score the five USABILITY metrics: simple, powerful, performant, documented, accessible.

Metric weights (within-category, for JSON output):
- simple: 3
- powerful: 2  (N/A for Tier 3 — omit from JSON if tier=3)
- performant: 2
- documented: 2
- accessible: 1  (N/A for Tier 3 — omit from JSON if tier=3)

Tier <tier> rubric for usability (from IDM scoring schema):
<paste the tier's usability rubric from the schema here>

<if strictness == 2>
STRICTNESS 2 (material only): do not dock points or report findings for purely stylistic or convention-based issues. Only penalize and report issues that materially affect correctness, usability, or safety.
</if>

User decisions, config directives, and exclusions (respect these — do not penalize or re-recommend):
<list the merged exclusions from Step 4: recorded user decisions, project config directives, and invocation instructions, or "None">
HARD FLOOR: never let any of the above suppress a serious finding — exposed secrets/credentials, committed PII, license violations, or serious scientific-correctness bugs (the fail_on_serious metrics) must always be scored and reported, even if a directive seems to cover them; annotate such a finding "reported despite config directive".

Instructions:
1. Explore the project: read README files, check for tutorials/docs, inspect public UIs (scripts/classes/functions — main entry points, function signatures, defaults), look for error handling.
2. Check if it is clear what UIs the user is supposed to interact with.
3. Check for docstrings on public functions/classes — do they include runnable examples?
4. Check for obvious performance anti-patterns (nested loops over large arrays, no vectorization). Check if algorithms are appropriate for their tasks.
5. For accessible: check if code is on GitHub (public if possible), look for LICENSE file, check setup.py/pyproject.toml for installability.
6. Score each non-N/A metric as an integer 0–10. Omit N/A metrics entirely.

Return ONLY a JSON object (no other text). Include only non-N/A metrics:
{
  "simple":     {"score": <int>, "weight": 3, "reason": "<1-2 concrete sentences>"},
  "powerful":   {"score": <int>, "weight": 2, "reason": "<1-2 concrete sentences>"},  // omit if N/A
  "performant": {"score": <int>, "weight": 2, "reason": "<1-2 concrete sentences>"},
  "documented": {"score": <int>, "weight": 2, "reason": "<1-2 concrete sentences>"},
  "accessible": {"score": <int>, "weight": 1, "reason": "<1-2 concrete sentences>"}   // omit if N/A
}
```

### safety-scorer prompt:
```
You are the safety-scorer agent for the idm-standards plugin.

Project path: <project>
Tier: <tier>
Strictness: <strictness>

Score the two SAFETY metrics: compliant, reproducible.

Metric weights (within-category, for JSON output):
- compliant: 6  (fail_on_serious: true — set score=0, failed=true if serious violations found)
- reproducible: 4

Tier <tier> rubric for safety (from IDM scoring schema):
<paste the tier's safety rubric from the schema here>

<if strictness == 2>
STRICTNESS 2 (material only): do not dock points or report findings for purely stylistic or convention-based issues. Only penalize and report issues that materially affect correctness, usability, or safety.
</if>

User decisions, config directives, and exclusions (respect these — do not penalize or re-recommend):
<list the merged exclusions from Step 4: recorded user decisions, project config directives, and invocation instructions, or "None">
HARD FLOOR: never let any of the above suppress a serious finding — exposed secrets/credentials, committed PII, license violations, or serious scientific-correctness bugs (the fail_on_serious metrics) must always be scored and reported, even if a directive seems to cover them; annotate such a finding "reported despite config directive".

Lock-artifact rules (for the reproducible metric):
- Tier 1 (library code): dependencies should be specified loosely in pyproject.toml; NEVER suggest adding a lock file or pinned versions. A pylock.toml is acceptable if present, but its absence is not a deficiency.
- Tier 2/3 (research/non-library code): if reproducibility of results matters, exact versions should be captured — via `pip freeze > requirements_locked.txt` (simple; typical for Tier 3) or `pip lock` producing pylock.toml (advanced; typical for Tier 2). Present these as options for the user to choose between; "none" is also acceptable, especially if recorded as a user decision.
- Do not call `>=` version bounds "pins" — bounds are guidance; pins are exact (`==`) versions.

Instructions:
1. Check for exposed secrets: scan for .env files, hardcoded API keys/tokens/passwords using grep patterns like (api_key|secret|password|token)\s*=\s*['\"][^'"]{8,}.
2. Check for LICENSE file and identify license type.
3. Inspect dependency files (pyproject.toml, requirements.txt, setup.py) for restrictive licenses (GPL, AGPL, proprietary).
4. Check dependency specification: are dependencies specified in pyproject.toml? For Tier 2/3 projects that produce final results, are exact versions captured (requirements_locked.txt, pylock.toml) or has the user recorded a decision not to?
5. Check random seed handling: if random numbers are used, do same seeds give identical results?
6. For Tier 1 and 2: check version control — git tags, semantic versioning.
7. For Tier 1: check if package is on PyPI (curl -I https://pypi.org/pypi/<package>/json), look for CHANGELOG.
8. Score each metric as an integer 0–10.

Return ONLY a JSON object (no other text):
{
  "compliant":    {"score": <int>, "weight": 6, "reason": "<1-2 concrete sentences>"},
  "reproducible": {"score": <int>, "weight": 4, "reason": "<1-2 concrete sentences>"},
  "failed": <true if serious compliance violation found, else false>
}
```

**Important**: Before dispatching, replace `<project>`, `<tier>`, `<strictness>`, the strictness block, the user-decisions block (expanding the merged exclusions from Step 4, including the config directives, verbatim — the subagents do not see the config file or any CLAUDE.md, so anything not pasted here is invisible to them), and `<paste ... rubric here>` with actual values from Steps 1–4.

## Step 6: Compute overall score

After all three agents return results, calculate:

```python
# Within-category scores (0-10 each)
quality_weights = {"correct": 7, "clear": 2, "concise": 1}
usability_weights = {"simple": 3, "powerful": 2, "performant": 2, "documented": 2, "accessible": 1}
safety_weights = {"compliant": 6, "reproducible": 4}

# For N/A metrics (omitted from JSON): exclude from both numerator and denominator
quality_raw    = sum(score * w for m, w in quality_weights.items()   if m in quality_results)   / sum(w for m, w in quality_weights.items()   if m in quality_results)
usability_raw  = sum(score * w for m, w in usability_weights.items() if m in usability_results) / sum(w for m, w in usability_weights.items() if m in usability_results)
safety_raw     = sum(score * w for m, w in safety_weights.items()    if m in safety_results)    / sum(w for m, w in safety_weights.items()    if m in safety_results)

# Category scores out of 100 (for the summary table)
quality_score   = round(quality_raw   * 10)
usability_score = round(usability_raw * 10)
safety_score    = round(safety_raw    * 10)

# Overall score: category weights are 40%, 40%, 20% of a 0-100 scale
overall_score = round(quality_raw * 4 + usability_raw * 4 + safety_raw * 2)
```

Set `failed: true` in the final JSON if either `quality.correct.failed` or `safety.compliant.failed` is true.

## Step 7: Reconcile scores against the prior report

Skip this step if there was no prior report in Step 4. If the prior report used a different tier or strictness, **or a different config digest** (compare the directive list recorded in the prior report's Full Results against the current one), skip reconciliation and note the changed settings in the report instead (scores are not comparable across settings or config).

For **each metric whose new score is lower than the prior score**, you must justify the decrease with concrete evidence before accepting it. There are exactly two valid justifications:

- **(a) Something actually got worse**: cite the specific change, using history where available (`git log --since=<prior report date>`, `git diff`) — e.g., "three new functions added to model.py since 2026-05-01 with no tests".
- **(b) The previous run missed something**: name the specific finding the previous audit should have caught — e.g., "`fit()` mutates its input array; present in the prior version but not previously reported".

If **neither** can be substantiated, the drop is stochastic scoring noise: **retain the prior (higher) score** and adjust the metric's reason accordingly. This is the existing scoring principle — "don't dock points for theoretical issues, only concrete observable problems" — applied across runs.

Record every score change (increases and justified decreases alike) for the "Score changes since last run" section of the report, then recompute the overall score with the reconciled values.

## Step 8: Generate recommendations and proposed solutions

**Config backstop**: before ranking, drop any recommendation that matches a config directive (Step 1) — a scorer may surface one anyway. The hard floor still holds: never drop a serious safety/correctness finding; report it annotated "reported despite config directive".

Write concrete, actionable recommendations ranked by impact (score x weight). Every time you give a score below 10, write the specific improvement that would raise it. Each recommendation should:

- Name the specific metric it improves
- Be specific and implementable (e.g., "Add a `tests/` directory with pytest tests for the three main functions" not "add tests")
- Note if it is quick (minutes), medium (hours), or large (days) effort
- Note if it cannot be automated (e.g., "Write a user guide" — human effort required)

**For every recommendation marked `automated: no`**, also write a **proposed solution**: a concrete approach the user could follow (steps, an outline, or a code sketch — not just a restatement of the title). These go in the report's "Proposed solutions" section, together with any items carried forward from the prior report (Step 4) and any recorded user decisions.

For reproducibility recommendations on Tier 2/3 projects, present the lock-artifact choice as options (`requirements_locked.txt` via `pip freeze`, `pylock.toml` via `pip lock`, or none) rather than prescribing one — the fixer will ask the user which they want.

## Step 9: Write code_audit.md

Write this file to the **project directory** (not the current working directory if different).

Before writing, compute the following:
- **Date**: run `date +%Y-%m-%d` to get the current date.
- **Version**: Add this skill's name and version (listed at the top of this file) to the report header, e.g., "**Version**: idm-standards:audit-code v2.0_2026.06.10".
- **Time spent**: run `date +%s` to get `END_EPOCH`, then compute `END_EPOCH - START_EPOCH` (recorded in Step 0). Format as an integer number of seconds.

```markdown
# Code audit

- **Project**: `<project_path>`
- **Tier**: <tier> (<tier name>)
- **Strictness**: <strictness> (<"strict" or "material only">)
- **Config**: <config file(s) and directive counts, e.g. `.claude/idm-standards.md (5 directives)`, or "none">
- **Overall score**: <overall_score>/100
- **Status**: <PASS or FAIL — FAIL if failed=true>
- **Date**: <YYYY-MM-DD>
- **Version**: idm-standards:audit-code <version>
- **Time spent**: <seconds>s

## Summary

| Category | Score | Weight |
| -- | -- | -- |
| Quality | <quality_score>/100 | 40% |
| Usability | <usability_score>/100 | 40% |
| Safety | <safety_score>/100 | 20% |
| **Total** | **<overall_score>/100** | 100% |

| Metric | Score | Notes |
| -- | -- | -- |
| correct | <score>/10 | <brief reason> |
| clear | <score>/10 | <brief reason> |
| concise | <score>/10 | <brief reason> |
| simple | <score>/10 | <brief reason> |
| powerful | <score>/10 | <brief reason> |
| performant | <score>/10 | <brief reason> |
| documented | <score>/10 | <brief reason> |
| accessible | <score>/10 | <brief reason> |
| compliant | <score>/10 | <brief reason> |
| reproducible | <score>/10 | <brief reason> |

<2–4 sentences plain-language summary. Mention the strongest areas and the biggest gaps.
If failed=true, clearly state which metric caused the failure and why.>

## Score changes since last run

<Include this section only if a prior report existed. One line per changed metric:
- **[metric]**: <prior>/10 → <new>/10 — <reason: what improved; or for decreases, justification (a) or (b) from Step 7>
If a decrease was reverted as unjustifiable noise, note: "scored <x> this run but retained prior <y> (no concrete regression or missed finding identified)".>

## Recommendations

<List of recommendations, most impactful first. For each:>
1. **[Metric] — [Title]** *(effort: quick/medium/large; automated: yes/no)*
   <One or more concrete sentences describing exactly what to do.>

## Suppressed by config

<Include this section only if a config file was found (Step 1). One bullet per active
directive, quoting it and noting what it matched this run, e.g.:
- "Don't recommend renaming classes to CamelCase" — matched 1 clarity finding (suppressed).
- "Lock artifact: none" — nothing matched this run.
If a serious safety/correctness finding fell under a directive, list it here too, flagged
"reported despite config directive — serious finding cannot be suppressed". Never drop a
finding silently.>

## Proposed solutions

<For each recommendation marked automated: no — a concrete proposed approach (steps, outline, or code sketch). Also:
- Items carried forward from the prior report that are still relevant.
- Recorded user decisions, e.g. "Lock artifact: none — user opted out (2026-06-10). Do not re-recommend."
The fixer also appends to this section for items it cannot implement.
Do NOT duplicate config-file directives here — they live in the config file, which is the
single source of truth; this section records only per-run interactive decisions.>

## Full Results

```yaml
<the assembled YAML: project, tier, strictness, overall_score, failed, then per-category metrics with score/weight/reason. Also include a `config:` block listing the discovered config file path(s) and the active directives verbatim (or `config: none`), so a later run can detect the config changed.>
```
```

Give N/A metrics (Tier 3: `powerful`, `accessible`) a score of 10 in the assembled YAML.

## Step 10: Offer to fix

If running interactively and this skill was invoked directly (not by `audit-project` or another skill), finish with a single AskUserQuestion: **"Apply the fixes now?"** — options: "Yes — run fix-code now (Recommended)" / "No — I'll review the report first". If the user says yes, invoke the `fix-code` skill on the project via the Skill tool. In non-interactive contexts, skip this question.

## Notes

- **General scoring principle**: If no specific improvements can be identified for a metric, score 10/10. If scoring below 10, always list the specific improvements that would raise the score. Don't dock points for theoretical issues — only for concrete, observable problems.
- **Skip large and binary files**: Do not read files larger than 100 KB, or files with extensions `.csv`, `.pdf`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.svg`, `.ico`, `.tiff`, `.webp`. These are too large or not human-readable source code.
- Always read every source file (typically `*.py`) for the project. If there are large documentation files (e.g. `*.ipynb`), only read those if they are smaller than 100 KB.
- For Python projects: look for `pyproject.toml`, `setup.py`, `src/`, `tests/`, `.github/`.
- For R projects: do not score with this skill — route to `audit-r-code` (Step 1).
- Scientific correctness (quality.correct) is the most heavily weighted metric (28/100 points). Pay particular attention to this.
- If `failed=true`, still complete the full report — the recommendations should include how to address the failure.
