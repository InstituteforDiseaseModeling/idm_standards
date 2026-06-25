# R style and engineering practice

This page is the R counterpart to the [Python guidance](2_python.md). It is deliberately short: for style, follow the [Tidyverse style guide](https://style.tidyverse.org/) (which builds on the [Google R style guide](https://google.github.io/styleguide/Rguide.html)), and that's most of it. IDM has no house R style rules beyond Tidyverse. What this page adds is IDM's expectations for R *engineering practice* — dependencies, testing, project structure, documentation, and CI — organized by [code tier](engineering_quality_guidelines.md#code-tiers).

## Style

- Follow the [Tidyverse style guide](https://style.tidyverse.org/): snake_case names, `<-` for assignment, meaningful function names (verbs), pipes for readable chains.
- Enforce mechanically rather than by hand: [lintr](https://lintr.r-lib.org/) for static analysis (a `.lintr` file at the repo root, via `lintr::use_lintr()`), and [Air](https://posit-dev.github.io/air/) (or [styler](https://styler.r-lib.org/)) for formatting. Air is the modern, fast option (the R analogue of `ruff format`), configured via `air.toml` (`usethis::use_air()`).
- As with Python, the aim is not complete uniformity — these tools handle the mechanical part so review can focus on substance.

## Managing R dependencies

The R equivalents of the [Python dependency guidance](2_python.md#managing-python-dependencies):

- **Packages (Tier 1)**: dependencies go in `DESCRIPTION` (`Imports`, not `Depends`; `Suggests` for test/documentation-only dependencies), as loosely as possible — version bounds only when older versions are genuinely known not to work. Packages should *not* include a lock file.
- **Research code where results must be reproducible (Tier 2/3)**: use [renv](https://rstudio.github.io/renv/). A healthy renv setup commits `renv.lock`, `.Rprofile`, `renv/activate.R`, and `renv/settings.json`, and `renv::status()` reports the project synchronized. Note that renv does not capture the R version itself beyond recording it — state the R version in the README too.
- **Lightweight alternative**: for simple projects where full renv feels heavy, a `DESCRIPTION` file plus a dated [Posit Public Package Manager](https://packagemanager.posit.co/) snapshot URL in the README gives approximate reproducibility at much lower cost. As with Python, "no lock artifact" is a legitimate choice for the project owner if results don't need exact reproduction.
- **packrat is deprecated**: if a project still uses `packrat/`, migrate with `renv::migrate()`.

## Testing

- Use [testthat](https://testthat.r-lib.org/) (edition 3: `Config/testthat/edition: 3` in `DESCRIPTION`). Test files in `tests/testthat/test-*.R`, mirroring the files in `R/`.
- testthat also works outside packages via `testthat::test_dir()` — shared research code should have at least a few tests covering the core scientific functions.
- As with Python, tests should primarily check end-to-end scientific correctness (parameter behavior, edge cases), not just units; see the [testing guidance](3_tests.md).
- For packages, `R CMD check` should pass with 0 errors, 0 warnings, 0 notes.

## Project structure (research code)

- One repo = one project: never `setwd()` or `rm(list = ls())` in committed code; build all paths with [here](https://here.r-lib.org/)`::here()` relative to the project root, never absolute paths.
- Factor reusable functions into `R/`, separate from the scripts that run the analysis; number run scripts if order matters, or use a [targets](https://docs.ropensci.org/targets/) pipeline (`_targets.R`) for anything with multiple slow, interdependent steps.
- Keep raw data immutable and separate from derived data (for example, `data/raw/` vs `data/derived/`).
- `set.seed()` wherever randomness affects results; keep credentials in `.Renviron` (gitignored), accessed via `Sys.getenv()`.

## Documentation

- Document functions with [roxygen2](https://roxygen2.r-lib.org/) comments; for packages, every exported function needs `@param`, `@return`, and a runnable `@examples`, and `NAMESPACE` is generated (never hand-edited).
- Packages: README (ideally `README.Rmd` rendered to `README.md`), `NEWS.md` as the changelog, at least one vignette, and a [pkgdown](https://pkgdown.r-lib.org/) site.
- Research code: a README with purpose, installation (`renv::restore()`), how to run, and repo structure — see the [documentation guidance](4_documentation.md).

## Continuous integration

- Use [r-lib/actions](https://github.com/r-lib/actions) (v2) for GitHub Actions; install standard workflows with `usethis::use_github_action()`.
- Packages (Tier 1): `R-CMD-check.yaml` (the standard 3-OS × R release/devel/oldrel matrix), plus test coverage, lint, and pkgdown workflows.
- Research code (Tier 2): a single workflow that restores the renv library (`r-lib/actions/setup-renv`) and runs the tests or pipeline is usually enough.

## Expectations by tier

Using the [IDM code tiers](engineering_quality_guidelines.md#code-tiers) (Tier 1 = library/package, Tier 2 = shared research code, Tier 3 = one-off):

- **Tier 3**: git repo; README with purpose and entry point; dependencies discoverable (`library()` calls at the top of scripts); no `setwd()`/absolute paths; `set.seed()` where randomness matters; no secrets in the repo.
- **Tier 2**: all of the above, plus healthy renv (or `DESCRIPTION` + dated snapshot); functions factored into `R/`; `here::here()` for paths; some testthat tests; Tidyverse style with lintr; LICENSE file; raw vs derived data separated; CI recommended.
- **Tier 1**: all of the above, plus the standard package skeleton (`DESCRIPTION`, generated `NAMESPACE`, `man/`, `tests/testthat/`, `vignettes/`, `NEWS.md`); `R CMD check` 0/0/0; full CI; pkgdown site; published on CRAN (or [r-universe](https://r-universe.dev/) as an interim); no `library()` calls inside `R/` (use namespacing or `@importFrom`).
