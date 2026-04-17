# IDM Standards

IDM's central hub for software quality standards, development practices, and tooling.

## Getting started

New to IDM? Start with the [getting started](getting_started/) guides:

- [Python setup](getting_started/python.md) -- setting up your development environment
- [AI tools](getting_started/ai.md) -- getting started with Claude Code and plugins
- [Communication](getting_started/comms.md) -- GitHub, Teams, meetings, and team culture

## Engineering guidance

The [engineering guidance](eng_guidance/) covers IDM's conventions for writing research software:

- [Philosophy](eng_guidance/1_philosophy.md) -- design principles and priorities
- [Python](eng_guidance/2_python.md) -- Python style conventions (Google style + IDM house rules)
- [Tests](eng_guidance/3_tests.md) -- testing practices for scientific code
- [Documentation](eng_guidance/4_documentation.md) -- standards for READMEs, docstrings, and tutorials
- [Other](eng_guidance/5_other.md) -- miscellaneous principles (e.g., data security)
- [Zen](eng_guidance/6_zen.md) -- short principles and credos
- [Engineering quality guidelines](eng_guidance/engineering_quality_guidelines.md) -- 10 metrics across 3 categories (quality, usability, safety) applied to 3 code tiers

## Documentation templates

The [docs templates](docs_templates/) provide starter templates for project documentation:

- [MkDocs template](docs_templates/mkdocs_template/) -- recommended for most projects
- [Quarto template](docs_templates/quarto_template/) -- for projects needing interactivity

## Claude Code plugins

This repo includes two Claude Code plugins for automating quality checks:

- **[IDM Engineering Plugin](idm_eng_plugin/)** (v1.2) -- scores and improves code against the [engineering quality guidelines](eng_guidance/engineering_quality_guidelines.md). Use `/idm-eng-plugin:eng-quality-checker` to score a project and `/idm-eng-plugin:eng-quality-fixer` to auto-fix issues.
- **[IDM Docs Plugin](idm_docs_plugin/)** (v0.0) -- checks documentation against IDM standards (work in progress).

Install via the Claude Code marketplace (configured in [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json)).
