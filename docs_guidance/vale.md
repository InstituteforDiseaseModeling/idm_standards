# Style and grammar

IDM style and grammar standards are defined using the Vale linter. We follow most Microsoft Manual of Style standards with some specific standards defined for IDM and our audience. Follow the instructions below to install and run Vale to apply these standards locally. 

If desired, you can configure a GitHub action to run Vale on all pull requests in a repository. For more information, see https://github.com/vale-cli/vale-action. 

**Save IDM standards locally**

1. Clone the [idm_standards](https://github.com/InstituteforDiseaseModeling/idm_standards) repository. 

**Install Vale**

1. Download the appropriate [Vale release](https://github.com/vale-cli/vale/releases) for your operating system.
2. Extract the files and save to your Program Files.

**Run in VSCode**

1. Open the VS Code Marketplace or use the Extensions view (Ctrl+Shift+X).
2. Search for and install "Vale VSCode" by Chris Chinchilla.
3. Under **File > Preferences > Settings > Extensions > Vale** set **Vale CLI:Config** to your path to idm_standards/vale.ini.
4. Add the path to the vale.exe in Program Files to your global VSCode settings.json.
5. Restart VSCode after installation. 
6. Open any supported file type (.qmd, .md, and .ipynb) and Vale will automatically highlight issues with wavy lines in the editor.

**Run at the command line:**

1. Set the environment variables for `VALE_CONFIG_PATH` and `VALE_STYLES_PATH` to vale.ini and .github/styles in the idm_standards repo.
2. Navigate to the location where you saved the vale.exe.
3. Run `vale ls-vars` to verify that the styles and configuration paths are correct.
4. Run `vale my_file.md` to inspect individual files and generate a report. See full CLI options at [vale.sh](https://vale.sh/docs/cli).
