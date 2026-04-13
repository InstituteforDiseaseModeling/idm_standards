# Tutorial topic

The purpose of a tutorial topic is to walk through a procedure or workflow with the goal of learning. It is a lesson primarily for illustrating generalizable principles rather than completing the specific task. Avoid digression that includes reference content or explanation content--link to those topics instead. This helps keep tutorials focused and makes maintenance of content easier. 

For additional information on how to structure tutorials, see [Diataxis](https://diataxis.fr/tutorials/) or the Diataxis skills included in the docs plugin. 

## Titles

Use imperative verbs for tutorial topics. For example, "Get Started," "Calibrate the Model," or "Configure a Vaccination Campaign." Avoid gerunds (-ing verbs) because they can be ambiguous, sometimes functioning as a verb, adjective, or noun. This can create confusion, especially in translation.

## Jupyter notebooks

When possible, we recommend using Jupyter notebooks for tutorial content. Notebooks can run both Python and R code. Notebooks are executed as part of the documentation build, so if the content becomes outdated, you will see an error. Tutorials can be some of the most challenging topic types to keep from becoming stale, so this integrated testing is very valuable. See the [example notebook](notebook.ipynb) tutorial for more info.

All packages needed to run the Jupyter notebook must be installed via requirements.txt.

### Notebook execution MkDocs

Configure `mkdocs-jupyter` in `mkdocs.yml` to execute notebooks during the build:

```yaml
plugins:
  - mkdocs-jupyter:
      execute: true
      allow_errors: false
      include_source: true
```

`allow_errors: false` ensures a broken notebook fails the build rather than publishing silently broken output.

### Notebook execution Quarto

Configure notebook execution in `_quarto.yml`:

```yaml
execute:
  execute-notebooks: true
  error: false
```

Setting `error: false` fails the build on notebook errors, equivalent to `allow_errors: false` in MkDocs.
