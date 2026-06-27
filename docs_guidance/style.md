# Style and grammar

IDM style and grammar standards are defined using the Vale linter. We follow most Microsoft Manual of Style standards with some specific standards defined for IDM and our audience. Follow the instructions below to install and run Vale to apply these standards locally.

If desired, you can configure a GitHub action to run Vale on all pull requests in a repository. For more information, see https://github.com/vale-cli/vale-action.

## Vale linter usage

**Save IDM standards locally**

1. Clone the [idm_standards](https://github.com/InstituteforDiseaseModeling/idm_standards) repository.

**Install Vale**

1. Download the appropriate [Vale release](https://github.com/vale-cli/vale/releases) for your operating system.
2. Extract the files and save to your Program Files.

**Run in VSCode**

1. Open the VS Code Marketplace or use the Extensions view (Ctrl+Shift+X).
2. Search for and install "Vale VSCode" by Chris Chinchilla.
3. Under **File > Preferences > Settings > Extensions > Vale** set **Vale CLI:Config** to your path to idm_standards/idm_standards_plugin/skills/audit-docs/assets/vale.ini.
4. Add the path to the vale.exe in Program Files to your global VSCode settings.json.
5. Restart VSCode after installation.
6. Open any supported file type (.qmd, .md, and .ipynb) and Vale will automatically highlight issues with wavy lines in the editor.

**Run at the command line:**

1. Set the environment variables for `VALE_CONFIG_PATH` and `VALE_STYLES_PATH` to the `vale.ini` and `styles` paths under `idm_standards_plugin/skills/audit-docs/assets/` in the idm_standards repo.
2. Navigate to the location where you saved the vale.exe.
3. Run `vale ls-vars` to verify that the styles and configuration paths are correct.
4. Run `vale my_file.md` to inspect individual files and generate a report. See full CLI options at [vale.sh](https://vale.sh/docs/cli).

## Style guidance

We generally follow the [Microsoft Manual of Style (MSTP)](https://docs.microsoft.com/en-us/style-guide/welcome/) in our documentation. This topic summarizes some notable rules in MSTP, and notes where we diverge from their guidance.

### MSTP

A few of the most notable rules to be aware of are listed below.

**Overview**

*  Use American English spelling and punctuation.
*  Use the Oxford comma (serial comma).
*  Use sentence case for topic titles and headings (capitalize only the first word and proper nouns).
*  Verb tense and voice
   *  In general, use present tense and active voice.
   *  Use primarily second-person imperative. For example, "create a configuration" or "run a simulation."
   *  Use first-person (I or we) sparingly. For example, "We recommend…" is more natural
      than "It is recommended that."
*  Be direct and use simple sentence structure.
   *  Avoid jargon.
   *  Don't use i.e. or e.g. as they can cause problems for non-native English speakers or machine translation.

**Procedures**

Procedure guidelines are extensive (see chapter 6.) The primary points to follow are:

*  Sentences must provide the context and then the action. For example, "In the **Print**
   dialog box, click **All**."
*  Each step must encompass a single action, unless they are short and occur in the same place.
*  Additionally, you "click", you don't "click on."
*  Use imperative mood. In other words, verbs should take the form of commands. For example, "Enter your password" not "The user enters their password."
*  Separate UI elements with **>** and not **,**. For example, "Select **Explore > Experiments**".

### Differences from MSTP

Our house style guide differs from MSTP guidance in the following ways.

**Parameters**

*  Use bold, not italics, for parameter names.
*  Parameter values, which are often in all-caps, are in plain text.

**Placeholder text**

*  Surround placeholder text with angle brackets.
*  For example, text where users are expected to enter their username `C:/Users/<username>`.

**Titles and headings**

*  For procedural content, MSTP generally recommends imperative mood but says there's a lot of variation across groups.
* For tutorials, we use imperative mood; for example, "Run a simulation" not "Running a simulation." The one exception is "Getting started" for the first tutorial.
* For how-tos, we lead with "how to;" For example, "How to run a simulation."

**Species names**

*  Italicize species names. For example, *A. funestus* and *A. gambiae*.
*  A note on mosquito names: for scientific naming convention, the first time you mention a species you give its full name (*Anopheles funestus*), and
   then the second time you can abbreviate the genus (*A. funestus*). However,
   there are two "A" mosquito genera that are commonly discussed in the disease
   literature (*Aedes* and *Anopheles*), so it's convention to use the first
   two letters of the genus name when abbreviating: *An. funestus* and *Ae.
   aegypti*. For other organisms, you'll just use
   the first letter and not the first two.
