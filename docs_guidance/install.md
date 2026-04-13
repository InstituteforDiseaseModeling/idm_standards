# Installation/Get started

Depending on the structure of the rest of the content, you may want to include either an "Installation" topic or a "Get started" topic. Generally, if there is a single "Get started" tutorial or if installation is a complex process, use a separate "Installation" topic. These topics should follow the guidelines for a [How-to topic](topic-types/howto.md). 

If installation is a simple process, such as a `pip` install, and there is a recommended path for getting started with a project or package  we recommend including the installation instructions as part of the Home page. 

**MkDocs syntax:**

MkDocs content tabs can be a neat way to present different instructions for different operating systems or Python installations. For example:

=== "Python"

    ```
    python -m venv <env-name>
    ```
=== "Anaconda"

    ```
    conda create -n <env-name>
    ```

## Tutorials

For a "Get started" topic, it's good practice to link to one or more of the beginning tutorials.