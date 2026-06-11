---
name: fix-code
description: The Fix-Code skill reads recommendations from a code_audit.md report and implements prioritized improvements to the project. Use this skill when the user asks to "fix my project", "implement the recommendations", "improve my project score", "apply engineering fixes", or invokes /idm-standards:fix-code. Also use when the user says "now fix it" after running audit-code.
argument-hint: "[project_path]"
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, AskUserQuestion
---

Read recommendations from `code_audit.md` and implement prioritized improvements to the project.

Skill version: 2.0_2026.06.10

## Step 1: Find and Read the Audit Report

1. If the user provided a `project_path`, look for `code_audit.md` in that directory.
2. Otherwise, look in the current working directory.
3. For compatibility with earlier plugin versions, fall back to `engineering_score.md` if `code_audit.md` does not exist.
4. If neither file exists, stop and tell the user:
   > "No `code_audit.md` found. Please run `/idm-standards:audit-code` first to generate the report."

Read the full contents of the report — particularly the **Recommendations**, **Proposed solutions**, and **Full Results** sections, and the **Tier** and **Strictness** fields in the header.

Respect what the report records:
- **Strictness**: if the report was generated at strictness 2 (material only), don't introduce fixes for stylistic issues the audit deliberately excluded.
- **User decisions** in the Proposed solutions section (e.g. "Lock artifact: none — user opted out"): do not re-raise them.
- **User config**: discover the project's idm-standards config following `$CLAUDE_PLUGIN_ROOT/reference/user-config.md` (read it now). Never implement a fix that a config directive suppresses — and the config **wins over the report**: if an older `code_audit.md` (generated before the config existed) still lists a now-suppressed recommendation, skip it. The hard floor still applies: directives can't stop you from fixing a serious finding (exposed secret, license violation, etc.) — those remain fix-or-flag.

## Step 2: Create a Prioritized Implementation Plan

Parse the recommendations and classify each as:

| Category | What it means |
|----------|---------------|
| **Can implement now** | File additions, code edits, config files, docstrings, README improvements, `.gitignore`, `LICENSE` |
| **Requires human input** | Writing tutorials, user guides, scientific validation, publishing to PyPI/CRAN, setting up CI/CD (you can scaffold, but the user must configure credentials) |
| **Cannot implement** | Fundamental redesigns, decisions about what the code should do, acquiring data licenses |

Present the plan to the user **before making any changes**:

```
## Implementation Plan

### Will implement automatically:
1. [Metric: clear] Add docstrings to 5 public functions in model.py (quick)
2. [Metric: accessible] Add MIT LICENSE file (quick)
3. [Metric: documented] Expand README with installation and usage sections (medium)
4. [Metric: concise] Refactor duplicated data loading code into a helper function (medium)

### Will scaffold (you complete):
5. [Metric: correct] Create tests/ directory with pytest structure and 3 example tests (medium)
   → You'll need to fill in the test logic and expected values
6. [Metric: accessible] Create pyproject.toml for pip installability (medium)
   → You'll need to fill in the project description and verify metadata

### Will ask you about:
7. [Metric: reproducible] Capture exact dependency versions (quick)
   → Choice of requirements_locked.txt, pylock.toml, or none — see Step 3

### Cannot implement (human effort required):
- [Metric: documented] Write a full tutorial notebook — requires domain knowledge
- [Metric: correct] Add CI/CD pipeline — requires GitHub repository secrets setup
- [Metric: correct] Validate scientific correctness — requires domain expert review

Estimated score improvement: +12 to +18 points (depending on test coverage achieved)

Proceed? (yes/no)
```

If config directives suppressed any recommendations from the report, list them under a **"Skipped per your config"** heading in the plan (quoting the directive) rather than dropping them silently — but never skip a serious safety/correctness fix on account of a directive. Wait for the user to confirm before making any changes.

## Step 3: Implement Approved Changes

Work through the "Will implement" items **one at a time**, in priority order (impact = score x weight, highest first).

### Before each change:
- State what you are about to do in one sentence
- Read the relevant file(s) before editing them

### For each type of fix:

#### Capturing exact dependency versions (Tier 2/3 only)

**Never do this for a Tier 1 (library) project** — libraries should not have lock files, and this recommendation should not appear in a Tier 1 report.

For Tier 2/3, ask the user with a single AskUserQuestion — which lock artifact do they want?
- **`requirements_locked.txt`** via `pip freeze > requirements_locked.txt` — simple, human-readable (recommended default for Tier 3 / simple projects)
- **`pylock.toml`** via `pip lock` (PEP 751; requires pip ≥25.1) — the standardized format (recommended default for Tier 2 / more advanced projects)
- **None** — skip capturing exact versions

Implement the chosen option (running the command in the project's environment if possible, or documenting the command in the README if not). If the user chooses **None**, record the decision in the report's Proposed solutions section (see Step 5) so future audits and fixes don't re-raise it.

For R projects, the equivalent is `renv::snapshot()` (producing `renv.lock`); offer that instead.

#### Adding a LICENSE file
Use the MIT license template with the current year and repo/author name from the README or git config:
```
MIT License

Copyright (c) <year> <author>

Permission is hereby granted, free of charge, to any person obtaining a copy...
[full MIT text]
```

#### Adding/improving docstrings (Python)
Follow Google docstring style. For a function:
```python
def function_name(param1, param2):
    """ Short one-line description.

    Longer description, if needed.

    Args:
        param1 (type):  Description of param1.
        param2 (type):  Description of param2.

    Returns:
        type: Description of return value.

    **Example**:
    
        function_name(param1, param2) # Give short usage example
    """
```

#### Adding/improving docstrings (R)
Use roxygen2 style:
```r
#' Short one-line description.
#'
#' @param param1 Description of param1.
#' @param param2 Description of param2.
#' @return Description of return value.
#' @export
#' @examples
#' result <- function_name(1, 2)
```

#### Scaffolding a test file (Python)
Create `tests/test_<module>.py`:
```python
"""Tests for <module>."""
import pytest
# TODO: import from your module
# from mymodule import MyClass, my_function

def test_basic():
    """TODO: Test basic expected behavior."""
    # result = my_function(...)
    # assert result == expected
    pass

def test_edge_case():
    """TODO: Test edge case."""
    pass

if __name__ == "__main__":
    pytest.main(['-x', '-v', __file__]) # Run tests as script
```
Also check for a `pytest.ini` or add to `pyproject.toml`.

#### Scaffolding a test file (R)
Create `tests/testthat/test-<name>.R` (plus `tests/testthat.R` if the project is a package):
```r
test_that("basic expected behavior", {
  # TODO: result <- my_function(...)
  # expect_equal(result, expected)
  skip("TODO: fill in test logic")
})

test_that("edge case", {
  skip("TODO: fill in test logic")
})
```

#### Scaffolding a pyproject.toml
```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "<project-name>"
version = "0.1.0"  # TODO: update to current version
description = "<TODO: one-line description>"
readme = "README.md"
license = {file = "LICENSE"}
requires-python = ">=3.9"
dependencies = [
    # TODO: list your dependencies here
]

[project.urls]
Repository = "<TODO: GitHub URL>"
```

#### Scaffolding a DESCRIPTION file (R)
```
Package: <project.name>
Title: <TODO: One-Line Title in Title Case>
Version: 0.1.0
Authors@R: person("<First>", "<Last>", email = "<email>", role = c("aut", "cre"))
Description: <TODO: a paragraph describing what the package does.>
License: MIT + file LICENSE
Encoding: UTF-8
Roxygen: list(markdown = TRUE)
Imports:
```

#### Improving README
Add missing sections. A Tier 3 (one-off) README needs at minimum:
- `## Overview` — what the project does (1–3 sentences, accessible to a general audience)
- `## Installation` — how to set it up
- `## Usage` — how to run it (minimal example)

A Tier 1 and 2 README additionally needs:
- `## Requirements`
- `## Project structure` — brief description of key files/folders
- `## Contributing` (Tier 1 library, unless separate CONTRIBUTING.md file exists)

#### Fixing code duplication
Identify the duplicate code, extract it into a well-named helper function, and replace the duplicates with calls to that function. Only refactor when it clearly improves readability — do not create unnecessary abstractions.

## Step 4: Handle Trade-offs

If implementing one recommendation would negatively impact another metric, **stop and ask the user** before proceeding:

> "Implementing [recommendation A] (e.g., adding strict type validation) would make the API less flexible, potentially lowering the `powerful` score. How would you like to proceed?
> - (a) Proceed with stricter validation (prioritize simplicity/safety)
> - (b) Skip this recommendation (preserve flexibility)
> - (c) Implement a middle ground (add validation but make it optional via a flag)"

## Step 5: Record Proposed Solutions and Report What Was Done

**Update the audit report** (`code_audit.md`): for every item you classified as "Requires human input" or "Cannot implement" — and any item the user chose to skip — write an entry in the report's **Proposed solutions** section (creating the section if it doesn't exist). Each entry should contain:

- The issue and the metric it affects
- A **concrete proposed approach** the user could follow: steps, an outline, or a code sketch — not just a restatement of the title
- The estimated effort, and why it can't be automated
- Any user decisions made during this run (e.g. "Lock artifact: none — user opted out (YYYY-MM-DD). Do not re-recommend."), so future audit and fix runs respect them

Do not modify the report's scores or other sections.

**Offer to persist durable preferences.** If during this run the user made a decision that should apply to *every* future audit (not just this report) — e.g. "stop recommending type hints", or a permanent opt-out — offer to save it as a directive in `.claude/idm-standards.md` (create the file from the template in `$CLAUDE_PLUGIN_ROOT/reference/user-config.md` if absent). Per-run-only decisions stay in the report's Proposed solutions, as above; durable ones belong in the config. If you create a `.local.md` overlay, offer to add `.claude/*.local.md` to the project's `.gitignore`.

Then provide a concise summary in chat:

```
## Changes Made

✅ Added MIT LICENSE
✅ Added docstrings to 7 functions in model.py and utils.py
✅ Created requirements_locked.txt via pip freeze (user's choice)
✅ Expanded README with Installation, Usage, and Project Structure sections
✅ Scaffolded tests/test_model.py (fill in test logic to complete)

⏭ Skipped: user guide (human effort required — proposed outline added to code_audit.md)
⏭ Skipped: CI/CD pipeline (human effort required — proposed workflow added to code_audit.md)

Estimated score impact: quality.clear +2, usability.documented +2, safety.reproducible +2, usability.accessible +3

Re-run `/idm-standards:audit-code` to get an updated score.
```

## Notes

- Only make changes that are clearly safe and reversible. If a change could break existing functionality, note it and ask the user to verify.
- If the project is R-based, adapt all Python-specific patterns to R equivalents (roxygen2 docstrings, testthat tests, DESCRIPTION metadata, renv for dependencies).
- If the `failed` flag is `true` in the audit report, prioritize the failure-causing metric first and be explicit about what was done to address it.
