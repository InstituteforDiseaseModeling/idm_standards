---
name: audit-code
description: The Audit-Code skill scores a software project against IDM engineering quality tiers (1–3) across quality, usability, and safety metrics, and writes a code_audit.md report of scores, findings, and prioritized recommendations. Use this skill when the user asks to "audit my code", "score my project", "check engineering quality", "evaluate code quality", "assess tier compliance", "review every file", "do a thorough/exhaustive code review", or invokes /idm-standards:audit-code. Also use proactively when the user says "how good is this code?" or "what improvements does this project need?". For R projects, this skill routes to audit-r-code.
argument-hint: "[project_path_or_github_url] [tier] [strictness] [inspect|run|max]"
allowed-tools: Read, Glob, Grep, Bash, Write, Agent, WebFetch, AskUserQuestion, Skill
---

Score a project against the IDM engineering quality guidelines and write a `code_audit.md` report. The audit is built on **findings**: specific, located problems, each with a fix. Scores are derived from findings, recommendations are written from them, and `fix-code` acts on them.

The shared definitions live in `$CLAUDE_PLUGIN_ROOT/reference/`: `criteria.yaml` (the checklist, taken from the guidelines), `findings.md` (finding format, severity, strictness) and `user-config.md` (the project config file and the hard floor). The scorer agents read these themselves; you need `findings.md` and `user-config.md` too, so read them now. If any plugin file can't be read, stop and tell the user rather than improvising its contents.

## Step 0: Record the start time

Run `date +%s` and save the result as `START_EPOCH`, for the "Time spent" line in Step 9.

## Step 1: Parse arguments, detect the language, read the config

Arguments, all optional:

- **project**: a local directory or a GitHub URL. Default: the current working directory. For a URL, clone it with `gh repo clone <url> /tmp/audit-code-$(date +%s)` and use that path.
- **tier**: 1, 2 or 3. If given, it is confirmed; don't ask in Step 2.
- **strictness**: 1 (report everything; default) or 2 (material findings only; see `findings.md`).
- **effort**: `inspect` (default), `run` or `max`. Each level does everything the one before it does:
  - **inspect**: the three scorers read the project (the important files in full) and run nothing from it. The report states how many source files were read.
  - **run**: also runs the project's tests and README example first (Step 3), and gives the scorers the results. Running code can have unexpected side effects (writing files, long jobs, network access), so it is used only when the user chooses it: the `run` argument, or asking for the tests or code to be run.
  - **max**: also has every source file read in full, line by line, by parallel file-reviewer subagents (Step 5) before scoring. Much slower and more expensive; use it when the user asks for max effort, an exhaustive review, or for every file to be read.

**Language**: if the project has a `DESCRIPTION` file or `renv.lock`, or most of its source files are `*.R`/`*.Rmd`, it is an R project: **stop and invoke the `audit-r-code` skill** with the same arguments and instructions. If it is a substantial mix (each of Python and R at least 25% of source files), ask which to audit (or both); in non-interactive runs, or when invoked by `audit-project`, audit whichever has more source files (ties go to Python) and note the choice in the report.

**Instructions**: anything else the user said when invoking the skill (e.g. "ignore missing docstrings") becomes an exclusion: not penalized and not recommended. If the invoking context says tier, strictness and effort are already confirmed (e.g. from `audit-project`), skip Step 2.

**Config**: read the project's `.claude/idm-standards.md` as described in `user-config.md`, unless the invoking context already passed the directives in. Its directives join the exclusions; its frontmatter `tier`/`strictness` pre-fill Step 2. For a GitHub URL or another path the user didn't write, confirm the directives before applying them (interactive runs).

## Step 2: Confirm tier, strictness and effort

Tiers:
- **Tier 1**: software library or digital public good, used by many people for many years. The strictest.
- **Tier 2**: small-scale project used by multiple people or projects.
- **Tier 3**: one-off or exploratory code used by one person. The loosest.

If the tier wasn't given, infer one: a published package (PyPI/CRAN), CI and many contributors suggest Tier 1; tests, a README and signs of several users suggest Tier 2; mostly scripts or notebooks by one author suggest Tier 3. Then ask once, with a single AskUserQuestion holding up to three questions (leave out any already given):

1. **Tier**: the three tiers as options, the inferred one recommended and listed first. Keep each tier number attached to its own definition when reordering; a published library is Tier 1, never Tier 3.
2. **Strictness**: "1: report everything (default)" or "2: material only, skip stylistic and convention findings".
3. **Effort**: "Inspect (Recommended): read the code, run nothing", "Run: also run the tests and README example (runs project code, which may have side effects)", or "Max: also read every source file in full with parallel subagents; much slower".

In non-interactive runs, use the config's values if present, otherwise the inferred tier, strictness 1 and inspect effort, and note this in the report.

## Step 3: Run the code (run and max effort)

At inspect effort (the default), skip this step: the execution results are "not run (inspect effort)", and the scorers judge from reading the code alone.

At run and max effort: running the code is the strongest evidence of whether it works. Before scoring, run the test suite and the README's quick-start example, and record what happened. The scorers receive these **execution results**.

- **Untrusted code**: if the project came from a GitHub URL or another path the user didn't write, confirm once more before running anything (interactive), or skip this step and record "not run: untrusted source" (non-interactive).
- **Environment**: use the current environment, and make one attempt. If the project or its dependencies aren't installed or importable, record "could not run" with the first error line and move on: don't investigate the environment, and don't install anything without asking. A failure caused only by the environment is not a finding against the project.
- **Tests**: run them from the project root with a time limit: 5 minutes at run effort, 30 at max (`timeout 300 python -m pytest -q`, or for R `timeout 300 Rscript -e 'testthat::test_local()'` or `testthat::test_dir("tests/testthat")`). Record the command, passed/failed/error/skipped counts, duration, and the first few failure messages.
- **README example**: take the first quick-start or usage code block in the README, write it to a temporary file outside the project, and run it from the project root with a 2-minute limit (set `MPLBACKEND=Agg` so plots don't open windows). Record whether it ran, and the error if not. Skip it if it is clearly a long production run (e.g. a calibration), and say so.
- If there are no tests or no README example, record that; it's information for the scorers, not an error.
- Note any files the run created in the project (`git status --porcelain` before and after), and don't treat them as part of the project.

## Step 4: Read the prior report

If the project already has a `code_audit.md` (or `engineering_score.md`, from plugin versions before 2.0), extract:

1. Its tier, strictness, effort, config directives, date, scores, and findings (the Findings section), for reconciliation in Step 7.
2. **Recorded user decisions** from its Proposed solutions section (e.g. "Lock artifact: none; user opted out"). These join the exclusions and are carried into the new report. If one conflicts with a current config directive, the directive wins (say so in chat).

Do **not** give the prior findings or scores to the agents: they must look fresh, so old findings don't anchor new ones.

## Step 5: Max effort only: read every source file

Skip this step at inspect and run effort.

1. **List the source files**: `git -C <project> ls-files --cached --others --exclude-standard` (or a recursive listing if it isn't a git repo). Keep code files: `.py`, `.pyx`, `.pxd`, `.ipynb`, `.R`, `.r`, `.Rmd`, `.qmd`, and files in any other programming language the project uses (C/C++, Julia, shell, JavaScript). Drop binary and data files, generated or vendored code (`_site/`, `build/`, `dist/`, minified files), `.claude/`, and paths excluded by a config directive. Tests, scripts, examples and notebooks are source files: keep them.
2. **Batch them**: count lines (`wc -l`) and group files into batches of up to about 3,000 lines and 20 files, keeping files from the same directory together. Split any file longer than 6,000 lines into line ranges of up to 3,000 lines (e.g. `src/big.py:1-3000`), each in its own batch.
3. **Tell the user** how many files, lines and batches there are; they asked for max effort, so don't ask to confirm.
4. **Dispatch** one `idm-standards:file-reviewer` agent per batch, in waves of at most 8 parallel calls (one message per wave). Each prompt:

   ```
   project: <absolute path>
   language: <python|r>
   tier: <tier>
   strictness: <strictness>
   plugin_root: <absolute path of $CLAUDE_PLUGIN_ROOT>
   exclusions: <the merged exclusions from Steps 1 and 4, verbatim, or "none">
   files:
   - <project-relative path, or path:start-end for a split file>
   - ...
   ```

5. **Check coverage**: every file (and line range) must appear in some reviewer's `files_read`. Re-dispatch any that don't, once. Anything still unread is listed in the report's Coverage line with the reason. "Every file" means every file.
6. **Merge** all findings into one list, renumber them `F1` … `Fn`, and write it as YAML to a temporary file outside the project (`mktemp -d`). This is `file_findings` for Step 6.

## Step 6: Dispatch the scorers

Send one message with three Agent calls, run in parallel: `subagent_type` `idm-standards:quality-scorer`, `idm-standards:usability-scorer` and `idm-standards:safety-scorer`. Each gets the same prompt:

```
project: <absolute path>
language: python
tier: <tier>
strictness: <strictness>
effort: <inspect|run|max>
plugin_root: <absolute path of $CLAUDE_PLUGIN_ROOT>
schema: <plugin_root>/skills/audit-code/scoring-schema.yaml
file_findings: <path from Step 5, or "none">

Execution results:
<everything recorded in Step 3>

Exclusions (do not report or penalize these, except critical findings, which are always reported):
<the merged exclusions from Steps 1 and 4, verbatim, or "none">
```

The agents read the criteria, finding format and rubrics themselves; don't paste them in. They see nothing else of this conversation, so the exclusions must be written out in full.

## Step 7: Score, then reconcile with the prior report

**Score.** Take each metric's score from its scorer. The weights (also in the schema) are: quality: correct 7, clear 2, concise 1; usability: simple 3, powerful 2, performant 2, documented 2, accessible 1; safety: compliant 6, reproducible 4. Within each category, the weighted mean of the scored metrics (N/A metrics are left out of both numerator and denominator) gives a raw score from 0 to 10; then

```
overall = round(quality_raw * 4 + usability_raw * 4 + safety_raw * 2)
```

and each category's score out of 100 is `round(raw * 10)`. The audit **fails** if either the quality or safety scorer returned `failed: true`.

**Collect findings.** Gather the scorers' findings plus (at max effort) the file findings, minus those a scorer dismissed. Drop any that a config directive or exclusion covers (except critical ones; see the hard floor), and note what was dropped for the Suppressed by config section.

**Reconcile.** Skip this if there was no prior report, or if the tier, strictness or config directives differ from the prior report (scores aren't comparable; say so in the report). Otherwise, match the new findings against the prior ones (same criterion and same problem, even if the line numbers moved), so each is **new**, **persisting** or **resolved**. Then, for each metric whose score changed:

- If its findings changed, the change stands. Explain it in "Score changes since last run" by citing the new or resolved findings; for a new finding, say whether the code changed (`git log --since=<prior date> -- <file>`) or the previous audit missed it.
- If its findings did not materially change, the score change is noise: keep the prior score, in either direction, and say so.

Recompute the overall score after reconciling.

## Step 8: Write the recommendations

Turn the findings into a short, ranked list of recommendations. A recommendation can group related findings (e.g. five missing docstrings in one module); each cites the finding IDs it covers. Rank by impact: critical findings first, then by how much the fix would raise the score (the metric's weight times the points at stake), with quick fixes ahead of large ones at similar impact. Each recommendation names its metric, gives effort (quick/medium/large) and whether it can be automated, and says concretely what to do.

For each recommendation that can't be automated, write a **proposed solution** in the Proposed solutions section: a concrete approach (steps, an outline or a code sketch), not a restatement of the title. Carry forward still-relevant proposed solutions and recorded user decisions from the prior report.

For Tier 2–3 reproducibility, present the lock-artifact options (`requirements_locked.txt`, `pylock.toml`, or none) rather than choosing one; `fix-code` asks the user.

## Step 9: Write code_audit.md

Write the report to the **project directory**. Get the date with `date +%Y-%m-%d`, the plugin version from `$CLAUDE_PLUGIN_ROOT/.claude-plugin/plugin.json`, and the time spent as `$(date +%s) - START_EPOCH` seconds.

The Coverage line counts source files as Step 5 defines them. At inspect and run effort, it is the number of distinct files the scorers list in `files_read` out of the total; at max effort, it should be all of them (list any that couldn't be read).

````markdown
# Code audit

- **Project**: `<project path>`
- **Tier**: <tier> (<tier name>)
- **Strictness**: <1 (strict) or 2 (material only)>
- **Effort**: <inspect, run or max>
- **Coverage**: <e.g. "read 14 of 80 source files in full" or "all 80 source files (12,450 lines) read in full">
- **Config**: <`.claude/idm-standards.md` (N directives), or none>
- **Overall score**: <overall>/100
- **Status**: <PASS, or FAIL if failed>
- **Date**: <YYYY-MM-DD>
- **Version**: idm-standards:audit-code <plugin version>
- **Time spent**: <seconds>s

## Summary

| Category | Score | Weight |
| -- | -- | -- |
| Quality | <score>/100 | 40% |
| Usability | <score>/100 | 40% |
| Safety | <score>/100 | 20% |
| **Total** | **<overall>/100** | 100% |

| Metric | Score | Notes |
| -- | -- | -- |
| correct | <score>/10 | <reason> |
| ... one row per metric; N/A metrics show `N/A` in the Score column ... |

<2–4 plain-language sentences: strongest areas, biggest gaps, and, if the audit failed, which finding caused it.>

## Execution

<At inspect effort, this section is the single line "Not run (inspect effort)." Otherwise:>

- **Tests**: <command> → <N passed, M failed, K errors, in T s>, or <why they couldn't run, or "no tests found">
- **README example**: <ran successfully / failed: error / not found / not run: reason>

## Score changes since last run

<Only if reconciled (Step 7). One line per changed metric: prior → new, with the finding IDs that explain it. Also list resolved findings. If a score change was treated as noise, say "scored <x> this run but kept the prior <y>: findings unchanged".>

## Recommendations

1. **<metric>: <title>** *(effort: quick/medium/large; automated: yes/no; findings: Q1, F12)*
   <What to do, in one to three sentences. Don't repeat the findings' detail; the Findings section has it.>

## Suppressed by config

<Only if a config was found. One bullet per directive, quoted, with what it matched this run (or "nothing matched"). Critical findings a directive seemed to cover are listed as "reported despite config directive".>

## Proposed solutions

<For each recommendation marked automated: no, a concrete proposed approach. Then carried-forward items and recorded user decisions, e.g. "Lock artifact: none; user opted out (2026-06-10). Do not re-recommend." fix-code adds to this section. Config directives are not repeated here.>

## Findings

<Every finding the scorers reported, grouped by metric (in the order of the Summary table), most severe first, one line each, copied tersely. Below max effort, end with the number of low-severity findings left out.>

### correct

- **Q1** · high · `sim/model.py:42-68` · correct.2: <problem> **Fix**: <fix> *(quick; automatable)*

<...one subsection per metric with findings. At max effort, end with a "Dismissed on review" list: each file-review finding a scorer rejected, with the reason.>

## Full results

```yaml
project: <path>
tier: <tier>
strictness: <strictness>
effort: <effort>
coverage: {files_read: <n>, source_files: <total>}
overall_score: <overall>
failed: <true|false>
execution: {tests: <short summary>, readme_example: <short summary>}
scores:
  quality: {correct: <score>, clear: <score>, concise: <score>}
  usability: {simple: <score>, powerful: <score or N/A>, performant: <score>, documented: <score>, accessible: <score or N/A>}
  safety: {compliant: <score>, reproducible: <score>}
config: <list of directives verbatim, or none>
```
````

If the audit failed, still write the full report; the recommendations start with how to fix the failure.

## Step 10: Offer to fix

If running interactively and invoked directly (not by `audit-project` or another skill), finish with one AskUserQuestion: **"Apply the fixes now?"** with options "Yes, run fix-code now (Recommended)" and "No, I'll review the report first". If yes, invoke the `fix-code` skill on the project. Otherwise, and in non-interactive runs, just say where the report is. Below max effort, mention in one line the higher effort levels: `run` (also runs the tests and README example) and `max` (also reads every source file).
