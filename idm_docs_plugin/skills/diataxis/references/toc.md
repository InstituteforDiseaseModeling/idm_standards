# Table of contents reference

## Overview

The table of contents (TOC) controls the structure and labeling of the documentation site navigation. This guidance covers shared principles that apply to all projects, followed by tool-specific implementation guidance for Material for MkDocs and Quarto.

Follow the Diataxis guidance when deciding what what topic type to use for information you want to share in the documentation. All topics should aim to be self-contained and describe a single subject, linking away to related topics but not duplicating their content. When content must appear in multiple topics (such as common warnings), create a snippet of reusable text rather than duplicating that content. 

## Shared principles

### Section ordering

Order top-level sections to match the new user's journey through the documentation. For example, a typical TOC might look like:

- Home (overview)
- Installation (how-to)
- What's new (reference)
- Tutorials (tutorial)
  - Get started (tutorial)
  - Add demographics (tutorial)
  - Calibrate the model (tutorial)
- Software/model overview (explanation)
  - Architecture overview (reference)
  - Feature A (explanation)
    - How to implement... (how-to)
  - Feature B (explanation)
    - How to implement... (how-to)
- Reference/API reference (reference)
- Code of conduct (reference)
- Contribution guide (how-to)

Not every project needs all sections; omit any that don't apply. Depending on the complexity of installation, you may include it in the home page or break it out into a separate topic. Place tutorials early because new users often learn better by doing and they provide a quick entry point to increase user retention and confidence. 

The explanation or reference for more complex functionality follows once they have that hands-on grounding in the workflow. You may decide to have a top-level section for the model/software overview with features/themes nested beneath or put individual features/themes at the top level. How-to guides for a particular feature always appear as subsections under a relevant parent section, never as a standalone top-level section. 

Always let user needs drive your organizational decisions. For example, if model users and model extenders are primary personas but have different workflows, you may want to have two top-level sections for "Use the model" and "Extend the model." 

### Naming conventions

- Use sentence case for nav display labels: `Get started`, `API reference`, `How to configure`
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

### Reused content

All repos should include CONTRIBUTING.md, CODE_OF_CONDUCT.md, CHANGELOG.md, and README.md files at the root. These files can be pulled into the built documentation so you don't need to maintain that content in two places. Use these labels:

- `Contribution guide` / `Contributing`
- `Code of conduct`
- `What's new` / `Changelog` / `Release notes` (optional, use whichever label the project already uses or prefers)
- `Home` / `Model name` (reuse README.md if it makes sense to)

**MkDocs syntax:**

```
{%
    include-markdown "../README.md"
%}
```

**Quarto syntax:**

```
{{< include ../README.md >}}
```

### Cross-references

Add cross-references when:
- A tutorial relies on concepts explained elsewhere → link to explanation
- A tutorial assumes setup covered in a how-to guide → link to how-to
- A how-to guide builds on concepts or skills introduced in a tutorial → link to tutorial
- A reference page relates to a how-to guide that shows it in use → link to how-to

**Placement:**
- Use inline cross-references when the link is essential to understanding the current sentence
- Place more general cross-references at the bottom of a page under a `## See also` heading
- Do not front-load pages with cross-references — orient the reader first

**MkDocs syntax:**

For simple page links, use standard relative Markdown links:

```markdown
See [calibration process](../calibration/process.md) for background.
```

Use the `autorefs` plugin (included in the standard `mkdocs.yml` template) to link by heading anchor, as shown below

```markdown
This works the same as [Heading text](../calibration/process.md#heading-text).
```

**Quarto syntax:**

For simple page links, use standard relative Markdown links:

```markdown
See [calibration process](../calibration/process.qmd) for background.
```

Quarto has built-in cross-reference support using `@` syntax for figures, tables, and sections:

```markdown
See @sec-calibration for additional background information.
```

Label a target section with:

```markdown
## Calibration {#sec-calibration}
```

### Jupyter notebooks

Tutorials written as Jupyter notebooks should be:
- Placed under a `Notebooks:` subsection within `Tutorials:` if there are non-notebook tutorials. Otherwise they should be within `Tutorials`.
- Given explicit human-readable labels in the nav — notebook filenames are often not readable on their own.
- Prefixed with zero-padded numbers when sequence matters: `01_intro.ipynb`, `02_next.ipynb`.
- Configured to execute during the documentation build so broken notebooks surface as build failures rather than silent errors (see tool-specific guidance below).

---

## Material for MkDocs

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

### Example nav structures

**Conceptual/explanation-heavy project:**

```yaml
nav:
  - Home: index.md
  - What's new: whatsnew.md
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
```

**Code/model-heavy project:**

```yaml
nav:
  - Home: index.md
  - What's new: whatsnew.md
  - Get started:
    - get-started/index.md
    - get-started/installation.md
  - Tutorials:
    - tutorials/index.md
    - tutorials/quickstart.md
    - Notebooks:
      - Tutorial one: tutorials/notebooks/01_tutorial.ipynb
      - Tutorial two: tutorials/notebooks/02_tutorial.ipynb
  - Software overview:
    - software-overview/index.md
    - software-overview/architecture.md
  - API reference: reference/
  - Code of conduct: code_of_conduct.md
  - Contribution guide: contribute.md
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

### Explicit labels

As with MkDocs, provide explicit labels for any page whose filename is not human-readable:

```yaml
- text: "SI model with no demographics"
  file: tutorials/notebooks/01_SI_nobirths.ipynb
```

### Example structure

```yaml
website:
  sidebar:
    contents:
      - index.qmd
      - section: Tutorials
        contents:
          - tutorials/index.qmd
          - section: Notebooks
            contents:
              - text: "Get started"
                file: tutorials/notebooks/01_get_started_tutorial.ipynb
              - text: "Add demographics"
                file: tutorials/notebooks/02_demographics_tutorial.ipynb
      - section: Software overview
        contents:
          - software-overview/index.qmd
          - software-overview/architecture.qmd
      - section: API reference
        contents:
          - reference/index.qmd
      - code_of_conduct.qmd
      - contribute.qmd
```