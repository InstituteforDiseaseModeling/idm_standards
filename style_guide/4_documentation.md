# IDM documentation style guide

People are probably (...hopefully!) going to be spending much more time reading the docs you write than reading the code you write. So make them good! Good docs make the difference between a tool that people adopt versus one they try out but quickly abandon. And just because LLMs are now reading your docs too, that isn't an excuse to be lazy and write something a human would find frustrating to wade through. Good docs should be succinct but comprehensive -- a devilish tradeoff to say the least!


## Audience

We identify five different "personas" as the audience for IDM (and IDM-related) tools:

| Name | Who they are | What they need |
| ---- | ------------ | -------------- |
| Model builder | People who design and implement new modeling frameworks and core methods | Detailed how-to guides and comprehensive API references that describe the full functionality, plus ways to extend the code |
| Model extender | People who adapt and calibrate existing models to new questions, countries, or datasets | Tutorials, how-to guides, and easy-to-understand API references with examples |
| Model user | People who run pre-built models or dashboards to answer concrete questions, without changing the underlying code | Simple tutorials and accessible how-to guides |
| Policy influencer | People who shape which evidence and models are used and how they are interpreted | Clear guidance about what this tool is useful for, accessible results (e.g. dashboards), and evidence that it's trustworthy |
| Policy maker | People who hold formal authority to set policy and allocate public resources | Clear, brief explanation of the tool's purpose and why it can be trusted |


## Documentation tools

Build your docs site using either:

- **[MkDocs](https://www.mkdocs.org/)** (with the [Material](https://squidfundamentals.com/mkdocs-material/) theme) -- slightly easier to set up, less control over layout and rendering.
- **[Quarto](https://quarto.org/)** -- slightly higher startup cost, but more flexibility.

Starsim itself uses Quarto, but most other projects use MkDocs. Either way, the docs should live in `docs/` and produce a static website. (Note: Please do not use Sphinx or rST unless you hate yourself and others.)


## Documentation contents

This section describes what your documentation should actually consist of. It is based on the [Diátaxis](https://diataxis.fr/) framework. Briefly, Diátaxis separates docs into four categories:

1. *Tutorials* are **learning-oriented, practical activity** where students learn by doing meaningful tasks toward achievable goals. They're lessons, not a task completion guide.
2. *How-to guides* are **goal-oriented directions** that help users accomplish specific tasks or solve real problems. They guide action through practical steps focused on what users want to achieve.
3. *Explanations* are **understanding-oriented** documentation that deepens reader comprehension through reflective, discursive treatment of topics. They answers: "Can you tell me about X?"
4. *Reference guides* provide **information-oriented** technical descriptions. They contain propositional/theoretical knowledge for users to consult during work, not to learn from sequentially.

### Readmes

The repo-level **README.md** is one of the most important entry points for the project. It should typically include:

- **What the package does** -- a clear, concise description.
- **Installation** -- `pip install`, `uv add`, and local/dev install instructions.
- **Quick usage example** -- a minimal "hello world" that runs in under 10 lines.
- **Project structure** -- a one-line description of each submodule/folder, so newcomers can orient themselves.
- **Links** -- to the full docs site, contributing guide, and issue tracker.

Repos should also include:

- **LICENSE** -- we use the MIT license.
- **What's new / changelog** -- release-by-release summary of changes.
- **Contributing** -- how to set up a dev environment, run tests, and submit PRs.
- **Code of conduct** -- how to not be a jerk (e.g, by writing rST files).

Except for the license, these should be standalone markdown files in the repo root.

#### Folder-level readmes

Every folder in the repo should have a `README.md` file -- even if it's just one or two sentences. It should explain why the folder exists, what it contains, and/or how its contents are organized. Someone browsing the repo on GitHub should never have to guess what a folder is for. The exception to this is if the folder structure is explained fully in the top-level README.

### API reference

The API reference should be **auto-generated from docstrings** -- use [quartodoc](https://machow.github.io/quartodoc/) (for Quarto) or [mkdocstrings](https://mkdocstrings.github.io/) (for MkDocs).

Expectations for docstrings:

- Every public module, class, and function should have a docstring.
- Use [Google-style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) docstrings.
- Docstrings should include at least: a one-line summary, a description of parameters and return values, and ideally **one usage example**.
- Configure interlinks so that cross-references to standard libraries (Python, NumPy, Pandas, Sciris, etc.) resolve automatically.

### Tutorials

Notebook-based tutorials are strongly encouraged even for small projects. At minimum, try to provide:

- A **"hello world" tutorial** -- the simplest possible working example, with explanation.
- A **slightly more advanced tutorial** -- demonstrating the core workflow end-to-end.

For larger projects, a progressive series of tutorials works well. Bonus points for including exercises/solutions.

*Note:* Historically, tutorials have been written as Jupyter notebooks for ease of sharing and execution. However, you may also use other formats, such as Quarto notebooks (`.qmd`), which are easier to edit by hand compared to Jupyter notebooks (which are encoded as a highly nested JSON file).

### User guide

For complex projects where tutorials + API reference aren't enough, add a **user guide** with deeper coverage of each topic. The user guide is explicitly framed as "more in-depth" than the corresponding tutorials.

A good structure progresses from concepts to practice:

1. **Introduction** -- what the package is, how models/workflows are structured.
2. **Basics** -- the core objects and how they fit together.
3. **Modules/Components** -- detailed coverage of each major subsystem.
4. **Workflows** -- common end-to-end tasks (running, calibrating, deploying).
5. **Advanced topics** -- performance, edge cases, internals.

Like tutorials, user guide pages should be Jupyter (or Quarto) notebooks with executable examples.
