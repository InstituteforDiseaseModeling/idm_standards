---
name: update-docs-plugin
description: Use when docs_guidance/ has changed and the idm-standards plugin's documentation skills need to be synced with those changes. Triggers on requests like "update the docs skills", "sync the plugin with docs_guidance", "propagate the docs_guidance changes", "bump the plugin version", or "update the changelog for the docs changes". Also use proactively after any edits to docs_guidance/ when the user indicates they're ready to release, and whenever the user mentions keeping the plugin in sync with the guidance source — even if they don't explicitly name the plugin.
---

# Update the idm-standards docs skills from docs_guidance

The documentation skills in `idm_standards_plugin/skills/` (`audit-docs`, `audit-docs-structure`, `audit-personas`, `audit-docstrings`) are derived from, and must stay consistent with, the source documentation in `docs_guidance/`. When the guidance changes, these skills need to learn those changes — otherwise the plugin drifts from the project's actual documentation standards and the audit/review skills give stale advice.

The `audit-docs` skill also bundles generated copies of repo-root assets — `vale.ini`, `.github/styles/`, and `docs_templates/` — under `idm_standards_plugin/skills/audit-docs/assets/`. An installed plugin only ships the `idm_standards_plugin/` directory, so the skill cannot read the repo-root sources at runtime; these bundled copies are how it reaches them. When any of those sources change, the bundled copies must be re-synced too (step 6b).

This skill walks you through that sync: identify what changed, figure out which plugin skills need updating, propose the edits, apply them, bump the version, and update the changelog.

## Workflow

### 1. Determine the diff range

If the user specified a commit, commit range, or date range in their request, use that. Otherwise **default to "since the last release"**: the diff range is the commit that set the current plugin version → HEAD.

Find the last-release commit with:

```bash
CURRENT_VERSION=$(python -c "import json; print(json.load(open('idm_standards_plugin/.claude-plugin/plugin.json'))['version'])")
git log -S "\"version\": \"$CURRENT_VERSION\"" --format=%H -- idm_standards_plugin/.claude-plugin/plugin.json | head -1
```

That commit hash is your base. The range is `<commit>..HEAD`.

If the user's intent is ambiguous (e.g., they just say "update the plugin" with no other context), ask: "Diff what — since the last release (default), a specific commit/range, or a date range?"

### 2. Read the diff of docs_guidance

```bash
git diff <range> -- docs_guidance/
```

Also list files that were added or deleted in the range:

```bash
git diff --name-status <range> -- docs_guidance/
```

Also check whether the bundled-asset sources changed in the range — if any of these are non-empty, step 6b applies:

```bash
git diff --name-status <range> -- vale.ini .github/styles/ docs_templates/
```

**Notebook files**: `docs_guidance/topic-types/notebook.ipynb` produces noisy JSON diffs. For notebooks, inspect the current file content directly rather than relying on the diff — or use `git diff --stat` to see whether it changed meaningfully, then read the current notebook if it did.

### 3. Map changes to plugin skills

The plugin has four documentation skills: `audit-docs-structure`, `audit-personas`, `audit-docstrings`, `audit-docs`. Use your judgment — read both the diff and the relevant `SKILL.md` files before deciding — but the typical mapping is:

| `docs_guidance/` area | Likely affected plugin skill |
|-----------------------|------------------------------|
| `personas/` | `skills/audit-personas/` |
| `topic-types/` (diataxis concepts, tutorial/howto/reference/explanation, TOC) | `skills/audit-docs-structure/` |
| Docstring-specific guidance (wherever it lives) | `skills/audit-docstrings/` |
| Broad structural or process changes | `skills/audit-docs/` |

Files like `install.md`, `mkdocs.md`, `quarto.md`, `vale.md`, `home.md`, `index.md` are usually about tooling or landing pages, not skill content — but confirm with the user before dismissing them. A single guidance change can affect multiple plugin skills; note all of them.

### 4. Read the current plugin skills

For each skill you identified as potentially affected, read `idm_standards_plugin/skills/<name>/SKILL.md`. You need the current content to (a) propose edits that preserve structure and voice, and (b) judge whether the guidance change is already reflected.

### 5. Propose updates and wait for confirmation

**Do not edit anything yet.** Present a plan to the user in this shape:

```
## Proposed plugin updates

### skills/<name>/SKILL.md
- <specific change, phrased as what the skill will now say or do differently>
- <another change>

### skills/<other>/SKILL.md
- <change>

### No change needed: skills/<name>, skills/<name>
Reason: <brief reason>
```

Wait for the user to confirm, reject, or modify the plan. If they push back, revise and re-present — do not proceed to editing until they confirm.

### 6. Apply the updates

Edit each affected `SKILL.md` using the `Edit` tool. When editing:

- Preserve existing frontmatter (`name`, `description`) unless the user explicitly asked for a change there. If the skill's scope genuinely shifted, update the description.
- Match the voice and structure of the existing skill — these skills read as a coherent set and shouldn't diverge stylistically.
- Reference `docs_guidance/` files by relative path rather than pasting whole sections. The plugin skills are pointers to the authoritative guidance, not duplicates. Duplication creates drift.
- If a new guidance file was added that a skill should reference, add the pointer; don't inline the content.

### 6b. Sync bundled audit-docs assets

Only if the asset-source check in step 2 showed changes to `vale.ini`, `.github/styles/`, or `docs_templates/` (or if the bundled copies are missing entirely). Re-generate the copies under `idm_standards_plugin/skills/audit-docs/assets/`:

```bash
ASSETS=idm_standards_plugin/skills/audit-docs/assets
rm -rf "$ASSETS/styles" "$ASSETS/docs_templates"
cp -r .github/styles "$ASSETS/styles"
cp -r docs_templates "$ASSETS/docs_templates"
cp vale.ini "$ASSETS/vale.ini"
```

Then re-point the bundled `vale.ini` `StylesPath` at the co-located styles dir — the repo-root copy uses `.github/styles`, the bundled copy must use `styles`:

```bash
sed -i 's|^StylesPath = .github/styles|StylesPath = styles|' "$ASSETS/vale.ini"
```

These copies are generated artifacts — never hand-edit them; edit the repo-root sources and re-run this step. The `assets/README.md` records this. A change here is a behavior change to `audit-docs`, so it counts toward the version bump and changelog below.

### 7. Bump the version

The version scheme is `MAJOR.MINOR_YYYY.MM.DD`.

- Default bump: **MINOR**, with the date updated to today. Example: `1.0_2026.04.13` → `1.1_2026.04.20`.
- Suggest a **MAJOR** bump only if something breaking happened: a skill was removed, renamed, or had its triggering description changed in a way that could surprise existing users.

**Always prompt the user to confirm the new version number before writing it.** Show them the old version, the proposed new version, and the reason for the bump type. Wait for confirmation.

Then update the version in **both** places:

1. `idm_standards_plugin/.claude-plugin/plugin.json` — the top-level `version` field
2. `.claude-plugin/marketplace.json` — the `version` field inside the single `idm-standards` entry

Note: the docs skills share the plugin version with the code-audit skills (it is one plugin now). Coordinate with `idm_standards_plugin/admin/update_prompt.md` if both the docs guidance and the engineering guidance changed in the same release.

### 8. Update the changelog

File: `idm_standards_plugin/CHANGELOG.md` (shared across all skills in the plugin).

Prepend a new version section above the previous one (newest first), matching the existing format. Write bullets describing the documentation-skill changes; if the same release also changed the code-audit skills, fold both sets of changes into the one version entry.

Write bullets from the user's perspective — what changed in the plugin's behavior or coverage, not a file-level diff summary. "Added persona guidance for policy-influencer" is better than "updated 3 files in skills/personas/".

### 9. Summarize for the user

Report:

- Which skills were updated (and which weren't, with a one-line reason)
- Old version → new version
- Path to the changelog entry
- A suggested one-line git commit message

**Do not create the commit.** Leave that to the user unless they explicitly ask for it.

## Why these steps matter

The plugin is the runtime artifact; `docs_guidance/` is the source of truth. Without syncing, the two drift — the plugin gives advice that contradicts the published guidance, and users who rely on the plugin get misled. The version bump and changelog make the sync visible: anyone looking at the plugin or the marketplace entry can tell at a glance whether it reflects the current guidance. Skipping the version bump is a silent change, which is worse than not updating at all.

The user-confirmation gate at step 5 exists because guidance changes aren't always meant to propagate to the plugin — sometimes a docs_guidance edit is a typo fix, a tooling note, or a reorganization that doesn't alter the substance the skills are teaching. The user knows which is which; the skill should not assume.
