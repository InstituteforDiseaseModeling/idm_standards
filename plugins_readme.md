# Claude plugins

This repo publishes two Claude Code plugins that help apply IDM's engineering and documentation standards. Install either from the IDM marketplace at [github.com/InstituteforDiseaseModeling/idm_standards](https://github.com/InstituteforDiseaseModeling/idm_standards).

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
