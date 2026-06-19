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
- Configure interlinks so that cross-references to standard libraries (Python, NumPy, Pandas, Sciris, etc.) resolve automatically.
- Provide enough context to help a disease-modeling researcher understand not just *what* the object does, but *where it fits* in their workflow. Link to related topics as appropriate.
- Use American English spelling and usage.

### Type hints

If type hints are included in the function or class signature, do not include them in the docstring itself--the
parser will pull that information from the signature. Including them in both places can result in inconsistent documentation. If type hints are not in the signature or would result in a convoluted type in the rendered documentation, you may include them in the docstring. The example below include them in the docstring because IDM generally avoids type hints.

### Structure of a good docstring

```python
def some_function(arg1, arg2):
    """ One-line summary ending with a period.

    Two to four sentences of prose explaining what this does and why a researcher
    would reach for it. Mention the disease model context — is this used during
    initialization, timestep updates, or post-simulation analysis?

    Link to related objects using MkDocs cross-reference syntax, for example,
    [`Model`][laser.generic.model.Model] or [`Susceptible`][laser.generic.components.Susceptible].

    Args:
        arg1 (array): Description including shape, dtype, and units where
            relevant. For example, "Shape ``(nticks+1, num_nodes)``, dtype float32."
        arg2 (int): Description. State default values explicitly if they matter.

    Returns:
        array: What is returned, its shape, dtype, and interpretation.
            For None returns, omit this section entirely.

    Raises:
        ValueError: When and why this is raised.

    Examples:

        # Show the most common researcher workflow. Use a self-contained snippet
        # that a researcher can run or adapt directly:

        model = Model(scenario, params)
        result = some_function(model.nodes.S[0], model.params.nticks)


    Note:
        Reserve for non-obvious caveats — performance warnings, thread safety,
        or behaviors that diverge from what the name implies.
    """
```

Use the plural, unbolded `Examples:` section header. It must be a plain Google-style
section header (not `**Example:**`) so that mkdocstrings/quartodoc parse it as a section —
the bolded form was a Sphinx-only requirement and is not recognized by the MkDocs/Quarto toolchain.
The example code is just an indented block under the header; do not wrap it in a ```` ```python ````
fence (an indented block is already rendered as code).

---

### Cross-references to other Python objects

#### MkDocs syntax

MkDocs projects use the [`autorefs`](https://mkdocstrings.github.io/autorefs/) plugin so you can link to any documented Python object directly from docstring prose.

**Syntax:**

| What you write | What renders |
|---|---|
| `` [`Model`][laser.generic.model.Model] `` | clickable link labelled `Model` |
| `` [`Susceptible`][laser.generic.components.Susceptible] `` | link to the Susceptible class |
| `` [`State`][laser.generic.shared.State] `` | link to the State enum |
| `` [`ValuesMap`][laser.generic.utils.ValuesMap] `` | link to ValuesMap |

Use these links in the **description prose** to guide a reader toward related components they will likely need next. Do not stuff links into Args or Returns sections — prose is the right place.

**Common objects to link to:**

- [`Model`][laser.generic.model.Model] — the top-level simulation container
- [`Susceptible`][laser.generic.components.Susceptible] — must appear before transmission components
- [`Exposed`][laser.generic.components.Exposed] — incubation period component for SEIR models
- [`State`][laser.generic.shared.State] — enum of agent health states (SUSCEPTIBLE, EXPOSED, INFECTIOUS, RECOVERED)
- [`ValuesMap`][laser.generic.utils.ValuesMap] — time-varying per-node parameter container

#### Quarto syntax

Cross-references typically work directly, e.g. `ss.Arr` automatically links to `starsim.arrays.Arr`. If you need to customize, use the syntax: [Arr](`starsim.arrays.Arr`).

---

### Researcher workflow context

A researcher using this library follows a predictable workflow. Your docstring should anchor the object to one of these stages:

```
1. Prepare scenario     →  GeoDataFrame with population, geometry, initial S/I/E/R counts
2. Set parameters       →  PropertySet with nticks, beta, capacity_safety_factor, prng_seed, ...
3. Build component list →  [Susceptible(model), Transmission(model, ...), ...]
4. Initialize model     →  model = Model(scenario, params)
5. Run simulation       →  model.run()
6. Analyze results      →  model.nodes.S, model.nodes.I, component.plot()
```

In the description prose, state clearly:
- **Which stage** this object belongs to (initialisation, per-timestep, post-run analysis)
- **What comes before it** in the component list, if ordering matters
- **What it produces** that downstream components or analysis code will consume

Example phrasing:
> "Add this component to `model.components` *before* any transmission component. It initialises the `S` array consumed by [`SIR.Transmission`][laser.generic.SIR.Transmission] at every timestep."

---

### Usage examples

Every public class and every non-trivial function needs an `Example:` section. A good example:

1. **Shows the full calling context**, not just the function call in isolation.
2. **Uses realistic variable names** (`scenario`, `params`, `model`) that match the tutorials.
3. **Demonstrates the most common researcher use case** — not edge cases.
4. **Is short** — three to eight lines. If you need more, split into two examples.

**Class example (component):**

```python
Example:
    Assemble a basic SIR model by listing components in execution order:

    ```python
    model.components = [
        Susceptible(model),
        SIR.Transmission(model, beta=0.3),
        SIR.Infectious(model, infdurdist, infdurmin=1),
        SIR.Recovered(model),
    ]
    model.run()
    model.nodes.S  # shape (nticks+1, num_nodes)
    ```
```

**Function example:**

```python
Example:
    Compute gravity-weighted migration rates between patches:

    ```python
    rates = gravity(populations, distances, k=1.0, a=1.0, b=2.0)
    migration_matrix = row_normalizer(rates)
    ```
```

---

### Class docstrings

For classes, the docstring lives on the class body (not `__init__`), because `merge_init_into_class: true` is set in `mkdocs.yml`. Structure it as:

```
One-line summary.

Two to four sentences of context: what disease model states this manages,
which stage of the researcher workflow it belongs to, and what it produces.
Link to closely related components.

Args:
    model (Model): The simulation model this component is attached to.
    some_dist (Callable): Brief description including expected signature.
    some_min (int): Minimum value in days. Defaults to 1.
    validating (bool): If True, runs pre/post validation hooks each tick.
        Enable during development; disable for production runs.

Example:
    ...

Note:
    ...
```

Do not repeat the class name in the one-line summary. Write "Manages the
susceptible compartment" not "Susceptible manages the susceptible compartment."

---

### What to omit

- **Do not document private methods** (`_check_flow_vs_census`, `nb_timer_update`, etc.) unless there is a strong reason.
- **Do not add a docstring to `__init__`** — put everything on the class.
- **Do not restate the type annotation** in the description ("arg1 is a numpy array" when the type is already `np.ndarray`). Use the prose to explain *meaning*, not *type*.
- **Do not write "This function/class ..."** — just say what it does directly.
- **Do not add a `Returns:` section for `None`**.
