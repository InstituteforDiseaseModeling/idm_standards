# IDM documentation guidance

This section describes the standards for writing IDM documentation. You may build documentation using either Material for MkDocs (recommended) or Quarto (if greater R support or interactivity needed).

Use the template files in coordination with this documentation or the AI-driven plugins. Style guidance for terminology, grammar, and formatting is defined and enforced via the Vale linter.

You should build or preview the documentation locally before submitting documentation changes.

## Hosting

Under .github/ there are GH-Actions files for running a test doc build when PRs are opened and pushing changes to GH-Pages when PRs are merged. Note that private repositories can host documentation via GH-Pages, but the hosted docs will be publicly available unless the GitHub organization has an Enterprise account. IDM LT is aware of this limitation and approves of hosting docs for private repositories on GH-Pages but not publicizing the docs more broadly until the repo is public.

Projects within the starsimhub, laser-base, EMOD-hub, or InstituteforDiseaseModeling GitHub organizations will automatically have GH-Pages projects hosted at the following custom subdomains:

* starsim.idmod.org/project
* laser.idmod.org/project
* emod.idmod.org/project
* docs.idmod.org/project

Contact the content team when you are ready to share the docs more broadly by listing the project on the landing page for each of those subdomains. For more information on custom subdomains, see [GitHub Docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).

If desired, teams may set up a tool site separate from the idmod.org subdomain (such as [starsim.org](https://starsim.org/)), but must configure redirects for users who try to access the site from one of the subdomains above.
