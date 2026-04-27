# idm_optimizer_plugin — Design

**Date:** 2026-04-27
**Status:** Approved for implementation

## Purpose

A new Claude Code plugin, `idm_optimizer_plugin`, that runs a fan-out code review across many files in a project and aggregates the results into a single report. It mirrors the orchestration pattern used by `idm_eng_plugin` (skill dispatches per-domain agents) but for a different purpose: per-file code review at scale.

Lives alongside `idm_eng_plugin/` in the repo root.

## Architecture

```
idm_optimizer_plugin/
├── README.md
├── CHANGELOG.md
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── code-optimizer/
│       └── SKILL.md          # orchestrator skill
└── agents/
    └── code-reviewer.md      # per-file reviewer (skeleton; user fills in review criteria)
```

- **Skill (`code-optimizer`)**: orchestrator. Gathers the file list, confirms scope, dispatches parallel reviewer agents in batched waves, aggregates returned markdown into a single report.
- **Agent (`code-reviewer`)**: stateless per-file reviewer. Receives one file path, performs the review baked into its system prompt, returns a structured markdown section for that file.

## Flow

1. **Gather files.** Skill prompts the user:
   - "all" → scan the repo for source files (respecting `.gitignore`, configurable extensions), show count, confirm.
   - "list" → accept user-supplied paths or globs.
2. **Confirm scope.** Show resolved file count; if >50, ask for explicit confirmation.
3. **Dispatch in waves.** Default wave size 8 (configurable). Each wave is one orchestrator message containing N parallel `Agent` tool calls to `code-reviewer`. Wait for all in the wave to complete, then launch the next wave.
4. **Collect results.** Each agent returns a structured markdown block (see format below). Orchestrator appends each block to the running report.
5. **Aggregate.** Write `optimizer_report.md` at the repo root with:
   - Top-level header: run timestamp, file count, wave size
   - Per-file index (table of contents)
   - Per-file findings, in stable order (the order files were supplied / discovered)

Failed agents (errors, timeouts) are noted in the report under a "Failures" section but do not halt the run.

## Per-file return format

Each `code-reviewer` agent returns:

```markdown
## <relative/path>
**Summary:** one-line summary

### Findings
- [HIGH] line 42: description
- [MED]  line 88: description
- [LOW]  line 120: description

### Suggestions
- short actionable suggestion
- short actionable suggestion
```

Severity tags: `HIGH`, `MED`, `LOW`. If no findings, the agent returns the header with `**Summary:** No issues found.` and empty sections.

## Agent contract

`code-reviewer.md`:
- **Tools:** Read, Grep, Glob (read-only — no Edit/Write/Bash).
- **Input:** a single absolute file path plus the review instructions in its system prompt (skeleton placeholder; the plugin owner replaces this with the actual review criteria).
- **Output:** the markdown block above and nothing else.
- **Scope:** never reads other files except as needed to resolve a symbol referenced in the target file.

## Skill contract

`skills/code-optimizer/SKILL.md`:
- Triggers on requests like "review all files", "run the optimizer", "audit the codebase", or invocation of a slash command.
- Asks user: all-files vs. supplied-list.
- Discovers files (when "all"): defaults to common source extensions (`.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.md` — configurable in the SKILL.md), excludes `.git/`, `node_modules/`, `dist/`, `build/`, virtualenvs, and anything in `.gitignore`.
- Dispatches waves; default wave size 8, override via user instruction.
- Writes `optimizer_report.md`; if one already exists, prompts before overwriting.

## Non-goals

- The skeleton agent does **not** define real review criteria. The user will replace the placeholder review prompt with their own (extensive) checklist after the plugin scaffold is in place.
- No automatic fixing — review only. A "fixer" sibling skill could come later, modeled on `eng-quality-fixer`.
- No persistence of review history across runs.

## Open configuration knobs

These default in the SKILL.md but can be overridden by the user at invocation time:
- Wave size (default 8)
- File extensions to include (default `.py`, `.ts`, `.tsx`, `.js`, `.jsx`)
- Output report path (default `optimizer_report.md` at repo root)
