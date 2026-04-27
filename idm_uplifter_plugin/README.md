# idm_uplifter_plugin

Runs a fan-out code review across many files in a project and aggregates per-file findings into a single markdown report.

## What it does

Given a project, the `idm-code-uplifter` skill:

1. Asks whether to review **all** source files or a **user-supplied list**.
2. Confirms the resolved file count.
3. Dispatches `idm-code-reviewer` subagents in batched parallel waves (default wave size: 8).
4. Collects each agent's structured markdown findings.
5. Writes `uplifter_report.md` at the project root.

## Components

- `skills/idm-code-uplifter/SKILL.md` — orchestrator skill.
- `agents/idm-code-reviewer.md` — per-file reviewer agent (the review criteria are a placeholder for the plugin owner to replace with a real checklist).

## Usage

Invoke the skill from Claude Code:

> "Run the uplifter on this repo."

or via the slash command form:

> `/idm-uplifter-plugin:idm-code-uplifter`

## Configuration

These defaults live in `skills/idm-code-uplifter/SKILL.md` and can be overridden at invocation time:

- Wave size (default `8`)
- File extensions to include (default `.py`, `.ipynb`, `.R`, `.md`, `.qmd`)
- Output report path (default `uplifter_report.md` at repo root)

## Status

This is the skeleton. The review criteria inside `agents/idm-code-reviewer.md` are intentionally generic — replace them with the actual checklist before relying on the plugin's output.
