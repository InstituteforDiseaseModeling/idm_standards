# Changelog

This document tracks updates to the IDM-Standards plugin (formerly three separate plugins: IDM-Eng-Plugin, IDM-Docs-Plugin, and IDM-Uplifter-Plugin; their pre-merge histories are preserved below).

## Version 2.0 (2026.06.10)

- **Merged the three IDM plugins into one**: `idm-eng-plugin`, `idm-docs-plugin`, and `idm-uplifter-plugin` are now a single `idm-standards` plugin, so one install provides the full suite while every skill remains individually invocable.
- **Renamed all skills verb-first**: `eng-quality-checker` → `audit-code`, `eng-quality-fixer` → `fix-code`, `docs_audit` → `audit-docs`, `diataxis` → `audit-diataxis`, `personas` → `audit-personas`, `python-docstrings` → `audit-docstrings`, `idm-code-uplifter` → `audit-code-exhaustive`.
- **Renamed output files to match**: `engineering_score.md` → `code_audit.md`, `uplifter_report.md` → `code_audit_exhaustive.md`, `.uplifter_cache/` → `.audit_cache/` (fixers fall back to reading `engineering_score.md` for compatibility).
- **New skills**: `audit-r-code` (R-specific engineering audit, invoked automatically for R projects), `audit-project` (runs code and/or docs audits with one set of questions), and `fix-project` (applies fixes from whichever audit reports exist).
- **Tier confirmation**: `audit-code` now infers a suggested tier from the codebase and asks the user to confirm it before scoring (an explicitly passed tier skips the prompt).
- **Strictness setting**: a second question alongside tier — strictness 1 (report everything, previous behavior) or 2 (only findings that materially affect usage; stylistic/convention findings are neither penalized nor reported).
- **Relaxed lockfile guidance**: Tier 1 (library) projects are never told to add a lock file; for Tier 2/3 the fixer asks the user to choose between `requirements_locked.txt` (simple), `pylock.toml` via `pip lock` (advanced), or none, and the choice is recorded so re-runs don't nag.
- **Score reconciliation across re-runs**: scorers still score fresh, but the skill now compares against the prior report and must justify any score decrease with concrete regression evidence or a specific previously-missed finding; unjustifiable drops retain the prior score. Justifications appear in a "Score changes since last run" report section.
- **Proposed solutions in the report**: recommendations that can't be automated get concrete proposed approaches, and the fixers record skipped/unfixable items (and user decisions) in a "Proposed solutions" section of the audit report.
- **Audit→fix chaining**: each audit ends by offering to run its fix counterpart immediately.
- Added an eval harness (`evals/` at the repo root) with fixture projects and round-trip checks (score must not decrease after fixes; implemented fixes must not be re-identified).
- **User config file**: a project can commit `.claude/idm-standards.md` (flexible naming — any root/`.claude` file whose name contains `idm` + `standard(s)` and ends in `.md`) with plain-English directives like "don't recommend renaming classes to CamelCase". Every audit and fix skill discovers it and suppresses matching findings (neither penalized, recommended, nor fixed), with an optional git-ignored `.claude/idm-standards.local.md` for personal overrides and frontmatter `tier`/`strictness` defaults. A **hard floor** means directives can never waive serious findings (exposed secrets, PII, license violations, scientific-correctness bugs, CRITICAL exhaustive findings) — these are always scored and reported. Reports gain a `Config` line and a "Suppressed by config" section so nothing is dropped silently. Discovery, precedence, and the floor are defined once in `reference/user-config.md`.

---

## Pre-merge history: IDM-Eng-Plugin

### Version 1.0 (2026.04.07)
- Copied from Starsim-AI's [Project-Improver](https://github.com/starsimhub/starsim_ai) v1.2 (2026.03.31).

## Pre-merge history: IDM-Docs-Plugin

### Version 1.1 (2026.04.20)
- Updated the `diataxis` skill to reflect IDM's topic-type guidance refresh: terminology now uses "how-to(s)" instead of "how-to guide(s)", and the skill frames IDM's approach as borrowing from Diátaxis rather than strictly following it.
- Added guidance in the `diataxis` skill on IDM's divergence from Diátaxis for TOC organization: tutorials and reference at the top level, with how-to and explanation topics grouped into subject-matter "user guides" (explanation topics typically as the parent).
- Updated the `docs_audit` skill to reference the user-guide grouping pattern when evaluating documentation structure.
- Fixed a broken `references` symlink in the `diataxis` skill so the topic-type reference files load correctly.

### Version 1.0 (2026.04.13)
- Initial release.

## Pre-merge history: IDM-Uplifter-Plugin

### 0.2_2026.05.06

- Split repo-level review into a dedicated `idm-repo-reviewer` agent, dispatched in parallel with the first file wave instead of running inline in the orchestrator.
- Inlined review checklists into both agents and removed `agents/metrics.yaml`. The file-level checklist now lives in `idm-code-reviewer.md`; the repo-level checklist lives in `idm-repo-reviewer.md`. Secrets remain checked at both scopes intentionally.
- Added a top-of-report **Summary** section: severity counts across all blocks, all CRITICALs lifted to the top with file/line, and top recurring criteria.
- Added resumability via `.uplifter_cache/`: each completed block is written to disk as it lands, and a re-run can reuse cached blocks for unchanged files.
- Switched the agent input format to XML-style tags (`<file>...</file>`, `<repo_root>...</repo_root>`) for unambiguous parsing.
- Added an explicit scope rule to both agents and the skill: never read files outside `<repo_root>`. Glob/Grep/Read/Bash are constrained to the project tree.
- Added a per-file size guard (~200 KB / ~5000 lines) and binary-file check; oversized/binary files are skipped and logged in the failures section.
- Anchor collisions in the index are resolved by appending `-2`, `-3`, etc.
- Added two more triggering examples to `idm-code-reviewer.md` and three to the new `idm-repo-reviewer.md`.
- Updated the README to reflect the actual current behavior (no longer described as a skeleton).

### 0.1_2026.04.27

- Initial scaffold: `idm-code-uplifter` skill and `idm-code-reviewer` agent skeleton.
- Review criteria in the agent are placeholder content to be replaced by the plugin owner.
