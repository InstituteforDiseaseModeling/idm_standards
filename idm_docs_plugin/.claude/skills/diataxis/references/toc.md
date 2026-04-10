# Table of contents reference

## Overview

The table of contents (TOC) controls the structure and labeling of the documentation site navigation. This reference covers shared principles that apply to all projects, followed by tool-specific implementation guidance for MkDocs with Material theme and Quarto.

## Shared principles

### Section ordering

Order top-level sections to match the user's journey through the documentation:

- Home
- Software overview (explanation)
  - Installation (how-to)
  - Architecture overview (reference)
  - Feature A (explanation)
    - How to implement (how-to)
  - Feature B (explanation)
    - How to implement (how-to)
- Explanation/concepts (explanation)
  - How to implement a concept (how-to)
- Tutorials (tutorial)
- Reference/API reference (reference)
- Standard pages

Not every project needs all sections, omit any that don't apply. How-to guides for a particular feature always appear as subsections under a relevant parent section, never as a standalone top-level section. Explanation of concepts appear before tutorials so users have conceptual grounding before hands-on practice.

### Naming conventions

- Use sentence case for nav display labels: `Get started`, `API reference`, `How-to guides`
- Use lowercase, hyphenated folder and file names: `get-started/`, `how-to-guides/`
- Be concise, one to three words per label where possible
- Match folder names to nav labels where possible: `tutorials/` → `Tutorials:`

### Hierarchy rules

- Maximum three levels of nesting is recommended
- Use subsections only when a section contains enough pages to warrant grouping
- A subsection with only one page should be a flat page instead:

```
# Avoid — unnecessary nesting
- Calibration:
  - Examples:
    - One example page   ← flatten this

# Prefer
- Calibration:
  - calibration/index or overview page
  - calibration/one-example-page
```

### Standard pages

Standard pages should appear at the end of the nav. "What's new" or changelog pages are optional and may not exist in all projects. Use these labels when the pages exist:

- `Code of conduct`
- `Contribution guide`
- `What's new` / `Changelog` / `Release notes` (optional, use whichever label the project already uses or prefers)

### Cross-references

Add cross-references when:
- A tutorial relies on concepts explained elsewhere → link to explanation
- A tutorial assumes setup covered in a how-to guide → link to how-to
- A how-to guide builds on concepts or skills introduced in a tutorial → link to tutorial
- A reference page relates to a how-to guide that shows it in use → link to how-to

**Placement:**
- Place cross-references at the bottom of a page under a `## See also` heading
- Use inline cross-references only when the link is essential to understanding the current sentence
- Do not front-load pages with cross-references — orient the reader first

### Jupyter notebooks

Tutorials written as Jupyter notebooks should be:
- Placed under a `Notebooks:` subsection within `Tutorials:` if there are non-notebook tutorials. Otherwise they should be within `Tutorials`.
- Given explicit human-readable labels in the nav — notebook filenames are often not readable on their own
- Prefixed with zero-padded numbers when sequence matters: `01_intro.ipynb`, `02_next.ipynb`
- Configured to execute during the documentation build so broken notebooks surface as build failures rather than silent errors (see tool-specific guidance below)

---

## MkDocs Material

The TOC is defined in `mkdocs.yml` under the `nav:` key.

### Index pages

Every section must point to an `index.md` as its first entry. The index serves as the section landing page:

```yaml
# Correct
- Tutorials:
  - tutorials/index.md
  - tutorials/sir.md

# Incorrect
- Tutorials:
  - tutorials/sir.md
```

### Notebook labels

Always provide explicit labels for notebooks in the nav:

```yaml
- Tutorials:
  - tutorials/index.md
  - Notebooks:
    - SI model with no demographics: tutorials/notebooks/01_SI_nobirths.ipynb
    - SI model with constant population: tutorials/notebooks/02_SI_wbirths.ipynb
```

### Notebook execution

Configure `mkdocs-jupyter` in `mkdocs.yml` to execute notebooks during the build:

```yaml
plugins:
  - mkdocs-jupyter:
      execute: true
      allow_errors: false
      include_source: true
```

`allow_errors: false` ensures a broken notebook fails the build rather than publishing silently broken output.

### Cross-references

Use the `autorefs` plugin (included in the standard `mkdocs.yml` template) to link by heading anchor:

```markdown
See [calibration process](calibration/process.md) for background before attempting this tutorial.
```

### Example nav structures

**Conceptual/explanation-heavy project:**

```yaml
nav:
  - Home: index.md
  - Get started:
    - get-started/index.md
    - Topic A:
      - get-started/topic-a/index.md
      - get-started/topic-a/subtopic.md
  - Models:
    - models/index.md
  - Calibration:
    - calibration/index.md
    - calibration/process.md
  - Code of conduct: code_of_conduct.md
  - Contribution guide: contribute.md
  - What's new: whatsnew.md
```

**Code/model-heavy project:**

```yaml
nav:
  - Home: index.md
  - Software overview:
    - software-overview/index.md
    - software-overview/architecture.md
  - Get started:
    - get-started/index.md
    - get-started/installation.md
  - Tutorials:
    - tutorials/index.md
    - tutorials/quickstart.md
    - Notebooks:
      - Tutorial one: tutorials/notebooks/01_tutorial.ipynb
      - Tutorial two: tutorials/notebooks/02_tutorial.ipynb
  - API reference: reference/
  - Code of conduct: code_of_conduct.md
  - Contribution guide: contribute.md
  - What's new: whatsnew.md
```

---

## Quarto

The TOC is defined in `_quarto.yml` under the `website.sidebar` or `website.navbar` key, depending on the layout chosen.

### Sidebar vs navbar

- Use `sidebar` for documentation-heavy projects with deep hierarchy (equivalent to MkDocs' default nav)
- Use `navbar` for simpler sites with few top-level sections
- Both can be combined: navbar for top-level sections, sidebar for within-section navigation

### Structure

Quarto uses `contents:` to define pages and sections within a sidebar:

```yaml
website:
  sidebar:
    contents:
      - index.qmd
      - section: Get started
        contents:
          - get-started/index.qmd
          - get-started/installation.qmd
      - section: Tutorials
        contents:
          - tutorials/index.qmd
          - tutorials/quickstart.qmd
```

### Index pages

Each section should have an `index.qmd` as its first entry, serving as the section landing page — the same principle as MkDocs.

### File conventions

- Use lowercase, hyphenated folder and file names: `get-started/`, `how-to-guides/`
- Quarto source files use `.qmd` extension; Jupyter notebooks use `.ipynb` and are supported natively

### Notebook execution

Configure notebook execution in `_quarto.yml`:

```yaml
execute:
  execute-notebooks: true
  error: false
```

Setting `error: false` fails the build on notebook errors, equivalent to `allow_errors: false` in MkDocs.

### Explicit labels

As with MkDocs, provide explicit labels for any page whose filename is not human-readable:

```yaml
- text: "SI model with no demographics"
  file: tutorials/notebooks/01_SI_nobirths.ipynb
```

### Cross-references

Quarto has built-in cross-reference support using `@` syntax for figures, tables, and sections:

```markdown
See @sec-calibration for background before attempting this tutorial.
```

Label a target section with:

```markdown
## Calibration {#sec-calibration}
```

For plain page links, use standard relative Markdown links:

```markdown
See [calibration process](../calibration/process.qmd) for background.
```

### Example structure

```yaml
website:
  sidebar:
    contents:
      - index.qmd
      - section: Software overview
        contents:
          - software-overview/index.qmd
          - software-overview/architecture.qmd
      - section: Tutorials
        contents:
          - tutorials/index.qmd
          - section: Notebooks
            contents:
              - text: "Tutorial one"
                file: tutorials/notebooks/01_tutorial.ipynb
              - text: "Tutorial two"
                file: tutorials/notebooks/02_tutorial.ipynb
      - section: API reference
        contents:
          - reference/index.qmd
      - code_of_conduct.qmd
      - contribute.qmd
```