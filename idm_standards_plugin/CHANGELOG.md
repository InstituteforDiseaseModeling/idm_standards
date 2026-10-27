# Changelog

This document tracks updates to the IDM-Standards plugin (formerly three separate plugins: IDM-Eng-Plugin, IDM-Docs-Plugin, and IDM-Uplifter-Plugin; their pre-merge histories are preserved below).

## Version 3.0 (2026.10.26)

- **Audits are built on findings.** The scorer agents now return a list of findings (a specific problem, its location, severity, and a concrete fix) and score each metric from them, instead of a score and a one-sentence reason. Recommendations are written from the findings and cite their IDs, the report lists every finding, and `fix-code` works from them directly. Scores can now be traced to evidence.
- **Three effort levels: inspect, run, max.** `inspect` (the default) reads the code and runs nothing. `run` also runs the project's tests and README quick-start example before scoring, and the scorers use the results; a new **Execution** report section records what happened. It is not the default because running project code can have side effects. `max` also has every source file read in full (see below). When the audit ran the tests, `fix-code` re-runs them after its changes and never leaves more failures than it found.
- **Max effort replaces `audit-code-exhaustive`.** `/idm-standards:audit-code . <tier> <strictness> max` runs the code and splits the project's source files into batches and has parallel file-reviewer agents read every line of every file before scoring, with a coverage check that every file was read. The old `audit-code-exhaustive` skill, its agents, `code_audit_exhaustive.md` and `.audit_cache/` are removed. Every report now has a **Coverage** line saying how many source files were read in full.
- **Fairer score changes between runs.** A score change is accepted only if the findings behind it changed (new or resolved findings, cited in "Score changes since last run"); otherwise it is treated as noise and the prior score kept, in either direction. Previously only decreases were checked, so scores could drift up but not down.
- **One source of truth.** The checklist now lives in `reference/criteria.yaml`, mirroring the guidelines item by item, and the finding format in `reference/findings.md`. `audit-code` dispatches the named scorer agents, which read these and the scoring schema themselves, instead of pasting long prompts whose rubrics had drifted from the schema. The scorers inherit the session's model instead of being pinned to Sonnet.
- **Broader privacy check, and the repo root is scored.** The safety scorer now checks every tracked file for private and sensitive material, not just secrets and patient data: internal documents (draft proposals, project plans, notes about named people) and developers' personal information (home-directory paths with usernames, personal email addresses). A cluttered repo root (scratch scripts, outputs, obsolete folders) is now an explicit `clear.1` finding instead of an unscored note.
- **Speed.** The audit asks the effort level alongside tier and strictness. When running code, it makes one attempt without debugging the environment. Below max effort it keeps findings to a sentence or two and leaves out low-severity findings (giving their count); max effort still reports everything.
- **Simpler config file.** The config is read only from `.claude/idm-standards.md` (the flexible file-name matching and the `.local.md` overlay are gone). The hard floor is defined once.
- **`audit-docstrings` is no longer LASER-specific.** Its examples, cross-reference list and researcher workflow were LASER's; they are now generic, and the workflow stages are taken from the audited project's own docs. It also no longer contradicts itself about `Examples:` sections (plural, no code fence). The same change is made in `eng_guidance/4_documentation.md`. `audit-docstrings` and `audit-docs-structure` gained a review mode with a defined output.
- **`audit-personas` ships its persona definitions** (it previously pointed at files not included in the installed plugin).
- Smaller fixes: N/A metrics are shown as N/A rather than 10/10; the score formula in the schema headers was wrong by a factor of 10; per-skill version lines are gone (reports use the plugin version).

## Version 2.2 (2026.07.21)

- **`audit-docstrings` now checks parameter semantics.** A docstring can pass every other check and still leave a parameter's meaning ambiguous — e.g. a threshold with no stated bound direction, or a path with no stated absolute/relative form. The skill now flags gaps like these. This guidance is sourced from `eng_guidance/4_documentation.md`, which the sync skills now know to treat as `audit-docstrings`' canonical source even though it lives outside `docs_guidance/`.
- **`audit-docs-structure` no longer contradicts IDM's TOC guidance.** It previously told reviewers that top-level doc structure should "emerge from the inside out" as pieces are improved — vanilla Diátaxis advice that conflicted with IDM's own prescriptive, user-journey-based TOC pattern described two sections later in the same skill (and in `docs_guidance/topic-types/toc.md`). That bullet is removed; the skill now points to the TOC pattern from the start instead of implying structure should emerge organically.
- **TOC grouping and cross-referencing are now treated as independent checks.** Grouping how-to/explanation topics into a subject-matter user guide is the preferred way to put related content side by side, but it's not always possible — reference, how-to, and explanation material for the same subject can legitimately live in separate top-level sections. `audit-docs-structure` and `audit-docs` now flag missing cross-links even when TOC placement is otherwise reasonable (e.g. a how-to and its related explanation that never link to each other, or a tutorial whose code examples don't link to the relevant API reference), instead of treating good TOC organization as evidence that cross-references exist.
- **`audit-personas` narrows what's expected of policy-maker/policy-influencer content.** These two personas are the lightest-touch in software documentation — at most one or two plain-language sentences of real-world policy relevance on the landing page or top of the README. The skill previously implied more was expected (track record, trust framing, real-world applications as a checklist); it now explicitly says not to recommend a dedicated section, case studies, or a landing-page reframe for these personas, since that content belongs in dashboards, briefs, or idmod.org rather than the docs site.


## Version 2.1 (2026.06.26)

- **`audit-docs` now ships its own Vale config, style rules, and doc templates.** Previously the Vale (grammar/style) and template-comparison passes couldn't run because the canonical `vale.ini`, `.github/styles/`, and `docs_templates/` lived at the repo root and aren't distributed with an installed plugin. They're now bundled under `skills/audit-docs/assets/` and reached via `$CLAUDE_PLUGIN_ROOT`. The grammar/style pass falls back to the bundled IDM config when the audited project has no Vale setup of its own, and the template audit diffs against the bundled mkdocs/quarto templates.
- The bundled assets are generated copies of the repo-root sources; the `update-docs-plugin` skill now re-syncs them whenever those sources change (new step 6b).

## Version 2.0 (2026.06.10)

- **Merged the three IDM plugins into one**: `idm-eng-plugin`, `idm-docs-plugin`, and `idm-uplifter-plugin` are now a single `idm-standards` plugin, so one install provides the full suite while every skill remains individually invocable.
- **Renamed all skills verb-first**: `eng-quality-checker` → `audit-code`, `eng-quality-fixer` → `fix-code`, `docs_audit` → `audit-docs`, `diataxis` → `audit-docs-structure`, `personas` → `audit-personas`, `python-docstrings` → `audit-docstrings`, `idm-code-uplifter` → `audit-code-exhaustive`.
- **Renamed output files to match**: `engineering_score.md` → `code_audit.md`, `uplifter_report.md` → `code_audit_exhaustive.md`, `.uplifter_cache/` → `.audit_cache/` (fixers fall back to reading `engineering_score.md` for compatibility).
- **New skills**: `audit-r-code` (R-specific engineering audit, invoked automatically for R projects), `audit-project` (runs code and/or docs audits with one set of questions), and `fix-project` (applies fixes from whichever audit reports exist).
- **Tier confirmation**: `audit-code` now infers a suggested tier from the codebase and asks the user to confirm it before scoring (an explicitly passed tier skips the prompt).
- **Strictness setting**: a second question alongside tier — strictness 1 (report everything, previous behavior) or 2 (only findings that materially affect usage; stylistic/convention findings are neither penalized nor reported).
- **Relaxed lockfile guidance**: Tier 1 (library) projects are never told to add a lock file; for Tier 2/3 the fixer asks the user to choose between `requirements_locked.txt` (simple), `pylock.toml` via `pip lock` (advanced), or none, and the choice is recorded so re-runs don't nag.
- **Score reconciliation across re-runs**: scorers still score fresh, but the skill now compares against the prior report and must justify any score decrease with concrete regression evidence or a specific previously-missed finding; unjustifiable drops retain the prior score. Justifications appear in a "Score changes since last run" report section.
- **Proposed solutions in the report**: recommendations that can't be automated get concrete proposed approaches, and the fixers record skipped/unfixable items (and user decisions) in a "Proposed solutions" section of the audit report.
- **Audit→fix chaining**: each audit ends by offering to run its fix counterpart immediately.
- Added an eval harness (`evals/` at the repo root) with fixture projects and round-trip checks (score must not decrease after fixes; implemented fixes must not be re-identified).
- **Docstring example convention**: docstring guidance and templates now use the plural, unbolded `Examples:` Google-style section header with a plain indented code block (no `**Example:**` bold heading, no inner ```` ```python ```` fence). The old bolded form was a Sphinx-only requirement that mkdocstrings/quartodoc do not parse as a section.
- **Version-control strategy in fixers**: `fix-code` and `fix-project` now ask up front how to manage version control for a run — one branch + PR for everything, a branch + PR per priority group (smaller, easier-to-review PRs), commit on the current branch with no PR, or edit-only with no git. `fix-project` asks once and passes the choice to `fix-code`.
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
