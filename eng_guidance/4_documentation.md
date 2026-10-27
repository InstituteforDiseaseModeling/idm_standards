# Documentation in code

People are probably (...hopefully!) going to be spending much more time reading the docs you write than reading the code you write. So make them good! Good docs make the difference between a tool that people adopt versus one they try out but quickly abandon. And just because LLMs are now reading your docs too, that isn't an excuse to be lazy and write something a human would find frustrating to wade through. Good docs should be succinct but comprehensive -- a devilish tradeoff to say the least!

For more information on stylistic standards, audience, supported doc tools, tutorials, and structuring your documentation, see the [docs guidance](../docs_guidance/index.md). This topic will focus on the repo READMEs and docstrings, documentation that lives directly in Python files and is rendered into API reference content. If migrating existing documentation from Sphinx, see [migrate from Sphinx](../docs_guidance/tools/sphinx.md) for some formatting gotchas.

## READMEs

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

### Folder-level readmes

Every folder in the repo should have a `README.md` file -- even if it's just one or two sentences. It should explain why the folder exists, what it contains, and/or how its contents are organized. Someone browsing the repo on GitHub should never have to guess what a folder is for. The exception to this is if the folder structure is explained fully in the top-level README.

## API reference

The API reference should be **auto-generated from docstrings** -- use [quartodoc](https://machow.github.io/quartodoc/) (for Quarto) or [mkdocstrings](https://mkdocstrings.github.io/) (for MkDocs). Both templates in this repository include the config settings for these plugins. If using MkDocs, all local modules are automatically included in the TOC; if using Quarto, modules must be listed in the _quarto.yml config file.

Expectations for docstrings:

- Every public module, class, and function should have a docstring.
- Use [Google-style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) docstrings.
- Docstrings should include at least: a one-line summary, a description of parameters and return values, and ideally **one usage example**.
- Provide clear, precise descriptions to avoid ambiguity in ranges, units, paths, assumptions, etc. that can introduce silent scientific errors.
- Configure interlinks so that cross-references to standard libraries (Python, NumPy, Pandas, Sciris, etc.) resolve automatically.
- Provide enough context to help a disease-modeling researcher understand not just *what* the object does, but *where it fits* in their workflow. Link to related topics as appropriate.
- Use American English spelling and usage.

### Type hints

If type hints are included in the function or class signature, do not include them in the docstring itself--the parser will pull that information from the signature. Including them in both places can result in inconsistent documentation. If type hints are not in the signature or would result in a convoluted type in the rendered documentation, you may include them in the docstring. The example below includes them in the docstring because IDM generally avoids type hints.

### Structure of a good docstring

```python
def some_function(arg1, arg2):
    """ One-line summary ending with a period.

    Two to four sentences of prose explaining what this does and why a researcher
    would reach for it. Say where it fits in their workflow: is it used when
    setting up a model, at each timestep, or when analyzing results?

    Link to related objects using cross-reference syntax (see below), for
    example the main simulation class that this function operates on.

    Args:
        arg1 (array): Description including shape, dtype, and units where
            relevant. For example, "Daily new infections, shape ``(n_days,)``."
        arg2 (int): Description. State default values explicitly if they matter.

    Returns:
        array: What is returned, its shape, dtype, and interpretation.
            For None returns, omit this section entirely.

    Raises:
        ValueError: When and why this is raised.

    Examples:

        # Show the most common researcher workflow, as a self-contained
        # snippet that a researcher can run or adapt directly
        sim = Sim(pars)
        sim.run()
        result = some_function(sim.results.new_infections, sim.pars.n_days)

    Note:
        Reserve for non-obvious caveats — performance warnings, thread safety,
        or behaviors that diverge from what the name implies.
    """
```

Use the plural, unbolded `Examples:` section header. It must be a plain Google-style section header (not `**Example:**`) so that mkdocstrings/quartodoc parse it as a section — the bolded form was a Sphinx-only requirement and is not recognized by the MkDocs/Quarto toolchain. The example code is just an indented block under the header; do not wrap it in a ```` ```python ```` fence (an indented block is already rendered as code). Put any explanation in code comments, as above.

### Cross-references to other Python objects

#### MkDocs syntax

MkDocs projects use the [`autorefs`](https://mkdocstrings.github.io/autorefs/) plugin so you can link to any documented Python object directly from docstring prose, using its full import path:

| What you write | What renders |
|---|---|
| `` [`Sim`][mypackage.sim.Sim] `` | clickable link labeled `Sim` |
| `` [`Sim.run`][mypackage.sim.Sim.run] `` | link to the `run` method |
| `` [`numpy.ndarray`][] `` | link to an external object (via interlinks) |

Use these links in the **description prose** to guide a reader toward related objects they will likely need next: the main class this object belongs to, components that must come before or after it, and the functions that consume its output. Do not stuff links into Args or Returns sections — prose is the right place.

#### Quarto syntax

Cross-references typically work directly, e.g. `ss.Arr` automatically links to `starsim.arrays.Arr`. If you need to customize, use the syntax: [Arr](`starsim.arrays.Arr`).

### Researcher workflow context

Researchers using a modeling library follow a typical workflow, for example:

```
1. Define parameters    →  population size, duration, disease parameters, random seed
2. Build the model      →  choose its components (diseases, networks, interventions, ...)
3. Run the simulation   →  sim.run()
4. Analyze results      →  plot, summarize, compare scenarios
```

The stages differ between libraries: take them from the project's own README and tutorials, and use the project's own names for things. The docstring should anchor the object to one of these stages. In the description prose, state clearly:

- **Which stage** this object belongs to (setup, per-timestep, post-run analysis)
- **What comes before it**, if ordering matters
- **What it produces** that downstream components or analysis code will consume

Example phrasing:

> "Add this intervention to the sim's `interventions` list. It runs each timestep after transmission, and records the doses given in `sim.results.vaccine.doses`."

### Usage examples

Every public class and every non-trivial function needs an `Examples:` section. A good example:

1. **Shows the full calling context**, not just the function call in isolation.
2. **Uses realistic variable names** that match the project's tutorials (e.g. `sim`, `pars`, `results`).
3. **Demonstrates the most common researcher use case** — not edge cases.
4. **Is short** — three to eight lines. If you need more, split into two examples.
5. **Runs**: it uses the current API and would work if pasted into a session.

**Class example:**

```python
Examples:

    # Create a simple SIR model and run it
    sim = Sim(diseases=SIR(beta=0.3), networks=RandomNet(n_contacts=4))
    sim.run()
    sim.results.sir.prevalence  # one value per timestep
```

**Function example:**

```python
Examples:

    # Compute gravity-weighted migration rates between patches
    rates = gravity(populations, distances, k=1.0, a=1.0, b=2.0)
    migration = row_normalize(rates)
```

### Class docstrings

For classes, the docstring lives on the class body (not `__init__`), with `merge_init_into_class: true` set in `mkdocs.yml`. Structure it as:

```
One-line summary.

Two to four sentences of context: what part of the model this represents,
which stage of the researcher workflow it belongs to, and what it produces.
Link to closely related classes.

Args:
    pars (dict): Parameters to override the defaults, e.g. ``dict(beta=0.3)``.
    dur_inf (float): Mean duration of infection, in days. Defaults to 10.
    validate (bool): If True, checks the state of each agent every timestep.
        Enable during development; disable for production runs.

Examples:

    ...

Note:
    ...
```

Do not repeat the class name in the one-line summary. Write "Manages the susceptible compartment" not "Susceptible manages the susceptible compartment."

### What to omit

- **Do not document private methods** (`_update_cache`, `_check_inputs`, etc.) unless there is a strong reason.
- **Do not add a docstring to `__init__`** — put everything on the class.
- **Do not restate the type annotation** in the description ("arg1 is a numpy array" when the type is already `np.ndarray`). Use the prose to explain *meaning*, not *type*.
- **Do not write "This function/class ..."** — just say what it does directly.
- **Do not add a `Returns:` section for `None`**.
