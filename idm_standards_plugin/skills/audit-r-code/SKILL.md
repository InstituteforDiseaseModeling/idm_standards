---
name: audit-r-code
description: The Audit-R-Code skill scores an R project against IDM engineering quality tiers (1–3) across quality, usability, and safety metrics, and writes a code_audit.md report. Use this skill when the project being audited is written in R (DESCRIPTION file, renv.lock, or mostly *.R files) — including when the user asks to "audit my code", "score my project", or "check engineering quality" for an R project, or invokes /idm-standards:audit-r-code. For Python projects, use audit-code instead.
argument-hint: "[project_path_or_github_url] [tier] [strictness]"
allowed-tools: Read, Glob, Grep, Bash, Write, Agent, WebFetch, AskUserQuestion, Skill
---

Score an R project against the IDM engineering quality guidelines (including the R-specific guidance in `eng_guidance/2b_r.md`, which defers to the [Tidyverse style guide](https://style.tidyverse.org/) for style) and write a `code_audit.md` report.

Skill version: 2.0_2026.06.10

## Workflow

This skill follows **exactly the same workflow as `audit-code`** — read `$CLAUDE_PLUGIN_ROOT/skills/audit-code/SKILL.md` now and follow its Steps 0–10 (start time; argument parsing; tier/strictness confirmation; prior-report reading; parallel sub-agent dispatch; score computation; score reconciliation; recommendations and proposed solutions; writing `code_audit.md`; offering to fix), with the R-specific differences below.

### Difference 1: Language routing (replaces audit-code Step 1 detection)

This skill is for R projects: a `DESCRIPTION` file, an `renv.lock`, or a majority of source files being `*.R`/`*.Rmd`. If the project turns out to be mainly Python, stop and invoke `audit-code` instead. For substantial Python+R mixes (each ≥25% of source files), ask the user which audit to run (or both) — but in non-interactive contexts, or when invoked by `audit-project`, default to auditing whichever language has more source files (ties → R, since this skill was selected) and note the choice in the report.

### Difference 2: Scoring schema (replaces audit-code Step 3)

Read the R schema from:
`$CLAUDE_PLUGIN_ROOT/skills/audit-r-code/r-scoring-schema.yaml`

Category weights, metric weights, N/A rules, and failure conditions are identical to the Python schema; the rubric anchors are R-specific.

### Difference 3: Tier inference signals (audit-code Step 2)

When inferring a suggested tier:
- `DESCRIPTION` + `NAMESPACE` + `man/` + CRAN/r-universe publication + CI → suggest Tier 1 (package)
- `renv.lock` (or `DESCRIPTION` without package skeleton), `R/` functions, some tests, README → suggest Tier 2 (shared research code)
- Loose `.R`/`.Rmd` scripts, single author → suggest Tier 3 (one-off)

### Difference 4: R-specific exploration instructions (audit-code Step 5)

Use the same three agents (`quality-scorer`, `usability-scorer`, `safety-scorer`) with the same prompt templates, strictness block, and user-decisions block as audit-code, but replace the per-agent "Instructions" lists with these R-specific versions (and paste the rubrics from the **R** schema):

**quality-scorer instructions (R)**:
1. Explore the project: read key source files (`R/`, scripts, `*.Rmd`), check structure, naming, roxygen2 comments, duplication.
2. Run `find <project> -name "*.R" -o -name "*.Rmd"` to discover files.
3. Check for tests: `tests/testthat/test-*.R`, runnable via `testthat::test_dir()`; for packages, `Config/testthat/edition: 3` in DESCRIPTION. Check if tests cover the core scientific functions and double as documentation.
4. For Tier 1: check CI (`.github/workflows/` using r-lib/actions: R-CMD-check, test-coverage, lint, pkgdown) and whether `R CMD check` would plausibly pass 0/0/0.
5. Grep for red flags: `setwd(`, `rm(list = ls())`, absolute paths (`/home/`, `/Users/`, `C:/`), `library(` calls inside `R/` for packages (should use namespacing or @importFrom).
6. Look for obvious bugs, scientific errors, or suspicious logic; check for evidence of peer review or validation.
7. Score each metric as an integer 0–10. Style findings (Tidyverse adherence, lintr/Air configs) count only at strictness 1, and only for clarity/conciseness — never for correctness.

**usability-scorer instructions (R)**:
1. Explore the project: read README (or README.Rmd), vignettes, pkgdown config (`_pkgdown.yml`); identify the main entry points (exported functions, run scripts, or a `_targets.R` pipeline).
2. Check if it is clear what UIs the user is supposed to interact with (exported functions for packages; numbered scripts or targets pipeline for research code).
3. Check roxygen2 coverage on exported/major functions — do they have `@param`, `@return`, and runnable `@examples`?
4. Check for performance anti-patterns: growing vectors in loops (`c()`, `rbind()` in a loop), `for` loops where vectorized/apply-family operations are natural, repeated `read.csv` of the same file.
5. For accessible: check GitHub presence, LICENSE, installability (`DESCRIPTION` for packages — `remotes::install_github()` or CRAN; `renv::restore()` for research code).
6. Score each non-N/A metric as an integer 0–10 (Tier 3: omit `powerful` and `accessible`).

**safety-scorer instructions (R)**:
1. Check for exposed secrets: grep for api_key/token/password literals; check `.Renviron` is gitignored and credentials use `Sys.getenv()`.
2. Check for LICENSE file and identify license type.
3. Inspect `DESCRIPTION` Imports/Depends and `renv.lock` for restrictive licenses.
4. Check dependency specification per the lock-artifact rules below.
5. Check `set.seed()` usage: if random numbers are used, are seeds set/configurable so the same seeds give identical results?
6. For Tier 1 and 2: check version control — git tags, semantic versioning, `NEWS.md`.
7. For Tier 1: check CRAN (`curl -I https://cran.r-project.org/web/packages/<package>/DESCRIPTION`) or r-universe publication.
8. Score each metric as an integer 0–10.

**Lock-artifact rules for R (replace audit-code's Python rules in the safety prompt)**:
- Tier 1 (package): dependencies in `DESCRIPTION` (Imports, not Depends), as loose as possible; **never suggest renv or a lock file for a package** — packages must work across dependency versions. Flag `packrat/` as deprecated (suggest `renv::migrate()`).
- Tier 2/3 (research code): if reproducibility of results matters, suggest **renv** (`renv.lock` + `.Rprofile` + `renv/` committed, `renv::status()` clean) as the standard, or a `DESCRIPTION` + dated Posit Package Manager snapshot as the lightweight alternative. "None" is also a legitimate, recordable user decision — if recorded, do not penalize or re-recommend.

### Difference 5: Report and fix chaining

The report file, format, and header are identical to audit-code (Step 9) — including the **Version** line, which should read `idm-standards:audit-r-code v<version>`. The final offer-to-fix (Step 10) invokes `fix-code` as usual; fix-code adapts its patterns to R (roxygen2, testthat, DESCRIPTION, `renv::snapshot()`).

## Notes

- All audit-code notes apply (general scoring principle, skip large/binary files, read every source file, complete the report even on FAIL).
- For R projects: look for `DESCRIPTION`, `NAMESPACE`, `R/`, `tests/testthat/`, `vignettes/`, `man/`, `renv.lock`, `_targets.R`, `.lintr`, `air.toml`.
- Style is scored against the Tidyverse style guide; at strictness 2, style findings are neither penalized nor reported.
