# IDM Standards

IDM's central hub for software quality standards, development practices, and tooling. This content is available as a [repo](https://github.com/InstituteforDiseaseModeling/idm_standards) and as [published docs](https://institutefordiseasemodeling.github.io/idm_standards).

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
- [Engineering quality guidelines](eng_guidance/engineering_quality_guidelines.md) -- principles for writing good code

## Documentation guidance

The [docs guidance](docs_guidance/) covers IDM's approach to documentation:

- [Style and grammar](docs_guidance/vale.md) -- style and grammar checking
- [MkDocs overview](docs_guidance/mkdocs.md) -- how to build docs with MkDocs
- [Quarto overview](docs_guidance/quarto.md) -- how to build docs with Quarto
- [Home page](docs_guidance/home.md) -- how to write a good home (landing) page
- [Installation page](docs_guidance/install.md) -- how to write a good installation page
- [Topic types](docs_guidance/topic-types/) -- how to structure your content as tutorials, explanations, how-to guides, etc.
- [Personas](docs_guidance/personas/) -- how to write for different audiences

## Claude Code plugins

This repo includes two Claude Code plugins for automating quality checks:

- **[IDM Engineering Plugin](idm_eng_plugin/)** (v1.2) -- scores and improves code against the [engineering quality guidelines](eng_guidance/engineering_quality_guidelines.md). Use `/idm-eng-plugin:eng-quality-checker` to score a project and `/idm-eng-plugin:eng-quality-fixer` to auto-fix issues.
- **[IDM Docs Plugin](idm_docs_plugin/)** (v1.0) -- checks and improves documentation against IDM standards. Use `/idm-docs-plugin:docs_audit` for a full audit, `/idm-docs-plugin:diataxis` for structure review, `/idm-docs-plugin:personas` for audience fit, and `/idm-docs-plugin:python-docstrings` for docstring quality.

Install via the Claude Code marketplace (configured in [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json)).