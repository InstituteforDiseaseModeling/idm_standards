---
name: idm-code-uplifter
description: Fan-out per-file code review for an entire project. Dispatches the idm-code-reviewer agent in parallel waves over a set of files and aggregates the findings into uplifter_report.md. Use when the user asks to "uplift the codebase", "run the uplifter", "review all files", or invokes the /idm-uplifter-plugin:idm-code-uplifter command.
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
   - Uses `subagent_type: "idm-code-reviewer"`.
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
