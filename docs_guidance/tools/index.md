# Doc tools

Build your docs site using either MkDocs or Quarto, using the templates provided in this repository. Both tools use Markdown as the source file format. Generally, we recommend using the same tool for all tools in a modeling ecosystem to make interlinking easier. A quick comparison of the two tools is below:

| Tool                                                         | Pros                                                         | Cons                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **[MkDocs](https://www.mkdocs.org/)** (with the [Material](https://squidfundamentals.com/mkdocs-material/) theme) | Easier to set up. Large user base and available plug-ins. Can include API reference documentation for external packages. | Less control over layout and rendering. MkDocs will not support Material going forward, so docs must be migrated to Zensical in the near future. |
| **[Quarto](https://quarto.org/)**                            | More flexibility and support for R packages and workflows. Easily produce research dashboards with interactive plotting. | Higher startup cost. Not a Python installation. Newer tool with smaller user base. |

In the past, IDM used [Sphinx](https://www.sphinx-doc.org/en/master/) to build documentation. Sphinx is no longer supported for actively maintained software. To migrate from Sphinx, review [How to migrate from Sphinx](sphinx.md).
