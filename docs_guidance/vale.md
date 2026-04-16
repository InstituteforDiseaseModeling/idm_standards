# Style and grammar

Style and grammar standards are defined and applied using the Vale linter. We follow most Microsoft Manual of Style standards with some specific standards defined for IDM and our audience. Follow the instructions below to install and run Vale.

**In VSCode:**

1. Open the VS Code Marketplace or use the Extensions view (Ctrl+Shift+X).
2. Search for and install "Vale VSCode" by Chris Chinchilla.
3. Restart VS Code after installation. 
4. If not already present in your repo, copy the Vale styles (.github/styles) and configuration file (vale.ini) from the https://github.com/InstituteforDiseaseModeling/idm_standards/ into your repo, maintaining the location.
5. If you store the files in a different location, you may need to update the location under **File > Preferences > Settings**.
6. Open any supported file type (.qmd, .md, and .ipynb) and Vale will automatically hightlight issues with wavy lines in the editor.

**At the command line:**

1. Install the Vale binary using your preferred package manager (https://vale.sh/docs/install).
2. If not already present in your repo, copy the Vale styles (.github/styles) and configuration file (vale.ini) from the https://github.com/InstituteforDiseaseModeling/idm_standards/ into your repo, maintaining the location. DO NOT run `vale sync` because this will overwrite the customized IDM settings.
3. Run `vale ls-vars` to verify that the styles and config paths are correct.
4. Run `vale my_file.md` to inspect individual files and generate a report. See full CLI options at https://vale.sh/docs/cli. 
