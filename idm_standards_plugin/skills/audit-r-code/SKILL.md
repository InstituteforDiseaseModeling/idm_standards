---
name: audit-r-code
description: The Audit-R-Code skill scores an R project against IDM engineering quality tiers (1–3) across quality, usability, and safety metrics, and writes a code_audit.md report of scores, findings, and prioritized recommendations. Use this skill when the project being audited is written in R (DESCRIPTION file, renv.lock, or mostly *.R files) — including when the user asks to "audit my code", "score my project", or "check engineering quality" for an R project, or invokes /idm-standards:audit-r-code. For Python projects, use audit-code instead.
argument-hint: "[project_path_or_github_url] [tier] [strictness] [effort]"
allowed-tools: Read, Glob, Grep, Bash, Write, Agent, WebFetch, AskUserQuestion, Skill
---

Score an R project against the IDM engineering quality guidelines (including the R guidance in `eng_guidance/2b_r.md`, which defers to the [Tidyverse style guide](https://style.tidyverse.org/)) and write a `code_audit.md` report.

## Workflow

Follow **exactly the same workflow as `audit-code`**: read `$CLAUDE_PLUGIN_ROOT/skills/audit-code/SKILL.md` now and follow its Steps 0–10, including both effort levels. Only these things differ:

1. **Language routing** (Step 1): this skill is for R projects. If the project turns out to be mainly Python, stop and invoke `audit-code` instead. For a substantial Python+R mix in a non-interactive run, ties go to R.
2. **Tier inference** (Step 2):
   - `DESCRIPTION` + `NAMESPACE` + `man/`, published on CRAN or r-universe, with CI → suggest Tier 1 (package).
   - `renv.lock` (or a `DESCRIPTION` without a package skeleton), functions in `R/`, some tests, a README → suggest Tier 2 (shared research code).
   - Loose `.R`/`.Rmd` scripts by one author → suggest Tier 3.
3. **Running the code** (Step 3): run tests with `Rscript -e 'testthat::test_local()'` for a package, or `Rscript -e 'testthat::test_dir("tests/testthat")'` otherwise. If the project uses renv and the library isn't restored, ask before running `renv::restore()` (interactive), or record "could not run".
4. **Agents** (Steps 5–6): pass `language: r` and `schema: <plugin_root>/skills/audit-r-code/r-scoring-schema.yaml`. The agents carry their own R-specific checks (roxygen2, testthat, renv, Tidyverse style, R red flags), so nothing else changes.
5. **Report** (Step 9): the Version line reads `idm-standards:audit-r-code <plugin version>`. The offer to fix still invokes `fix-code`, which adapts to R (roxygen2, testthat, DESCRIPTION, `renv::snapshot()`).
