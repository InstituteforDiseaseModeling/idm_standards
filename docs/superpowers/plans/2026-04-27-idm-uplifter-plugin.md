# idm_uplifter_plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold a new Claude Code plugin `idm_uplifter_plugin` that runs a fan-out per-file code review across a project and aggregates per-file findings into a single markdown report.

**Architecture:** A plugin sibling to `idm_eng_plugin/`, structured the same way: a `code-uplifter` skill orchestrates, dispatching parallel `code-reviewer` agents (one per file) in batched waves, then concatenates each agent's structured markdown into `uplifter_report.md`. The agent contains a placeholder review prompt the plugin owner will replace later.

**Tech Stack:** Claude Code plugin format (`.claude-plugin/plugin.json`, `skills/`, `agents/`), markdown SKILL.md and agent files, no runtime code.

**Spec:** `docs/superpowers/specs/2026-04-27-idm-uplifter-plugin-design.md`

---

## File Structure

All paths are relative to the repo root `/home/cliffk/idm/idm_standards/`:

- Create: `idm_uplifter_plugin/.claude-plugin/plugin.json` — plugin manifest
- Create: `idm_uplifter_plugin/README.md` — short user-facing intro
- Create: `idm_uplifter_plugin/CHANGELOG.md` — initial entry
- Create: `idm_uplifter_plugin/skills/code-uplifter/SKILL.md` — orchestrator skill
- Create: `idm_uplifter_plugin/agents/code-reviewer.md` — per-file reviewer agent (skeleton)

No tests — this is a markdown-only plugin scaffold. Verification is by structural inspection (files exist, frontmatter parses, content matches spec) and by validating the plugin manifest with the `plugin-dev:plugin-validator` agent at the end.

---

### Task 1: Create plugin manifest

**Files:**
- Create: `idm_uplifter_plugin/.claude-plugin/plugin.json`

- [ ] **Step 1: Create the directory and manifest**

```bash
mkdir -p idm_uplifter_plugin/.claude-plugin
```

Write `idm_uplifter_plugin/.claude-plugin/plugin.json` with this exact content:

```json
{
  "name": "idm-uplifter-plugin",
  "version": "0.1_2026.04.27",
  "description": "Run a fan-out code review across many files in parallel and aggregate findings into a single report"
}
```

- [ ] **Step 2: Verify the manifest is valid JSON**

Run: `python -c "import json; json.load(open('idm_uplifter_plugin/.claude-plugin/plugin.json'))"`
Expected: no output (success).

- [ ] **Step 3: Commit**

```bash
git add idm_uplifter_plugin/.claude-plugin/plugin.json
git commit -m "Add idm_uplifter_plugin manifest"
```

---

### Task 2: Create README and CHANGELOG

**Files:**
- Create: `idm_uplifter_plugin/README.md`
- Create: `idm_uplifter_plugin/CHANGELOG.md`

- [ ] **Step 1: Write the README**

Write `idm_uplifter_plugin/README.md`:

```markdown
# idm_uplifter_plugin

Runs a fan-out code review across many files in a project and aggregates per-file findings into a single markdown report.

## What it does

Given a project, the `code-uplifter` skill:

1. Asks whether to review **all** source files or a **user-supplied list**.
2. Confirms the resolved file count.
3. Dispatches `code-reviewer` subagents in batched parallel waves (default wave size: 8).
4. Collects each agent's structured markdown findings.
5. Writes `uplifter_report.md` at the project root.

## Components

- `skills/code-uplifter/SKILL.md` — orchestrator skill.
- `agents/code-reviewer.md` — per-file reviewer agent (the review criteria are a placeholder for the plugin owner to replace with a real checklist).

## Usage

Invoke the skill from Claude Code:

> "Run the uplifter on this repo."

or via the slash command form:

> `/idm-uplifter-plugin:code-uplifter`

## Configuration

These defaults live in `skills/code-uplifter/SKILL.md` and can be overridden at invocation time:

- Wave size (default `8`)
- File extensions to include (default `.py`, `.ipynb`, `.R`, `.md`, `.qmd`)
- Output report path (default `uplifter_report.md` at repo root)

## Status

This is the skeleton. The review criteria inside `agents/code-reviewer.md` are intentionally generic — replace them with the actual checklist before relying on the plugin's output.
```

- [ ] **Step 2: Write the CHANGELOG**

Write `idm_uplifter_plugin/CHANGELOG.md`:

```markdown
# Changelog

## 0.1_2026.04.27

- Initial scaffold: `code-uplifter` skill and `code-reviewer` agent skeleton.
- Review criteria in the agent are placeholder content to be replaced by the plugin owner.
```

- [ ] **Step 3: Commit**

```bash
git add idm_uplifter_plugin/README.md idm_uplifter_plugin/CHANGELOG.md
git commit -m "Add README and CHANGELOG for idm_uplifter_plugin"
```

---

### Task 3: Create the code-reviewer agent (skeleton)

**Files:**
- Create: `idm_uplifter_plugin/agents/code-reviewer.md`

- [ ] **Step 1: Create the directory**

```bash
mkdir -p idm_uplifter_plugin/agents
```

- [ ] **Step 2: Write the agent file**

Write `idm_uplifter_plugin/agents/code-reviewer.md`:

````markdown
---
description: >
  Reviews a single source file against a fixed checklist and returns a structured
  markdown findings block. Dispatched in parallel by the code-uplifter skill, one
  invocation per file. Read-only — never modifies code.

  Examples:
  <example>
  Context: code-uplifter skill is running and dispatching reviewers in a wave
  user: "Review src/foo.py"
  assistant: "I'll use the code-reviewer agent to review src/foo.py and return findings."
  <commentary>Per-file review task — dispatch code-reviewer agent.</commentary>
  </example>
tools:
  - Read
  - Glob
  - Grep
model: sonnet
color: blue
---

You are a code reviewer agent. You review **one file** against a fixed checklist and return a structured markdown findings block. You never modify code.

## Input

You will receive a prompt specifying:
- `file`: an absolute path to a single source file to review.
- `repo_root`: the repository root, so you can construct relative paths in your output.

If the prompt is missing either of these, return an error block (see Output below) instead of guessing.

## What to do

1. Read the target file with the Read tool.
2. If you need to resolve a symbol referenced in the file (an import, a function call), you may use Grep/Glob/Read on related files. Do not wander beyond what is needed to understand the target file.
3. Apply the **review checklist** below to the target file.
4. Return the findings block in the exact format specified under "Output". Return nothing else — no preamble, no closing remarks.

## Review checklist (PLACEHOLDER — replace with real criteria)

> **Note to the plugin owner:** Replace this entire section with the actual review checklist. The skeleton below is generic and only exists so the agent runs end-to-end during scaffolding.

For each file, check for:

- **Correctness:** obvious bugs, off-by-one errors, incorrect API usage, unhandled error paths that matter.
- **Clarity:** unclear variable names, dead code, overly long functions, missing docstrings on public APIs.
- **Conciseness:** duplicated logic, unnecessary abstractions, code that could be simpler.
- **Safety:** hardcoded secrets, unsafe `eval`/`exec`, SQL or shell injection risks, missing input validation at trust boundaries.

Assign each finding a severity:

- `HIGH` — likely bug, security issue, or correctness problem.
- `MED` — quality issue that materially affects readability or maintainability.
- `LOW` — minor nit, style suggestion.

## Output

Return **exactly** this markdown structure for the file you reviewed, and nothing else:

```markdown
## <relative/path/from/repo_root>
**Summary:** one-line summary of the file's overall state.

### Findings
- [HIGH] line 42: description
- [MED]  line 88: description
- [LOW]  line 120: description

### Suggestions
- short actionable suggestion
- short actionable suggestion
```

If you have no findings, still return the header and `**Summary:**` line, then leave the `### Findings` and `### Suggestions` sections empty (just the header) and set Summary to `No issues found.`.

If the input is malformed (missing `file` or `repo_root`, or the file does not exist), return:

```markdown
## <path-or-unknown>
**Summary:** ERROR — <one-line reason>.

### Findings

### Suggestions
```
````

- [ ] **Step 3: Verify the frontmatter parses**

Run: `python -c "import re,sys; t=open('idm_uplifter_plugin/agents/code-reviewer.md').read(); m=re.match(r'^---\n(.*?)\n---\n', t, re.S); assert m, 'no frontmatter'; import yaml; yaml.safe_load(m.group(1)); print('ok')"`
Expected: `ok`

- [ ] **Step 4: Commit**

```bash
git add idm_uplifter_plugin/agents/code-reviewer.md
git commit -m "Add code-reviewer agent skeleton"
```

---

### Task 4: Create the code-uplifter skill (orchestrator)

**Files:**
- Create: `idm_uplifter_plugin/skills/code-uplifter/SKILL.md`

- [ ] **Step 1: Create the directory**

```bash
mkdir -p idm_uplifter_plugin/skills/code-uplifter
```

- [ ] **Step 2: Write the SKILL.md**

Write `idm_uplifter_plugin/skills/code-uplifter/SKILL.md`:

````markdown
---
name: code-uplifter
description: Fan-out per-file code review for an entire project. Dispatches the code-reviewer agent in parallel waves over a set of files and aggregates the findings into uplifter_report.md. Use when the user asks to "uplift the codebase", "run the uplifter", "review all files", or invokes the /idm-uplifter-plugin:code-uplifter command.
argument-hint: "[project_path] [wave_size]"
allowed-tools: Read, Glob, Grep, Bash, Write, Agent
---

Run a fan-out code review across many files and aggregate the findings into `uplifter_report.md`.

Skill version: 0.1_2026.04.27

## Defaults

These can be overridden by anything the user says when invoking the skill:

- **Wave size:** `8` parallel agents per wave.
- **File extensions:** `.py`, `.ipynb`, `.R`, `.md`, `.qmd`.
- **Excluded directories:** `.git`, `node_modules`, `dist`, `build`, `.venv`, `venv`, `__pycache__`, `_site`.
- **Output path:** `uplifter_report.md` at the project root.

If the user supplies different values (e.g., "use a wave size of 4", "include `.js` files", "write to `review.md`"), follow their instruction.

## Step 1: Resolve the project path

The first argument is the project path. If not supplied, default to the current working directory. Resolve it to an absolute path and confirm the directory exists.

## Step 2: Choose file-selection mode

Ask the user:

> "Should I review **all** source files in the project, or do you want to supply a **list** of files/globs?"

- If **all**: proceed to Step 3a.
- If **list**: proceed to Step 3b.

## Step 3a: Discover files (all-files mode)

Use `Glob` to find files under the project path matching the configured extensions. Then filter out anything inside an excluded directory.

A simple pattern: run `Glob` once per extension (e.g., `**/*.py`), union the results, and drop any path whose components contain an excluded directory name.

Also drop anything ignored by git. To check, run from the project root:

```bash
git check-ignore -v -- <path1> <path2> ...
```

(or, equivalently, intersect the discovered list against the output of `git ls-files`). Files that are git-ignored are excluded.

## Step 3b: Resolve a user-supplied list

The user provides paths or globs. Expand globs using `Glob`. Verify each resolved path exists. Drop directories (only files are reviewed).

## Step 4: Confirm scope

Show the user the resolved file count. If the count is greater than 50, ask for explicit confirmation before proceeding:

> "This will dispatch reviews for N files in waves of W. Proceed?"

If the count is zero, stop and tell the user no files matched.

## Step 5: Check the output path

If `uplifter_report.md` already exists at the project root, ask the user whether to overwrite or write to a different path. Do not silently overwrite.

## Step 6: Dispatch in waves

Split the file list into chunks of `wave_size`. For each chunk:

1. Send a single message containing one `Agent` tool call per file in the chunk, all in parallel. Each call:
   - Uses `subagent_type: "code-reviewer"`.
   - Has a short `description` like `Review <relative/path>`.
   - Has a `prompt` of the form:

     ```
     Review the following file and return the structured markdown block per your instructions.

     file: <absolute path>
     repo_root: <absolute project root>
     ```

2. Wait for all agents in the wave to finish.
3. Append each returned markdown block to an in-memory list, in the same order the files were dispatched. If an agent failed (errored or returned malformed output), record the file path and error in a separate `failures` list — do not abort the run.

Then proceed to the next wave.

## Step 7: Write the report

Write the report file (default `uplifter_report.md`) at the project root with this structure:

```markdown
# Uplifter Report

- **Generated:** <UTC timestamp>
- **Project:** <absolute path>
- **Files reviewed:** <count>
- **Wave size:** <wave_size>

## Index

- [<relative/path/1>](#<anchor-1>)
- [<relative/path/2>](#<anchor-2>)
...

---

<concatenated per-file blocks, in dispatch order>

---

## Failures

<one bullet per failed file with a short error reason; omit this section entirely if there were no failures>
```

Anchors are GitHub-flavored markdown anchors derived from the per-file `## <relative/path>` headers.

## Step 8: Tell the user where the report is

Print a short summary message:

> "Uplifter run complete. N files reviewed (F failed). Report written to `<output path>`."
````

- [ ] **Step 3: Verify the frontmatter parses**

Run: `python -c "import re,yaml; t=open('idm_uplifter_plugin/skills/code-uplifter/SKILL.md').read(); m=re.match(r'^---\n(.*?)\n---\n', t, re.S); assert m; yaml.safe_load(m.group(1)); print('ok')"`
Expected: `ok`

- [ ] **Step 4: Commit**

```bash
git add idm_uplifter_plugin/skills/code-uplifter/SKILL.md
git commit -m "Add code-uplifter orchestrator skill"
```

---

### Task 5: Validate the plugin

**Files:** none modified.

- [ ] **Step 1: List the final structure and confirm against the spec**

Run: `find idm_uplifter_plugin -type f | sort`
Expected output (exactly these files):

```
idm_uplifter_plugin/.claude-plugin/plugin.json
idm_uplifter_plugin/CHANGELOG.md
idm_uplifter_plugin/README.md
idm_uplifter_plugin/agents/code-reviewer.md
idm_uplifter_plugin/skills/code-uplifter/SKILL.md
```

- [ ] **Step 2: Run the plugin validator agent**

Dispatch the `plugin-dev:plugin-validator` agent against `idm_uplifter_plugin/`. Pass it the absolute path to the plugin and ask it to validate the structure, manifest, skill frontmatter, and agent frontmatter.

If it reports any issues, fix them inline and re-run. If it reports clean, continue.

- [ ] **Step 3: Final commit (if validator changes were made)**

If Step 2 produced fixes:

```bash
git add idm_uplifter_plugin
git commit -m "Address plugin-validator feedback for idm_uplifter_plugin"
```

Otherwise skip.

---

## Self-review notes

- Spec coverage:
  - Plugin layout (spec §Architecture) → Tasks 1–4.
  - Per-file return format (spec §Per-file return format) → Task 3, "Output" section of agent.
  - Skill flow (spec §Flow steps 1–5) → Task 4 Steps 2–7.
  - Failure handling (spec §Flow last paragraph) → Task 4 Step 6 ("failures list") and Step 7 ("Failures" section).
  - Configuration knobs (spec §Open configuration knobs) → Task 4 "Defaults" block.
  - Skeleton review criteria (spec §Non-goals first bullet) → Task 3 "Review checklist (PLACEHOLDER)".
  - Triggers (spec §Skill contract) → Task 4 frontmatter `description`.
- No placeholders in the plan; the only intentional placeholder is the review checklist inside the agent file, which the spec explicitly calls out as the user's to replace.
- Type/name consistency: plugin name `idm-uplifter-plugin`, skill `code-uplifter`, agent `code-reviewer`, report `uplifter_report.md` — used consistently across tasks.
