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

## Step 7: Repo-level review

Per-file agents only evaluate the `files:` section of `metrics.yaml`. You — the skill — are responsible for the `repo:` section, which covers project-wide concerns (README, tests, CI, licenses, secrets, releases, etc.).

Read `${CLAUDE_PLUGIN_ROOT}/agents/metrics.yaml` and walk the `repo:` tree. Each leaf is `category > dimension > key: description` (e.g. `quality > correct > ci: "Tests are incorporated in an automated pipeline..."`).

For every criterion, gather comprehensive evidence and make an explicit judgment. Use every tool available to you — `Glob`, `Grep`, `Read`, `Bash` — to inspect the project thoroughly. Read the full README, the full CHANGELOG, the full top-level config files (`pyproject.toml`, `setup.py`, `package.json`, `DESCRIPTION`, `environment.yml`, `requirements*.txt`, `poetry.lock`, etc.). Inspect every CI workflow file in full. Walk `tests/` to assess coverage and style. Read `LICENSE` in full and cross-check it against declared dependencies' licenses. Run `git log`, `git tag --list`, `git remote -v` as needed to assess versioning, release history, and hosting. Read `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `ROADMAP.md`, issue/PR templates, and any `docs/` content. Inspect `.gitignore` and `.gitattributes` for what is and isn't tracked.

Suggested checks per criterion (non-exhaustive — apply judgment and add more as needed):

- `quality.correct.spec` → read the full README and any `docs/` index; assess whether the scientific/technical scope is clearly and correctly described.
- `quality.correct.validated` → search README/docs for validation, peer-review citations, comparisons to published results, or benchmark suites.
- `quality.correct.test-coverage` → enumerate test files, run coverage if a coverage config exists, and look for obvious gaps (untested public APIs).
- `quality.correct.test-style` → read several test files end-to-end; assess whether they are mostly unit vs. end-to-end and whether they exercise scientific behavior.
- `quality.correct.ci` → list every workflow under `.github/workflows/` (or equivalent) and read each in full; confirm tests actually run.
- `quality.clear.structure` → walk the top two or three directory levels; assess whether the layout matches conventions for the project's language/ecosystem.
- `quality.concise.duplication` → spot-check for duplicated modules, parallel implementations, or near-identical config files.
- `usability.simple.workflows` → assess whether common tasks (install, run, test) are one-liners; read any `Makefile` / `justfile` / top-level scripts.
- `usability.performant.fast` / `usability.performant.profiled` → look for benchmark scripts, profiling docs, or performance regression tests.
- `usability.documented.*` → read the full README, the docs site config (`mkdocs.yml`, `_config.yml`, `conf.py`), and a representative sample of doc pages; assess audience fit, tutorial presence, and UI clarity.
- `usability.accessible.github` → check `git remote -v` and confirm the repo lives in an appropriate org.
- `usability.accessible.key-files` → check for `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `ROADMAP.md`.
- `usability.accessible.installation` → follow the README's install instructions mentally; confirm they're 1–3 commands and don't require special environments.
- `usability.accessible.support` → look for issue templates, support docs, a discussions link, or contact info.
- `usability.accessible.ai-friendly` → check for `CLAUDE.md`, `.claude/`, `AGENTS.md`, skills, MCP server configs, or other AI-assistant scaffolding.
- `safety.compliant.data-permission` → if any data is bundled or downloaded, search README/docs for permission/citation/license info.
- `safety.compliant.secrets` → grep the entire tracked tree for likely-secret patterns (`API_KEY=`, `SECRET=`, `TOKEN=`, `BEGIN PRIVATE KEY`, AWS access-key prefixes, common provider patterns) and review any matches. **Do not scan binary blobs** — restrict text scans to text-extension files (use `git ls-files` and filter, or skip large/binary files explicitly).
- `safety.compliant.licenses` → read `LICENSE`; for each declared dependency, identify its license and flag incompatibilities with this project's license.
- `safety.reproducible.dependencies` → confirm dependencies are pinned in a lock file or environment file appropriate for the language; for non-library code, a lock file is required.
- `safety.reproducible.versioning` → run `git tag --list` and read `CHANGELOG.md` in full; assess whether semver is followed and whether tags exist for each release.
- `safety.reproducible.published` → check whether the package is on PyPI / CRAN / npm / etc. as appropriate (look for `pyproject.toml` `[project]` metadata, a publish workflow, or visible release artifacts).

Use the same severity scale and tagging convention as the per-file agent. If a check is genuinely impossible from inside the repo (e.g. you cannot reach the public internet), say so explicitly rather than guessing. Do not modify any files.

Produce a single repo-level findings block in this format (mirrors the per-file agent's output):

```markdown
## Repo
**Summary:** One-paragraph summary of the project's overall state at the repo level.

### Issues
- [HIGH] quality.correct.ci (overall): No CI pipeline detected; add a GitHub Actions workflow that runs the test suite on push/PR.
- [MED] usability.accessible.key-files (overall): CHANGELOG is missing.
- [LOW] safety.reproducible.versioning (overall): No git tags found; adopt semantic versioning and tag releases.

### Assessments
- quality.correct.spec: README clearly describes the project purpose and scope.
- quality.correct.ci: No workflows under `.github/workflows/`.
- ...one bullet per criterion in metrics.yaml's `repo:` section...
```

Every criterion under `repo:` must appear once in the `### Assessments` section, even if the assessment is "N/A" or "Not applicable to this project". If a `CRITICAL` issue is found at the repo level (e.g. an exposed API key), prefix the summary with `FAIL: Critical issues were found in this repository that need to be addressed immediately. These are listed below.` — same convention as the per-file agent.

## Step 8: Write the report

Write the report file (default `uplifter_report.md`) at the project root with this structure:

```markdown
# Uplifter Report

- **Generated:** <UTC timestamp>
- **Project:** <absolute path>
- **Files reviewed:** <count>
- **Wave size:** <wave_size>

## Index

- [Repo](#repo)
- [<relative/path/1>](#<anchor-1>)
- [<relative/path/2>](#<anchor-2>)
...

---

<repo-level findings block from Step 7>

---

<concatenated per-file blocks, in dispatch order>

---

## Failures

<one bullet per failed file with a short error reason; omit this section entirely if there were no failures>
```

Anchors are GitHub-flavored markdown anchors derived from the `## Repo` and per-file `## <relative/path>` headers.

## Step 9: Tell the user where the report is

Print a short summary message:

> "Uplifter run complete. N files reviewed (F failed). Report written to `<output path>`."
