# IDM-Docs-Plugin

A Claude Code plugin that checks and improves documentation against the [IDM documentation standards](https://institutefordiseasemodeling.github.io/idm_standards).

## Features

- **Docs Audit** (`/idm-docs-plugin:docs_audit`): Comprehensive documentation audit that checks completeness against IDM standards, then applies the diataxis, persona-check, and python-docstrings skills to produce a unified report with prioritized recommendations.
- **Diataxis** (`/idm-docs-plugin:diataxis`): Guides writing, reviewing, or improving documentation using the [Diataxis framework](https://diataxis.fr) (tutorials, how-to guides, reference, explanation).
- **Persona Check** (`/idm-docs-plugin:personas`): Checks that documentation is written appropriately for its target IDM personas (policy-maker, policy-influencer, model-user, model-extender, model-builder).
- **Python Docstrings** (`/idm-docs-plugin:python-docstrings`): Guidelines for writing Google-style Python docstrings consistent with IDM conventions and MkDocs/Quarto rendering.

## Usage

### Audit a project's documentation

```text
/idm-docs-plugin:docs_audit                    # audit current directory
/idm-docs-plugin:docs_audit /path/to/repo      # audit a specific path
```

Output: a unified report with strengths, weaknesses, and prioritized recommendations.

### Check documentation structure

```text
/idm-docs-plugin:diataxis                      # review docs in current directory
```

Applies the Diataxis framework to identify and fix structural issues (e.g., tutorials mixed with reference material).

### Check audience fit

```text
/idm-docs-plugin:personas                      # check persona alignment in current directory
```

Evaluates whether each documentation section is written for the right audience.

### Review Python docstrings

```text
/idm-docs-plugin:python-docstrings             # review docstrings in current directory
```

Checks Google-style formatting, completeness, and consistency with MkDocs/Quarto rendering.

## IDM Personas

| Persona | Description |
| --- | --- |
| Policy-maker | Needs high-level summaries and policy implications |
| Policy-influencer | Needs results, case studies, and model credibility |
| Model-user | Runs existing models; needs tutorials and user guides |
| Model-extender | Adapts models; needs API reference and how-to guides |
| Model-builder | Builds models from scratch; needs architecture docs |

## Installation

```bash
# From the IDM marketplace: https://github.com/InstituteforDiseaseModeling/idm_standards
# Add to .claude-plugin/marketplace.json or install via Claude Code settings
```

## Update

Use the internal skill `/update-docs-plugin` to update the `idm_docs_plugin` based on changes to the `docs_guidance` folder.
