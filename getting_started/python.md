---
pagetitle: "Installing Python"
---

# Installing Python

This guide presents three options for getting up and running with Python. It assumes no prior knowledge of Python. If you have used Python before and know what setup you prefer, you are always welcome to use that.

Note: since this document assumes you have no prior Python experience, it does not discuss [virtual environments](https://code.visualstudio.com/docs/python/environments). These are useful (sometimes critical) for juggling multiple different Python projects. However, if you will primarily be working on one Python project at a time, or working on a set of projects that all have similar dependencies, you probably don't need them.


## Editor options

Before getting started, you need to install a Python environment and editor.

### Option 1: VS Code (recommended)

VS Code is by far the most commonly used editor among IDM team members due to its excellent Python and AI support.

1. Download and install [VS Code](https://code.visualstudio.com/).
2. Install the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python).
3. VS Code will prompt you to install Python if it's not already on your system. Alternatively, download Python from [python.org](https://www.python.org/downloads/).
4. From the terminal inside VS Code, install your project's dependencies: `pip install -r requirements.txt` (or similar).
5. Check that it worked: create a file called e.g. `demo.py` with a simple script, and then click on the play button at the top right of the editor.

More info: [VS Code Python tutorial](https://code.visualstudio.com/docs/python/python-tutorial)

### Option 2: Cursor

[Cursor](https://cursor.com/) is a popular AI-first editor that is based on (and intercompatible with) VS Code. The main difference is that Cursor uses its own system for managing AI agents. This system is often considerably faster than VS Code + Claude Code, but is often not as capable for large-scale tasks. You might want to try both Cursor and VS Code for a while and see which one you like better.

1. Download and install [Cursor](https://cursor.com/).
2. Follow the remaining steps above for VS Code.

### Option 3: Conda-forge + Spyder

If you are coming from an [RStudio](https://posit.co/download/rstudio-desktop/) background, Spyder might feel most familiar to you. Compared to VS Code, it's very basic (and lacks AI support), but it excels at quickly running scripts and working in the command line. Some people use VS Code for AI-heavy workflows, and then switch to Spyder for quick interactive development and debugging.

1. Install [Miniforge](https://conda-forge.org/download/). This will add the commands `python`, `conda`, and `pip` (among others) to your terminal.
2. From your terminal, install Spyder: `conda install spyder`
3. Install your project's dependencies: `pip install -r requirements.txt` (or similar).
4. Check that it worked: from the Spyder console, run a simple script to verify your setup. (Note: if you want your plots to appear as new windows rather than in the "Plots" pane, you can change this option under Tools → Preferences.)

More info: [Conda getting started](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html) | [Spyder docs](https://docs.spyder-ide.org/)

_Note:_ If you want to use both Spyder and VS Code, install Conda + Spyder first, then install VS Code. This ensures that VS Code uses the same Python installation as Spyder.

### Other options

- [Positron](https://positron.posit.co/) is a new Python and R editor from the makers of RStudio. It is somewhat like a hybrid between VS Code and Spyder.
- [PyCharm](https://www.jetbrains.com/pycharm/) is one of the most popular Python editors. It is extremely fully featured, including GitHub and AI integration. We don't recommend it here because it has a steeper learning curve than VS Code, and VS Code now has more or less the same features.
- Python files are just text files, so you can use a text editor like [Sublime](https://www.sublimetext.com/) and run directly from the command line (`python your_script.py`). This workflow is useful for power users who need to switch between files and projects quickly, but is less likely to be ideal for someone just getting started in Python.


## Package management: pip vs uv

The instructions above use `pip`, which is the standard Python package installer that comes bundled with Python. However, you may increasingly see projects provide instructions for using `uv` instead:
```bash
# Install uv (see https://docs.astral.sh/uv/)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Use it like pip
uv pip install somepackage
```

`uv` is much faster than `pip`, but if you're reading this guide, the difference is almost certainly going to be negligble to you since you are unlikely to be creating new Python environments multiple times a day. The two tools are interchangeable, so use whichever you prefer.
