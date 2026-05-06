# Changelog

## 0.2_2026.05.06

- Split repo-level review into a dedicated `idm-repo-reviewer` agent, dispatched in parallel with the first file wave instead of running inline in the orchestrator.
- Inlined review checklists into both agents and removed `agents/metrics.yaml`. The file-level checklist now lives in `idm-code-reviewer.md`; the repo-level checklist lives in `idm-repo-reviewer.md`. Secrets remain checked at both scopes intentionally.
- Added a top-of-report **Summary** section: severity counts across all blocks, all CRITICALs lifted to the top with file/line, and top recurring criteria.
- Added resumability via `.uplifter_cache/`: each completed block is written to disk as it lands, and a re-run can reuse cached blocks for unchanged files.
- Switched the agent input format to XML-style tags (`<file>...</file>`, `<repo_root>...</repo_root>`) for unambiguous parsing.
- Added an explicit scope rule to both agents and the skill: never read files outside `<repo_root>`. Glob/Grep/Read/Bash are constrained to the project tree.
- Added a per-file size guard (~200 KB / ~5000 lines) and binary-file check; oversized/binary files are skipped and logged in the failures section.
- Anchor collisions in the index are resolved by appending `-2`, `-3`, etc.
- Added two more triggering examples to `idm-code-reviewer.md` and three to the new `idm-repo-reviewer.md`.
- Updated the README to reflect the actual current behavior (no longer described as a skeleton).

## 0.1_2026.04.27

- Initial scaffold: `idm-code-uplifter` skill and `idm-code-reviewer` agent skeleton.
- Review criteria in the agent are placeholder content to be replaced by the plugin owner.
