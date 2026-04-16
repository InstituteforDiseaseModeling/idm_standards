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

## Installing plugins

Claude Code plugins give Claude specialized knowledge about specific frameworks and tools.

To install a plugin:

1. Type `/` to see the command menu (or click on the slash button)
2. Click on "Manage plugins"
3. Go to "Marketplaces"
4. Add the marketplace URL for the plugin you want to install
5. Select the plugin(s) you want from that marketplace
6. Go back to the list of plugins, find the plugin, and click "Install".
7. Restart VS Code.

Once installed, Claude Code will automatically use the plugin's skills when you're working on relevant projects.

## Cursor

AI support is built into Cursor; there isn't any additional setup.

You can [install plugins](https://cursor.com/docs/plugins) the same way in Cursor as Claude Code.
