---
pagetitle: "AI-assisted development"
---

# AI-assisted development

## Claude Code in VS Code

[Claude Code](https://docs.anthropic.com/en/docs/claude-code) is Anthropic's AI coding assistant that runs directly in your terminal and IDE. It can read your codebase, edit files, run commands, and help you build and debug software.

### Installation

1. If you don't have one already, sign up for an Anthropic account.
2. In VS Code, install the [Claude Code extension](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code) (see [installation details](https://code.claude.com/docs/en/vs-code))
3. Open the Claude Code panel (Ctrl+Shift+P, then "Claude Code: Open").
4. Follow the prompts to authenticate with your Anthropic account.

### Usage

- Open the Claude Code panel in VS Code and type your request in natural language.
- Claude Code can read and edit files, run terminal commands, search your codebase, and more.
- Use `/help` within Claude Code for a full list of commands.

## Installing the Starsim AI plugin

The [starsim-ai](https://github.com/starsimhub/starsim_ai) plugin gives Claude Code specialized knowledge about the Starsim framework -- including architecture, style conventions, and API patterns.

To install:

1. Type `/` to see the command menu (or click on the slash button)
2. Click on "Manage plugins"
3. Go to "Marketplaces"
4. Add <https://github.com/starsimhub/starsim_ai>
5. Select "Starsim-AI" (and any other plugins you want from that marketplace)
6. Go back to the list of plugins, find Starsim-AI, and click "Install".
7. Restart VS Code.

Once installed, Claude Code will automatically use the plugin's skills when you're working on Starsim projects. This includes guidance on:

- Simulation setup and configuration
- Disease models, networks, and interventions
- Calibration and analysis
- Starsim coding style and conventions

_Note:_ While Claude usually picks up the Starsim-AI plugin automatically, you can also ask to use it explicitly, e.g. "Use the Starsim-AI plugin to help me create tests for this project."

## Cursor

AI support is built into Cursor; there isn't any additional setup.

You can [install plugins](https://cursor.com/docs/plugins) the same way in Cursor as Claude Code.
