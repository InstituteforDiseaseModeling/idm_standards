# idm_uplifter_plugin

Runs a fan-out code review across the files in a project plus a repo-level review, and aggregates the findings into a single markdown report with a summary at the top.

## What it does

Given a project, the `idm-code-uplifter` skill:

1. Asks whether to review **all** source files or a **user-supplied list**.
2. Confirms the resolved file count.
3. Dispatches the `idm-code-reviewer` subagent in batched parallel waves (default wave size: 8) plus the `idm-repo-reviewer` subagent for project-level concerns, all in parallel.
4. Streams each completed block to a partial report so a re-run can resume rather than redo work.
5. Synthesizes a top-of-report summary (CRITICALs, severity counts, recurring criteria) and writes the final `uplifter_report.md` at the project root.

All agents are restricted to the target project directory; they do not read files elsewhere on disk.

## Components

- `skills/idm-code-uplifter/SKILL.md` — orchestrator skill.
- `agents/idm-code-reviewer.md` — per-file reviewer agent. The `files:` review checklist is inlined in the agent.
- `agents/idm-repo-reviewer.md` — repo-level reviewer agent. The `repo:` checklist is inlined in the agent.

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
- Per-file size cap (default 200 KB / 5000 lines — larger files are skipped and noted in the failures section)
