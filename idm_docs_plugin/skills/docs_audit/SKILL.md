---
name: docs-audit
description: Comprehensive documentation audit for IDM projects. Checks docs completeness against IDM standards (README, tutorials, user guide, API reference, changelog, etc.), then applies the diataxis, persona-check, and python-docstrings skills to evaluate structure, audience fit, and docstring quality. Produces a unified report with strengths, weaknesses, and prioritized recommendations. Use when reviewing, auditing, or scoring project documentation quality.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, Agent, Skill
---

# Documentation audit

Skill version: 1.0_2026.04.13

This skill performs a comprehensive documentation audit for an IDM project. It checks general completeness against the IDM documentation standards, then delegates to three specialized skills for deeper analysis, and assembles everything into a single prioritized report.

## Workflow

### Step 1: Identify the project and its documentation

Determine which project to audit. If the user specified a project, use that. Otherwise, use the current working directory.

Scan for documentation artifacts:

- `README.md` at the repo root
- `LICENSE` file
- `CHANGELOG.md`, `CHANGES.md`, or `WHATSNEW.md` (or equivalent)
- `CONTRIBUTING.md` or equivalent
- `CODE_OF_CONDUCT.md` or equivalent
- `docs/` folder (or equivalent documentation directory)
- `mkdocs.yml` or `_quarto.yml` (documentation build config)
- Folder-level `README.md` files in major directories
- Jupyter notebooks (`.ipynb`) or Quarto notebooks (`.qmd`) used as tutorials
- Python source files with docstrings

Record what exists and what is missing.

### Step 2: Check general completeness

Evaluate the project's documentation against the IDM documentation standards in `eng_guidance/4_documentation.md`. Check for:

**README.md contents:**
- What the package does (clear, concise description)
- Installation instructions (`pip install`, `uv add`, and local/dev install)
- Quick usage example (minimal "hello world" in under 10 lines)
- Project structure (one-line description of each submodule/folder)
- Links to full docs site, contributing guide, and issue tracker

**Required repo-level files:**
- LICENSE (MIT)
- Changelog / what's new
- Contributing guide
- Code of conduct

**Folder-level READMEs:**
- Check whether major directories have `README.md` files explaining their purpose

**Documentation site / docs folder:**
- Tutorials (at minimum: a hello-world tutorial and a slightly more advanced one)
- User guide (for complex projects where tutorials + API reference aren't enough)
- API reference (auto-generated from docstrings via quartodoc or mkdocstrings)
- Documentation build configuration (`mkdocs.yml` or `_quarto.yml`)

**API reference setup:**
- Interlinks configured for cross-references to standard libraries
- Auto-generation from docstrings (not hand-written API docs)

Score each item as: **Present** / **Partial** / **Missing** / **N/A**

### Step 3: Run specialized audits

Apply each of the three sub-skills by invoking them. For each, follow the skill's workflow against the project's documentation. You do not need to produce separate reports for each -- collect findings to merge into the final report.

#### 3a: Diataxis audit

Invoke the `diataxis` skill. Evaluate:
- Whether the four Diataxis documentation types are represented (tutorials, how-to guides, reference, explanation)
- Whether existing docs are correctly categorized (e.g., a "tutorial" that is actually a how-to guide)
- Whether there is cross-contamination between types (e.g., reference material embedded in tutorials)
- How well the table of contents / navigation organizes content by type

#### 3b: Persona audit

Invoke the `persona-check` skill. Evaluate:
- Whether documentation sections are written for their target personas
- Whether the landing page / top of README serves policy-maker and policy-influencer personas
- Whether tutorials serve model-user, model-extender, and model-builder personas
- Whether technical depth matches audience expectations
- Whether LMIC context is acknowledged where appropriate

#### 3c: Python docstrings audit

Invoke the `python-docstrings` skill. Sample a representative set of public modules, classes, and functions (at least 10-15 if the project is large enough) and evaluate:
- Whether public objects have docstrings
- Whether docstrings follow Google style
- Whether docstrings include: one-line summary, parameter descriptions, return values, usage examples
- Whether docstrings provide researcher workflow context
- Whether cross-references to related objects are present
- Overall docstring coverage (rough percentage of public objects with adequate docstrings)

### Step 4: Assemble the report

Produce a single structured report with these sections and write to `docs_audit.md`:

#### Documentation audit report

**1. Summary**

A 2-3 sentence overview of the project's documentation health. State clearly whether documentation is in good shape, has notable gaps, or needs significant work.

**2. Strengths**

Bullet list of what the documentation does well. Be specific -- cite actual docs, sections, or patterns that are effective. Only include genuine strengths; do not pad this section.

**3. Weaknesses**

Bullet list of significant gaps or issues, organized by severity. For each weakness:
- What the issue is
- Why it matters (which users are affected, what they can't do)
- Where in the docs the issue occurs (file/section reference)

**4. Recommendations**

A numbered list of concrete, actionable improvements, **ranked by importance**. Importance is determined by:

1. **Impact on users** -- how many personas are affected, how severely
2. **Effort to fix** -- quick wins rank higher than large rewrites (at equal impact)
3. **Standards compliance** -- items required by IDM standards rank higher than nice-to-haves

For each recommendation:
- What to do (specific and actionable)
- Why it matters (brief justification)
- Estimated effort: **Low** (< 1 hour), **Medium** (1-4 hours), **High** (> 4 hours)

**5. Completeness checklist**

A compact table summarizing the presence/absence of each expected documentation component:

```
| Component                  | Status  | Notes |
|----------------------------|---------|-------|
| README.md                  | ...     | ...   |
| LICENSE                    | ...     | ...   |
| Changelog                  | ...     | ...   |
| Contributing guide         | ...     | ...   |
| Code of conduct            | ...     | ...   |
| Folder-level READMEs       | ...     | ...   |
| Docs site config           | ...     | ...   |
| Hello-world tutorial       | ...     | ...   |
| Advanced tutorial(s)       | ...     | ...   |
| User guide                 | ...     | ...   |
| API reference              | ...     | ...   |
| Diataxis coverage          | ...     | ...   |
| Persona targeting          | ...     | ...   |
| Docstring quality          | ...     | ...   |
```

## Guidelines

- **Be concrete, not generic.** Cite specific files, sections, and examples. "The README lacks installation instructions" is useful; "documentation could be improved" is not.
- **Calibrate to the project's size and maturity.** A small utility package does not need a full user guide. A large modeling framework does. Judge what is appropriate and flag missing items accordingly.
- **Don't penalize for N/A items.** If a project has no Python code, skip the docstrings audit. If a project is a pure library with no policy audience, note that the persona audit is limited.
- **Acknowledge good work.** If documentation is genuinely well done in some area, say so clearly. The report should be balanced, not just a list of complaints.
- **Keep the report concise.** Aim for a report that can be read in 5-10 minutes. Use brief bullets, not paragraphs. The goal is actionable insight, not exhaustive analysis.
