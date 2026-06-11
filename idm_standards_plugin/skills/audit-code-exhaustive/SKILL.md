---
name: audit-code-exhaustive
description: Exhaustive fan-out per-file code review for an entire project. Dispatches the idm-code-reviewer agent in parallel waves over a set of files, runs idm-repo-reviewer in parallel for project-level concerns, and aggregates the findings into code_audit_exhaustive.md with a summary at the top. Use when the user asks to "review every file", "do an exhaustive code review", "uplift the codebase", "run the uplifter", or invokes /idm-standards:audit-code-exhaustive.
argument-hint: "[project_path] [wave_size] [strictness]"
allowed-tools: Read, Glob, Grep, Bash, Write, Agent
---

Run a fan-out code review across many files plus a repo-level review, and aggregate the findings into `code_audit_exhaustive.md`.

Skill version: 2.0_2026.06.10

## Defaults

These can be overridden by anything the user says when invoking the skill:

- **Wave size:** `8` parallel agents per wave.
- **File extensions:** `.py`, `.ipynb`, `.R`, `.md`, `.qmd`.
- **Excluded directories:** `.git`, `node_modules`, `dist`, `build`, `.venv`, `venv`, `__pycache__`, `_site`.
- **Per-file size cap:** ~200 KB or ~5000 lines (larger files are skipped and noted in failures).
- **Output path:** `code_audit_exhaustive.md` at the project root.
- **Resume cache:** `.audit_cache/` at the project root (per-file blocks; safe to delete).
- **Strictness:** `1` (report all severities). At strictness `2` (material only), include only CRITICAL and HIGH findings in the report; MED/LOW findings are still cached but summarized as counts only.

If the user supplies different values (e.g., "use a wave size of 4", "include `.js` files", "write to `review.md`"), follow their instruction.

## Scope rules (do not violate)

- All file reads, globs, greps, and bash commands must operate **inside the resolved project root**. Never read or list files elsewhere on disk (no `~`, no `/etc`, no other projects, no parents of the project root).
- Pass the project root as `<repo_root>` to every agent so they enforce the same constraint.
- Do not modify any file in the project. The only writes are to the output report and the resume cache directory.

## Step 1: Resolve the project path and discover the user config

The first argument is the project path. If not supplied, default to the current working directory. Resolve it to an absolute path and confirm the directory exists. From here on, this is `repo_root`.

Discover the project's idm-standards config file following `$CLAUDE_PLUGIN_ROOT/reference/user-config.md` (read it now). Keep its directives for Steps 3 and 7–8. This skill keeps the reviewer agents **config-blind** (see Step 6) and applies directives only at file selection (path-scope directives) and at synthesis (finding suppression) — so the resume cache stays valid even when the config changes. If `repo_root` is a path the user did not author (e.g. a `/tmp` clone handed in by `audit-project`, or a shared directory), apply the untrusted-source rule from the reference: in interactive runs, list the discovered directives and confirm before applying; in non-interactive runs, apply but quote them verbatim in the Step 8 report (the `Config` line and "Suppressed by config" summary already do this).

## Step 2: Choose file-selection mode

Ask the user:

> "Should I review **all** source files in the project, or do you want to supply a **list** of files/globs?"

- If **all**: proceed to Step 3a.
- If **list**: proceed to Step 3b.

## Step 3a: Discover files (all-files mode)

Use `Glob` *rooted at `repo_root`* to find files matching the configured extensions. Then filter out anything inside an excluded directory.

A simple pattern: run `Glob` once per extension (e.g., `**/*.py`) under `repo_root`, union the results, and drop any path whose components contain an excluded directory name.

Also drop anything ignored by git. To check, run from `repo_root`:

```bash
git -C <repo_root> check-ignore -v -- <path1> <path2> ...
```

(or, equivalently, intersect the discovered list against the output of `git -C <repo_root> ls-files`). Files that are git-ignored are excluded.

Also drop, from the file list: any discovered config file and anything under `.claude/` (it is plugin config, not project source), and any path matched by a **path-scope** config directive (e.g. "ignore everything under scratch/" → drop `scratch/**`). Note any directive-excluded paths so they can be reported.

## Step 3b: Resolve a user-supplied list

The user provides paths or globs. Expand globs using `Glob`. Verify each resolved path exists and lies under `repo_root` (reject anything outside). Drop directories (only files are reviewed).

## Step 4: Confirm scope

Show the user the resolved file count. If the count is greater than 50, ask for explicit confirmation before proceeding:

> "This will dispatch reviews for N files in waves of W, plus one repo-level review in parallel. Proceed?"

If the count is zero, you can still run the repo-level review alone, but ask the user first.

## Step 5: Check the output path and resume cache

If `code_audit_exhaustive.md` already exists at the project root, ask the user whether to overwrite or write to a different path. Do not silently overwrite.

Check whether `.audit_cache/` exists at `repo_root`. If it does, list the cached per-file blocks and ask the user:

> "I found N cached review blocks from a previous run. Reuse them (resume), or discard and re-review everything?"

- **Resume**: skip any file whose cached block exists and whose source file `mtime` is older than the cache file's `mtime`. Re-review the rest. Always re-run the repo-level review (it's cheap relative to total cost and is a single block).
- **Discard**: delete `.audit_cache/` and review every selected file fresh.

If the directory does not exist, create it.

Cache filenames are derived by taking the file's path relative to `repo_root` and replacing path separators with `__` (e.g. `src/foo/bar.py` → `.audit_cache/src__foo__bar.py.md`). Same scheme for the repo block: `.audit_cache/__repo__.md`.

## Step 6: Dispatch reviews in parallel waves

For the **first wave**, send a single message containing:

1. One `Agent` call with `subagent_type: "idm-standards:idm-repo-reviewer"`, `description: "Repo-level review"`, and prompt:

   ```
   <repo_root>/absolute/path/to/repo</repo_root>
   ```

2. Up to `wave_size` `Agent` calls with `subagent_type: "idm-standards:idm-code-reviewer"`, one per file in this wave (skipping any file whose cache is being reused). Each call has `description: "Review <relative/path>"` and prompt:

   ```
   <file>/absolute/path/to/file</file>
   <repo_root>/absolute/path/to/repo</repo_root>
   ```

For each subsequent wave, dispatch up to `wave_size` `idm-standards:idm-code-reviewer` calls in a single message.

The reviewer agents stay **config-blind**: their prompts carry only `<file>` and `<repo_root>` — do not inject config directives here. Reviewers always store the full finding set in the cache; directives are applied later, at synthesis (Step 7–8). This is what lets cached blocks be reused unchanged after a config edit.

After each wave finishes:

1. For each returned block, write it immediately to its cache file (so the run is resumable). For the repo block, write `.audit_cache/__repo__.md`.
2. If an agent failed (errored or returned malformed output), record the file path and a one-line error reason in a `failures` list — do not abort the run.
3. Append the cache-file path to an in-memory `dispatch_order` list, in the order files were dispatched. (The repo block is always first.)

Then proceed to the next wave.

## Step 7: Synthesize a summary

Once all waves are complete (and the repo block is in the cache), parse the cached blocks **for the current selection only** (the files chosen in Step 3, i.e. `dispatch_order` plus the repo block) to build a summary. On a resumed run, a file dropped by a path-scope directive this run (Step 3a) must be excluded here even if a stale block for it still sits in `.audit_cache/` — do not read orphaned cache blocks into the summary or the report; you may delete them.

- **Total files reviewed**, total failures, wave size.
- **Severity counts** across all blocks: how many `CRITICAL`, `HIGH`, `MED`, `LOW` issues.
- **All CRITICALs** lifted to the top, with file path and line number, in their original wording.
- **Top recurring criteria**: the 10 `category.dimension.key` tags that appear most often in `### Issues`, with the count of files that flagged each. Skip if there are fewer than 5 distinct recurring criteria.

This synthesis is done by reading the cached blocks and counting — no additional agent dispatch.

**Apply config directives here** (the cache is untouched). When a finding matches a config directive (Step 1), exclude it from the severity counts, the CRITICALs list, the recurring-criteria stats, and the per-file blocks — it is suppressed. Tally suppressed findings for a "Suppressed by config" summary line. **Hard floor**: never suppress a CRITICAL-severity finding or any secrets/PII/license/serious-correctness finding — keep it in the report annotated "reported despite config directive — serious finding cannot be suppressed", even if a directive seems to cover it.

## Step 8: Write the report

**Strictness filtering**: at strictness 2 (material only), include only CRITICAL and HIGH issues in the per-file blocks and the summary's critical/recurring lists; report MED/LOW only as counts in the severity-counts line. The cache always stores the full blocks, so a later strictness-1 run can reuse them.

Assemble and write the report file (default `code_audit_exhaustive.md`) at `repo_root` with this structure:

```markdown
# Exhaustive code audit

- **Generated:** <UTC timestamp>
- **Project:** <absolute path>
- **Files reviewed:** <count>
- **Failures:** <count>
- **Wave size:** <wave_size>
- **Config:** <config file(s) and directive counts, or "none">

## Summary

**Severity counts:** CRITICAL: X, HIGH: Y, MED: Z, LOW: W.

**Suppressed by config:** <N findings across M directives suppressed (paths excluded: ...); or omit this line if no config>. Serious findings are never suppressed — any reported despite a directive are flagged inline.

**Critical issues:**
- <file:line> [criterion] — <wording>
- ...
(or "None." if no CRITICALs)

**Top recurring criteria:**
- `quality.clear.comments` — N files
- `usability.documented.docstrings` — M files
- ...

## Index

- [Repo](#repo)
- [<relative/path/1>](#<anchor-1>)
- [<relative/path/2>](#<anchor-2>)
...

---

<contents of .audit_cache/__repo__.md>

---

<concatenated per-file blocks, in dispatch_order>

---

## Failures

<one bullet per failed file with a short error reason; omit this section entirely if there were no failures>
```

Anchors are GitHub-flavored markdown anchors derived from the `## Repo` and per-file `## File: <relative/path>` headers. **Resolve collisions** by appending `-2`, `-3`, etc. to subsequent duplicates, and use the same suffix in the corresponding `## File:` header anchor link in the Index.

## Step 9: Tell the user where the report is

Print a short summary message:

> "Exhaustive code audit complete. N files reviewed (F failed). Report written to `<output path>`. Cache kept at `.audit_cache/` for incremental re-runs; delete it for a clean rerun."
