# IDM-Standards plugin

A Claude Code plugin that audits and improves scientific research code and documentation against the [IDM Software Engineering Quality Guidelines](https://institutefordiseasemodeling.github.io/idm_standards) and [IDM documentation standards](https://institutefordiseasemodeling.github.io/idm_standards). One install provides the full suite; every skill can also be invoked individually.

> **Migrating from the old plugins?** This plugin replaces the former `idm-eng-plugin`, `idm-docs-plugin`, and `idm-uplifter-plugin` (as of v2.0). Uninstall those and install `idm-standards` instead. Skill names changed too — see the table below. As of v3.0, `audit-code-exhaustive` is replaced by `audit-code` at max effort.

## Skills

| Skill | What it does | Replaces |
| --- | --- | --- |
| `audit-code` | Scores a project across 10 metrics (quality, usability, safety), and writes `code_audit.md` with findings and prioritized recommendations. Options: max effort (every source file read in full by parallel subagents) and run code (run the tests and README example) | `eng-quality-checker`, `idm-code-uplifter` |
| `audit-r-code` | The same audit, specialized for R projects (renv, testthat, Tidyverse style); invoked automatically when the project is R | *(new)* |
| `fix-code` | Reads `code_audit.md` and implements the recommendations | `eng-quality-fixer` |
| `audit-docs` | Comprehensive documentation audit, producing `docs_audit.md` | `docs_audit` |
| `audit-project` | Runs code and/or docs audits with a single set of questions, summarized in `project_audit.md` | *(new)* |
| `fix-project` | Applies fixes from whichever audit reports exist | *(new)* |
| `audit-docs-structure` | Reviews docs structure against the four topic types (tutorials, how-tos, reference, explanation) and IDM's TOC organization | `diataxis` |
| `audit-personas` | Checks each docs section is pitched at the right IDM persona | `personas` |
| `audit-docstrings` | Guidelines for writing and reviewing Google-style Python docstrings | `python-docstrings` |

## Quality tiers

| Tier | Description | Example |
|------|-------------|---------|
| 1 | Software library / digital public good | FPsim, LASER |
| 2 | Small-scale project | A model calibrated to one country |
| 3 | One-off / exploratory | A script to plot simulation outputs |

The audits ask you to confirm the tier (suggesting one based on the codebase), along with a **strictness** level: 1 = report everything; 2 = only findings that materially affect usage (stylistic/convention findings are neither penalized nor reported).

## Scoring metrics (`audit-code` / `audit-r-code`)

| Category (weight) | Metric | Within-category weight |
|---|---|---|
| **Quality (40%)** | Correct | 70% |
| | Clear | 20% |
| | Concise | 10% |
| **Usability (40%)** | Simple | 30% |
| | Powerful | 20% |
| | Performant | 20% |
| | Documented | 20% |
| | Accessible | 10% |
| **Safety (20%)** | Compliant | 60% |
| | Reproducible | 40% |

**Failure conditions**: `quality.correct` and `safety.compliant` can trigger a FAIL (score=0) if serious violations are found (e.g., scientific bugs, exposed secrets).

## Usage

### Audit a project

```text
/idm-standards:audit-code                                  # audit current directory (confirms tier/strictness)
/idm-standards:audit-code . 3                              # audit current directory at tier 3
/idm-standards:audit-code /path/to/repo 1                  # audit a local path at tier 1
/idm-standards:audit-code https://github.com/org/repo 2    # audit a GitHub repo
/idm-standards:audit-code . 2 2                            # tier 2, strictness 2 (material findings only)
/idm-standards:audit-code . 1 1 max                        # tier 1, max effort: every source file read in full
/idm-standards:audit-code . 2 1 run                        # tier 2, also run the tests and README example
```

Output: `code_audit.md` written to the project directory. R projects are automatically routed to `audit-r-code`. Each audit ends by offering to apply the fixes immediately.

How it works: three scorer agents (quality, usability, safety) look for **findings**: specific problems with a location and a fix. Scores are derived from the findings, and the report lists them all, so every score can be traced to evidence. By default the audit only reads the code (**inspect only**); with **run code** (the `run` argument, or the option in the audit's questions) it first runs the project's tests and README example and gives the scorers the results. Running code is off by default because it can have side effects.

- **Standard effort** (default): the scorers read the important files (README, tests, entry points, core scientific code) in full and report how many source files they read.
- **Max effort**: before scoring, the project's source files are split into batches and parallel file-reviewer agents read every line of every file. Much slower and more expensive; use it for a release, a handover, or a model about to inform a decision.

### Fix a project

```text
/idm-standards:fix-code                                    # fix current directory
/idm-standards:fix-code /path/to/repo                      # fix a specific path
```

Requires `code_audit.md` to exist (run `audit-code` first; reports named `engineering_score.md` from the 1.x plugins also work). Skipped or unfixable items are recorded — with concrete proposed solutions — in a "Proposed solutions" section of the report.

### Audit code and docs together

```text
/idm-standards:audit-project                               # asks: eng audit, docs audit, or both?
/idm-standards:fix-project                                 # applies fixes from whichever reports exist
```

### Docs-only skills

```text
/idm-standards:audit-docs                                  # full docs audit → docs_audit.md
/idm-standards:audit-docs-structure                        # docs structure (topic types + TOC)
/idm-standards:audit-personas                              # audience fit
/idm-standards:audit-docstrings                            # Python docstring review
```

## Configuring recommendations

Tell the audits which recommendations to make and which to skip by committing **`.claude/idm-standards.md`** to your repo, with plain-English directives (there are no rule IDs to learn):

```markdown
---
tier: 2
strictness: 1
---
# IDM Standards configuration
- Don't recommend renaming classes to CamelCase — lowercase (sim, people) is house style.
- Never recommend adding type hints; we don't use them.
- `import *` from sciris and starsim is our convention; don't flag it.
- Lock artifact: none — we opted out. Do not re-recommend.
- Ignore everything under scratch/ and examples/legacy/.
```

How it works:

- **One location.** `.claude/idm-standards.md` at the project (or git repo) root. Commit it so everyone's audits behave the same.
- **Suppressed, not hidden.** A directive means a finding is neither penalized, recommended, nor fixed. Every report lists what was suppressed (in a **Suppressed by config** section), so nothing is dropped silently.
- **Hard floor.** A directive can **never** waive a critical finding: exposed secrets, committed PII, license violations, or bugs that make scientific results wrong are always scored and reported.
- **Frontmatter defaults.** Optional `tier`/`strictness` frontmatter pre-fills the audit's questions (an explicit argument still wins).

The full spec lives in [`reference/user-config.md`](reference/user-config.md).

## IDM personas

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

## Updating (for internal use only)

- Code-audit skills derive from the [engineering quality guidelines](../eng_guidance/engineering_quality_guidelines.md); see `admin/update_prompt.md`.
- Docs skills derive from the `docs_guidance/` folder; use the internal skill `/update-docs-plugin`.
- The eval harness in `evals/` (repo root) checks skill behavior end-to-end; see `evals/README.md`.
- Shared definitions live in `reference/`: `criteria.yaml` (the checklist, mirroring the guidelines one-to-one), `findings.md` (finding format, severity, strictness), and `user-config.md` (the config file and the hard floor). The agents read these at run time, so a guidelines change is usually an edit to `criteria.yaml` or a scoring schema, not to the agents.
- `skills/audit-docs-structure/references` and `skills/audit-personas/personas` are symlinks into `docs_guidance/`; plugin installation copies the linked files, so they stay in sync automatically.
