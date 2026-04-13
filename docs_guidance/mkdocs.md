# MkDocs templates and guidance

For MkDocs, the mkdocs.yml file controls most aspects of the documentation build, style, table of contents, and plug-in functionality. The minimal files under customization/ are needed to meet GF requirements and should not require frequent updates. Avoid adding any other CSS or Javascript customization as it makes the doc build fragile and difficult to maintain consistency. For more information, see the [MkDocs documentation](https://squidfunk.github.io/mkdocs-material/reference/).

## Doc builds and previews

You should build or preview the documentation locally before submitting documentation changes. 

### Install required packages

1. Install MkDocs and associated packages:
    ```
    pip install -r docs/requirements.txt
    ```
### Preview the docs in a browser

1. Run a local server with:
   ```
   mkdocs serve --watch .
   ```
   
    The `watch` option will rebuild on changes outside the docs/ folder, such as docstring changes. 

2. Open a browser window at http://127.0.0.1:8000/<project>. This will rebuild to reflect changes each time a source file is updated and saved. 

### Build the docs 

1.  Build the documents:
    ```
    mkdocs build
    ```
2.  The built documents will be in `site/`.
