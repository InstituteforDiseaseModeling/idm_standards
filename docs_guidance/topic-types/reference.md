# Reference topic

The purpose of a reference topic is to describe the technical nuts and bolts of a package or project: the API, classes, functions, interface, etc. The content is oriented towards information, not action or understanding. For additional information on how to structure reference, see [Diataxis](https://diataxis.fr/reference/) or the Diataxis skills included in the docs plugin. 

## Python

Both Material for MkDocs and Quarto can automatically create API reference topics from Python docstrings. The templates provide the configuration for achieving this.

### Docstring format

Include a description of the module, including its purpose and functionality. We use Google style docstrings. Most common text editors and IDEs can be configured to automatically create stubbed out docstrings in the Google format.

To refer to other Python objects, such as methods or classes, in the docstring
you can create a link using the following syntax, where the first part is the link text to be displayed and the second part is the Python object to link to, including the module name `[Arr][starsim.Arr]`. There is a simple example of a function definition and docstring below:

```
def example_function(param1, param2):       
    """
    Include a description of what the function does, including enough context to understand how it fits into a broader research workflow. For example, if there are similar functions that are recommended for use in conjunction with this one, those should be mentioned as well. Note that this docstring is in Google style format. Including 

    Args:
        param1 (int): The first number.
        param2 (int): The second number.

    Returns:
        int: The sum of the two numbers.

    Examples:
        Include an introduction to help readers understand more complex usage
        examples. Including the right angle brackets in the examples will include
        the example for testing via doctest, which is useful for ensuring that the
        examples are correct and that the code behaves as expected.
        >>> example_function(2, 3)
        5
        >>> example_function(-1, 1)
        0
    """
    return param1 + param2
```
For more information, see the following resources, listed in order of relevance:

* [Google style docstring examples](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html)
* [PEP 257 docstring conventions](https://www.python.org/dev/peps/pep-0257/)
* [PEP 484 annotation](https://www.python.org/dev/peps/pep-0484/)
* [Google style guide on docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) (Note that we do not follow Google's guidance to use descriptive instead of imperative verbs, choosing to follow the PEP 257 guidance instead.)
* [Python 3 documentation](https://docs.python.org/3/)
  
## R

The [roxygen2](https://roxygen2.r-lib.org/articles/roxygen2.html) package automatically produces API reference documentation from R comments. Roxygen2 generates .Rd files in the man/ directory of documentation written in RStudio. You can also use `knitr` to convert Rmarkdown files to Markdown so they can be integrated into a MkDocs project.

You can use [pkgdown](https://pkgdown.r-lib.org/), MkDocs, or Quarto to build those files into HTML documentation. While `pkgdown` is often the default tool used for R packages, we recommend MkDocs or Quarto for consistency across IDM documentation.

### MkDocs

You can use then convert the R package documentation from .Rd to .md for integration into MkDocs using `rdmarkdown` and `rdconvert`. Follow the rest of the guidance here about using MkDocs for writing, building, and hosting documentation. We recommend this over the previous workflow to write all documentation in RStudio both for consistency across documentation projects and the limitations of the content structure in RStudio.
