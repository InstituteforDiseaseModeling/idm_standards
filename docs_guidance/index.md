# IDM documentation guidance

This section describes the standards for writing IDM documentation. You may built documentation using either Material for MkDocs (recommended) or Quarto (if greater R support or interactivity needed). 

Use the template files in coordination with this documentation or the AI-driven plugins. Style guidance for terminology, grammar, and formatting is defined and enforced via the Vale linter.

You should build or preview the documentation locally before submitting documentation changes. 

## Hosting

Under .github/ there are GH-Actions files for running a test doc build when PRs are opened and pushing changes to GH-Pages when PRs are merged. Note that private repositories can host documentation via GH-Pages, but the hosted docs will be publicly available unless the GitHub organization has an Enterprise account. IDM LT is aware of this limitation and approves of hosting docs for private repositories on GH-Pages but not publicizing the docs more broadly until the repo is public.

The default URL for GH-Pages is org.github.io/repo, but when documentation is ready to share broadly, you should set up a custom domain at one of the following subdomains:

* starsim.idmod.org/project
* laser.idmod.org/project
* emod.idmod.org/project
* docs.idmod.org/project 

For more information, see [GitHub Docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site). Coordinate with the research content team to add the CNAME record and set up a link on the docs landing pages and a tool page on [idmod.org ](https://www.idmod.org/tools/).
