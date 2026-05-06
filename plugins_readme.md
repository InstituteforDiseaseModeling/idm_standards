# Claude plugins

This repo publishes three Claude Code plugins that help apply IDM's engineering and documentation standards. Install any of them from the IDM marketplace at [github.com/InstituteforDiseaseModeling/idm_standards](https://github.com/InstituteforDiseaseModeling/idm_standards).

## Engineering plugin

[`idm_eng_plugin`](idm_eng_plugin/README.md) scores and improves code against the [IDM Software Engineering Quality Guidelines](eng_guidance/engineering_quality_guidelines.md), across quality, usability, and safety metrics.

- **eng-quality-checker** — scores a project and writes `engineering_score.md` with prioritized recommendations.
- **eng-quality-fixer** — implements the recommendations from that report.

## Docs plugin

[`idm_docs_plugin`](idm_docs_plugin/README.md) checks and improves documentation against the [IDM documentation standards](docs_guidance/index.md).

- **docs_audit** — runs the other three skills and produces a unified report.
- **diataxis** — reviews structure against the four Diátaxis topic types.
- **personas** — checks each section is pitched at the right IDM persona.
- **python-docstrings** — checks Google-style docstrings for completeness.

## Uplifter plugin

[`idm_uplifter_plugin`](idm_uplifter_plugin/README.md) runs a fan-out code review across an entire project. It dispatches a per-file reviewer agent in parallel waves and a repo-level reviewer agent concurrently, then aggregates the findings (with a top-of-report summary of CRITICALs, severity counts, and recurring issues) into `uplifter_report.md`. Re-runs are incremental via a `.uplifter_cache/` directory.

- **idm-code-uplifter** — orchestrates the run end-to-end (`/idm-uplifter-plugin:idm-code-uplifter`).
