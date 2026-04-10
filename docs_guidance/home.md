# Home topic

Include an introductory paragraph describing broadly what the project or package is and what the intended usage is. Don't forget to include the broader context about how it fits into disease modeling tools.

It's generally a good practice to automatically reuse the README.md file for the repo in your documentation home page. 

**MkDocs syntax:**

```
{%
    include-markdown "../README.md"
%}
```

**Quarto syntax:**

```
{{< include ../README.md >}}
```

## README guidance

In the package README, include the following:

A summary of the repo with enough context to guide model/tool selection relative to other similar tools. Although primarily for model builders/extenders/users, remember to ground the repo in potential policy/research applications. 

### Requirements

Software/hardware requirements.

### Installation

Installation instructions.

### Documentation and usage

Provide a link to the hosted documentation at https://docs.idmod.org/project or relevant modeling framework subdomain. If desired, include brief instructions on running a demo or simple simulation. 

### Package structure

An overview of the core model code, classes, and submodules. 

### Contributing

Any instructions on how to provide code contributions or reach out for support.

### Disclaimer

The code in this repository was developed by <IDM to support our research on flexible agent-based modeling>. We've made it publicly available under the MIT License to provide others with a better understanding of our research and an opportunity to build upon it for their own work. We make no representations that the code works as intended or that we will provide support, address issues that are found, or accept pull requests. You are welcome to create your own fork and modify the code to suit your own modeling needs as permitted under the MIT License.

## Learn more 

After reusing the README.md file, you can append additional content to orient the reader to the documentation.

**MkDocs syntax:**

One visually appealing way to present the high-level sections of the documentation is to include [grid cards](https://squidfunk.github.io/mkdocs-material/reference/grids/). There are many different icons available and the cards can be combined with other MkDocs formatting, such as content tabs, code blocks, or lists. This is an illustrative example; you may add or remove grid cards to best meet the needs of your documentation set. 

```html
<div class="grid cards" markdown>

-   :simple-jupyter:{ .lg .middle } __Tutorials__

    ---

    An interactive tour of key features.

    [:octicons-arrow-right-24: Tutorials](tutorials/index.md)

-   :material-api:{ .lg .middle } __Reference__

    ---

    Full details on all classes and functions. Update the path with the package name.

    [:octicons-arrow-right-24: API reference](autoapi/package/index.md)

-   :material-new-box:{ .lg .middle } __What's new__

    ---

    See what's in the latest releases.

    [:octicons-arrow-right-24: What's new](whatsnew.md)

</div>
```

