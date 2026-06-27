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
- [R](eng_guidance/2b_r.md) -- R style and engineering practice (Tidyverse style + IDM expectations)
- [Tests](eng_guidance/3_tests.md) -- testing practices for scientific code
- [Documentation](eng_guidance/4_documentation.md) -- standards for READMEs, docstrings, and tutorials
- [Other](eng_guidance/5_other.md) -- miscellaneous principles (for example, data security)
- [Zen](eng_guidance/6_zen.md) -- short principles and credos
- [Engineering quality guidelines](eng_guidance/engineering_quality_guidelines.md) -- principles for writing good code

## Documentation guidance

The [docs guidance](docs_guidance/) covers IDM's approach to documentation:

- [Style and grammar](docs_guidance/style.md) -- style and grammar checking
- [MkDocs overview](docs_guidance/tools/mkdocs.md) -- how to build docs with MkDocs
- [Quarto overview](docs_guidance/tools/quarto.md) -- how to build docs with Quarto
- [Home page](docs_guidance/topic-types/home.md) -- how to write a good home (landing) page
- [Installation page](docs_guidance/topic-types/install.md) -- how to write a good installation page
- [Topic types](docs_guidance/topic-types/) -- how to structure your content as tutorials, explanations, how-to guides, etc.
- [Personas](docs_guidance/personas/) -- how to write for different audiences

## Claude Code plugin

This repo includes the **[IDM-Standards plugin](idm_standards_plugin/)** (v2.0) for automating quality checks against the [engineering quality guidelines](eng_guidance/engineering_quality_guidelines.md) and IDM documentation standards. Its skills:

- `/idm-standards:audit-code` -- score a project and write `code_audit.md` (routes to `audit-r-code` for R projects); `/idm-standards:fix-code` applies the recommendations.
- `/idm-standards:audit-docs` -- full documentation audit (`docs_audit.md`), composing `audit-docs-structure`, `audit-personas`, and `audit-docstrings`.
- `/idm-standards:audit-project` -- run code and/or docs audits with one set of questions; `/idm-standards:fix-project` applies fixes across both.
- `/idm-standards:audit-code-exhaustive` -- fan-out per-file review aggregated into `code_audit_exhaustive.md`.

> **Migrating from v1.x?** The former `idm-eng-plugin`, `idm-docs-plugin`, and `idm-uplifter-plugin` are now this single plugin, and the skills were renamed (for example, `eng-quality-checker` → `audit-code`). Uninstall the old three and install `idm-standards`.

Install via the Claude Code marketplace (configured in [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json)).

### Installation with Claude Code

To install, add this repo as a marketplace inside Claude Code using either of the methods below (it will be available in both places regardless of installation method). If you see a permissions error, you may need to enable Admin by Request.

**CLI**

1. Run `/plugin marketplace add https://github.com/InstituteforDiseaseModeling/idm_standards`.
2. Run `/plugin`, from the **Discover** tab, install any of the plugins.

**VSCode extension**

1. In the Claude Code chat window, type `/plugin` in the Claude Code chat and select **Manage plugins > Marketplaces**.
2. Enter `https://github.com/InstituteforDiseaseModeling/idm_standards` and click **Add**.
3. In **Plugins** select the plugins you want and click **Install**.

### Installation with other LLMs

Although these plugins were built for Claude Code, they will work with any LLM via [OpenSkills](https://github.com/numman-ali/openskills).
