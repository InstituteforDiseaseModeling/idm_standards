# Table of contents

The table of contents (TOC) controls the structure and labeling of the documentation site navigation. IDM guidance around organizing the table of contents diverges from [Diátaxis](https://diataxis.fr/). Our documentation is often complex and the researcher workflow is less predictable than the user workflow for most software products. The templates for MkDocs and Quarto provide a minimal table of contents that should provide a good starting place for most projects.

## Shared principles

This section covers shared principles that apply to all projects, followed by tool-specific implementation guidance for Material for MkDocs and Quarto.

### Align with the user journey

Whenever making decisions about documentation organization, aim to align structure with a typical user journey. In model documentation, users typically follow a path something like this:

1. Complete a "getting started" tutorial to gain confidence with the tool and understanding of the workflow. Many people prefer to "learn by doing" at a high level before digging into specific details.
2. Gain more understanding about a particular subject matter of interest (migration, data cleaning, calibration, etc.).
3. Complete a few more complex tutorials to gain a broader understanding of using the tool.
4. Switch from acquisition of knowledge to action, eventually getting stuck and needing to return to the docs. Usually readers consult how-to topics, troubleshooting, or reference to get unstuck. Lather, rinse, repeat.

Users actively look for tutorials and reference as a topic type, so these should be in top-level sections in the TOC. However, how-to topics and explanations work best when contained in user guides grouped by subject matter. For example, users may want to learn more about demographics in a model and would seek out a demographics user guide with both explanation and how-to topics related to that subject. 

**Example TOC**

- Home (overview)
- Installation (how-to)
- What's new (reference)
- Tutorials (tutorial)
  - Get started (tutorial)
  - Add demographics (tutorial)
  - Calibrate the model (tutorial)
- Software/model user guide (explanation)
  - Architecture overview (reference)
  - Feature A user guide (explanation)
    - How to implement... (how-to)
    - Troubleshooting (how-to)
  - Feature B user guide (explanation)
    - Subtopic of feature B (explanation)
    - How to implement... (how-to)
- Reference/API reference (reference)
- Code of conduct (reference)
- Contribution guide (how-to)

Not every project needs all sections; omit any that don't apply. Depending on the complexity of installation, you may include it in the home page or break it out into a separate topic. The explanation or reference for more complex functionality follows once users have that hands-on grounding in the workflow through the tutorials. 

You may decide to have a top-level section for the model/software user guide with features/themes nested beneath or put individual features/themes at the top level. How-to topics for a particular feature always appear as subsections under a relevant parent section, never as a standalone top-level section. 

Always let user needs drive your organizational decisions. For example, if model users and model extenders are primary personas but have different workflows, you may want to have two top-level user guide sections for "Use the model" and "Extend the model." 

### Reuse content

All repos should include CONTRIBUTING.md, CODE_OF_CONDUCT.md, CHANGELOG.md, and README.md files at the root. You can reuse these files in the built documentation so you don't need to maintain that content in two places. Use these labels:

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
{{{< include ../README.md >}}}
```

### Naming conventions

- Use sentence case for nav display labels: `Getting started`, `API reference`, `How to configure`
- Use lowercase, hyphenated folder and file names: `get-started/`, `how-to-guides/`
- Be concise, one to three words per label where possible
- Match folder names to nav labels where possible: `tutorials/` → `Tutorials:`

### Hierarchy depth

- We recommend a maximum of three levels of nesting
- Use subsections only when a section contains enough pages to warrant grouping
- A subsection with only one page should be a flat page instead:

```
# Avoid — unnecessary nesting
- Calibration:
  - Examples:
    - One example page  ← flatten this

# Prefer
- Calibration:
  - calibration/index or overview page
  - calibration/one-example-page
```

### Cross-references

Add cross-references when:

- A tutorial relies on concepts explained elsewhere → link to explanation
- A tutorial assumes setup covered in a how-to topic → link to how-to
- A how-to topic builds on concepts or skills introduced in a tutorial → link to tutorial
- A reference topic relates to a how-to guide that shows it in use → link to how-to

**Placement:**

- Use inline cross-references when the link is essential to understanding the current sentence
- Place more general cross-references at the bottom of a page under a **See also** heading
- Do not front-load pages with cross-references--orient the reader first

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

## Quarto

The TOC is defined in `_quarto.yml` in `contents` under the `website.sidebar` or `website.navbar` key, depending on the layout chosen.

- Use `sidebar` for documentation-heavy projects with deep hierarchy (equivalent to MkDocs default nav)
- Use `navbar` for simpler sites with few top-level sections
- Both can be combined: navbar for top-level sections, sidebar for within-section navigation

### Index pages

Each section should have an `index.qmd` as its first entry, serving as the section landing page--the same principle as MkDocs.

### Notebook labels

As with MkDocs, provide explicit labels for notebooks in contents:

```yaml
- text: "SI model with no demographics"
  file: tutorials/notebooks/01_SI_nobirths.ipynb
```