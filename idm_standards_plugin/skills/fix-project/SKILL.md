---
name: fix-project
description: The Fix-Project skill reads whichever IDM audit reports exist in a project (code_audit.md, docs_audit.md, code_audit_exhaustive.md) and implements prioritized fixes across code and documentation. Use this skill when the user asks to "fix my project", "apply the audit recommendations", "fix the code and docs", says "now fix it" after running audit-project, or invokes /idm-standards:fix-project. For code-only fixes from code_audit.md, fix-code can be used directly instead.
argument-hint: "[project_path]"
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, AskUserQuestion, Skill
---

Apply fixes from whichever IDM audit reports exist in a project — dispatching `fix-code` for the code report and implementing documentation fixes directly.

Skill version: 2.0_2026.06.10

## Step 1: Find the audit reports

In the project directory (argument, or current working directory), look for:

- `code_audit.md` (or, for compatibility with earlier plugin versions, `engineering_score.md`)
- `docs_audit.md`
- `code_audit_exhaustive.md`

If the invoking context restricts scope (e.g. `audit-docs` chained here with "act on docs_audit.md only"), honor that. If **none** of the reports exist, stop and tell the user:

> "No audit reports found. Please run `/idm-standards:audit-project` (or `audit-code` / `audit-docs`) first."

If more than one report exists and the scope wasn't restricted, confirm with the user via one AskUserQuestion (multiSelect) which reports to act on — default: all found.

## Step 2: Fix the code

If acting on `code_audit.md`: invoke the **`fix-code`** skill via the Skill tool, passing the project path. It handles its own planning, confirmation, implementation, and recording of proposed solutions (including the Tier 2/3 lock-artifact question).

If acting on `code_audit_exhaustive.md`: treat its CRITICAL and HIGH findings as additional fix candidates. Fold them into the plan below (or into fix-code's plan where they overlap with `code_audit.md` recommendations), fixing the clearly safe ones and recording the rest.

## Step 3: Fix the docs

If acting on `docs_audit.md`, implement its recommendations directly (there is no separate docs fixer). Parse the **Recommendations** section and classify, mirroring fix-code's approach:

| Category | Examples |
|----------|----------|
| **Can implement now** | README sections (installation, usage, structure), LICENSE, CHANGELOG scaffold, folder READMEs, docstring fixes, broken links, TOC reorganization per the diataxis findings, Vale errors |
| **Will scaffold** | Tutorial/notebook skeletons, docs-site config (`mkdocs.yml`/`_quarto.yml` from the templates in `docs_templates/`), API reference setup |
| **Cannot implement** | Writing full tutorials or user guides (domain knowledge), persona-targeted rewrites needing scientific content, anything requiring publication decisions |

Present the combined plan (code + docs) to the user **before making any changes**, wait for confirmation, then work through items in priority order (the reports rank them). Respect the report's recorded strictness and any user decisions.

## Step 4: Record proposed solutions

For every item classified "Cannot implement" (or skipped by the user), write an entry into the **Proposed solutions** section of the report it came from (`code_audit.md` items are handled by fix-code; add docs items to `docs_audit.md`, creating the section if needed). Each entry: the issue, a concrete proposed approach (steps, outline, or sketch), estimated effort, and why it can't be automated. Record any user decisions made during the run so future audits and fixes respect them. Do not modify report scores or other sections.

## Step 5: Report what was done

Summarize in chat, grouped by report:

```
## Changes Made

### Code (via fix-code)
<fix-code's summary>

### Docs
✅ Added Installation and Project structure sections to README
✅ Scaffolded docs/ with mkdocs.yml from the IDM template
⏭ Skipped: getting-started tutorial (domain knowledge required — outline added to docs_audit.md)

Re-run `/idm-standards:audit-project` to get updated results.
```
