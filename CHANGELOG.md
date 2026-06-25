# Changelog

## 2026-06-10

- Consolidated the three former plugins (`idm-eng-plugin`, `idm-docs-plugin`, `idm-uplifter-plugin`) into a single plugin, `idm-standards` (v2.0). One install now provides all skills.
- Renamed the skills verb-first: for example, `eng-quality-checker` → `audit-code`. The plugin now ships `audit-code`, `fix-code`, `audit-code-exhaustive`, `audit-docs` (composing `audit-docs-structure`, `audit-personas`, and `audit-docstrings`), `audit-project`, and `fix-project`; `audit-code` routes to `audit-r-code` for R projects.
- Updated the root README and `plugins_readme.md` for the new plugin name and structure. Users on v1.x should uninstall the old three plugins and install `idm-standards`.

## 2026-05-06

- Added `idm_uplifter_plugin` (v0.2): fan-out per-file code review with parallel waves, a concurrent repo-level reviewer, resumable runs via `.uplifter_cache/`, and a synthesized top-of-report summary. See [idm_uplifter_plugin/CHANGELOG.md](idm_uplifter_plugin/CHANGELOG.md) for details.
- Updated root README and `plugins_readme.md` to list the new plugin and refresh the version numbers for the engineering (v1.3) and docs (v1.1) plugins.

## 2026-04-20

- Expanded `eng_process/public_release.md` with manager/director-facing guidance covering project tiers, quality assessment, effort estimation, the release process, and ongoing maintenance commitments.
