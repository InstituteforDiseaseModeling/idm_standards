# Quarto templates and guidance

For Quarto, the `_quarto.yml` file controls most aspects of the documentation build, style, table of contents, and extension functionality. Avoid adding custom CSS or JavaScript as it makes the doc build fragile and difficult to maintain consistency.

Use the [Quarto template](https://github.com/InstituteforDiseaseModeling/idm_standards/tree/main/idm_standards_plugin/skills/audit-docs/assets/docs_templates/quarto_template) provided in this repository. For more information, see the [Quarto documentation](https://quarto.org/docs/guide/).

## Doc builds and previews

You should build or preview the documentation locally before submitting documentation changes.

### Install required packages

1. Install Quarto from [quarto.org/docs/get-started](https://quarto.org/docs/get-started/).

2. Install any required Python or R dependencies:
    ```
    pip install -r docs/requirements.txt
    ```

### Preview the docs in a browser

1. Run a local server with:
   ```
   quarto preview
   ```

   This will watch for changes and automatically rebuild.

2. A browser window will open automatically (typically at http://localhost:4200). The preview will rebuild to reflect changes each time a source file is updated and saved.

### Build the docs

1.  Build the documents:
    ```
    quarto render
    ```
2.  The built documents will be in `_site/` (for websites) or `_book/` (for books).
