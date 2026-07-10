# How to migrate from Sphinx

In the past, IDM used [Sphinx](https://www.sphinx-doc.org/en/master/) to build documentation that was hosted on Read the Docs. Sphinx is no longer supported for actively maintained software and hosting has moved to GitHub Pages. To migrate existing documentation from Sphinx to MkDocs or Quarto, follow the guidance below:

## Migrate from Sphinx

1. Prompt an AI agent to migrate the doc project and provide it with either the [MkDocs template](https://github.com/InstituteforDiseaseModeling/idm_standards/tree/main/idm_standards_plugin/skills/audit-docs/assets/docs_templates/mkdocs_template) or [Quarto template](https://github.com/InstituteforDiseaseModeling/idm_standards/tree/main/idm_standards_plugin/skills/audit-docs/assets/docs_templates/quarto_template), as appropriate.
1. Attempt to build the migrated content locally and troubleshoot any issues you identify.
1. Review the HTML output to identify any styling issues that pass build validation but look incorrect.
1. Remove all Sphinx files and references that are no longer needed, such as:
    - References in .gitignore
    - References in the README or repo settings
    - Links using the docs.idmod.org/projects/\<package>/en/latest Read the Docs URL pattern
    - GitHub Action files
    - The .readthedocs.yml configuration file
1. Check for common migration issues described below.

## Common issues with migration

As implied by the steps above, both MkDocs and Quarto builds may succeed without detecting incorrect formatting, such as a numbered list incorrectly rendered as a paragraph. These are the most common issues seen after AI-assisted migration from Sphinx.

## Markdown files

These are the issues most likely to be seen in Markdown files.

**Numbered lists**

In Sphinx, you can use `#.` for every item in a numbered list, and the list will be automatically renumbered during the documentation build. Quarto and MkDocs have similar renumbering functionality, but the syntax used is `1.` for every item.

**Notes and warnings**

To draw attention to notes or warnings, use syntax that renders them in callout/admonition boxes.

In Sphinx, the syntax is as follows:

```rst
.. warning::

    My warning text.

.. note::

    My user note.
```

In Quarto, the syntax is as follows:

```md
::: {.callout-note}
User note that there are five types of callouts, including:
`note`, `warning`, `important`, `tip`, and `caution`.
:::
```

In MkDocs, the syntax is as follows:

```md
!!! note:

    My user note.

!!! warning: Optional custom title

    My warning text.
```

**Anchor links**

It can often be helpful to link to figures, sections, and other items in the docs. In Sphinx, linkable labels required anchors to be added before individual items using the following syntax:

```rst
.. _my-reference-label:

Section to cross-reference
--------------------------

This is the text of the section.

To link to this section, see :ref:`my-reference-label`.
```

In Quarto and MkDocs, the templates add anchors to every section heading by slugifying the heading text. Anchors for figures and other elements need to be added to the source individually.

In Quarto, the syntax to add an anchor and then cross-reference it is as follows:

```md
## Introduction {#sec-introduction}

@sec-introduction
```
In MkDocs, the syntax to add an anchor and then cross-reference it is as follows:

```md
## Hello, world!

## Another heading

Link to [Hello, World!](#hello-world) on the same page.

Link to [Hello, World!](../index.md#hello-world) on the parent page.
```

**Code samples**

In Sphinx, you introduce code samples with either a double colon `::` for Python samples, or the code directive `.. code-block:: <language>`.

In MkDocs and Quarto, use fenced code samples with the following syntax:

````rst
```python
code sample
```
````
### Docstrings in Python files

In general, docstrings are parsed differently than RST or MD files and have specific formatting requirements. Therefore, many migration issues occur in docstrings. Both Quarto and MkDocs use the [Griffe parser](https://mkdocstrings.github.io/griffe/guide/users/how-to/parse-docstrings/).

**Links to Python objects**

In Sphinx, you link to Python objects using the syntax `` :class:`package.module.ClassName` `` or `` :func:`package.module.function` ``. You can prepend the package name with a tilde (~) to show only the class or function name.

In Quarto, you link to Python objects using the syntax `` [](`package.module.ClassName`) ``. If you want to display only the class or function name, include the desired link text in the square brackets.

In MkDocs, you link to Python objects using the syntax `` [package.module.ClassName][] `` If you want to display only the class or function name, use the syntax `` [`ClassName`][package.module.ClassName] ``. Note that the path is inside the first set of square brackets for the auto-populated link text and inside the second set of square brackets for the custom link text.

**Code examples**

Headings for code examples are not recognized as a section keyword by Sphinx, so our template indicated to use the syntax `**Example**` or `**Examples**` to make the section heading bold. If immediately followed by a code block follow by two colons `::`.

In both Quarto and MkDocs, `Examples:` is recognized as as section keyword, but not the singular `Example:`. Note that these should be followed with only a single colon.

The code or explanatory text that follows should be indented.

Only precede the code samples with `>>>` if you have implemented [doctest](https://docs.python.org/3/library/doctest.html). Otherwise, use fenced code blocks as follows:

````python
Examples:
    ```python
    code sample
    ```
````

