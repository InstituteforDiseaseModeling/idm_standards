# Claude plugins

This repo publishes the **IDM-Standards** Claude Code plugin, which applies IDM's engineering and documentation standards. Install it from the IDM marketplace at [github.com/InstituteforDiseaseModeling/idm_standards](https://github.com/InstituteforDiseaseModeling/idm_standards).

> **Note:** as of v2.0 the three former plugins (`idm-eng-plugin`, `idm-docs-plugin`, `idm-uplifter-plugin`) are merged into one plugin, [`idm_standards_plugin`](idm_standards_plugin/README.md), and the skills were renamed verb-first. Uninstall the old three and install `idm-standards`.

## Skills

[`idm_standards_plugin`](idm_standards_plugin/README.md) scores and improves code against the [IDM Software Engineering Quality Guidelines](eng_guidance/engineering_quality_guidelines.md) and documentation against the [IDM documentation standards](docs_guidance/index.md). One install provides all skills; each is also individually invocable.

**Code**

- **audit-code** — scores a project and writes `code_audit.md` with prioritized recommendations (routes to **audit-r-code** for R projects).
- **fix-code** — implements the recommendations from that report.
- **audit-code-exhaustive** — fan-out per-file review across the whole project plus a repo-level review, aggregated into `code_audit_exhaustive.md` (incremental re-runs via `.audit_cache/`).

**Docs**

- **audit-docs** — full documentation audit (`docs_audit.md`); composes the three skills below.
- **audit-diataxis** — reviews structure against the four Diátaxis topic types.
- **audit-personas** — checks each section is pitched at the right IDM persona.
- **audit-docstrings** — checks Google-style docstrings for completeness.

**Combined**

- **audit-project** — runs code and/or docs audits with a single set of questions, summarized in `project_audit.md`.
- **fix-project** — applies fixes from whichever audit reports exist.
