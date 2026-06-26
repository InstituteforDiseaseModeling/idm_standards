# audit-docs bundled assets

**Generated — do not edit by hand.** These files are copied from the repo root
by the `update-docs-plugin` skill so the `audit-docs` skill can reach them at
runtime via `$CLAUDE_PLUGIN_ROOT/skills/audit-docs/assets/`. An installed plugin
only ships the `idm_standards_plugin/` directory, so the skill cannot read the
repo-root copies directly.

| Asset            | Source of truth        | Notes                                              |
|------------------|------------------------|----------------------------------------------------|
| `vale.ini`       | `/vale.ini`            | `StylesPath` is rewritten from `.github/styles` → `styles` |
| `styles/`        | `/.github/styles/`     | Vale rule packages (IDM, Microsoft, write-good, Notebooks, config) |
| `docs_templates/`| `/docs_templates/`     | Reference mkdocs/quarto project templates          |

To change any of these, edit the source of truth at the repo root and re-run the
`update-docs-plugin` skill.
