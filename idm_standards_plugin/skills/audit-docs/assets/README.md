# audit-docs bundled assets

These files are the **canonical source** for IDM's Vale configuration and the
reference docs templates. They live here so the `audit-docs` skill can reach
them at runtime via `$CLAUDE_PLUGIN_ROOT/skills/audit-docs/assets/` — an
installed plugin only ships the `idm_standards_plugin/` directory, so the skill
cannot read anything outside it. The repo formerly kept duplicate copies at the
repo root (`/vale.ini`, `/.github/styles/`, `/docs_templates/`); those were
removed to avoid drift, and these are now the only copies.

| Asset            | Notes                                                              |
|------------------|--------------------------------------------------------------------|
| `vale.ini`       | `StylesPath` points at the co-located `styles/` directory          |
| `styles/`        | Vale rule packages (IDM, Microsoft, write-good, Notebooks, config) |
| `docs_templates/`| Reference mkdocs/quarto project templates                          |

Edit these files directly. Documentation that points users at the Vale config
or the docs templates (e.g. `docs_guidance/style.md`, `docs_guidance/tools/`)
links to this location, so keep those references in sync if the layout changes.
Any change here is a behavior change to the `audit-docs` skill, so it counts
toward the plugin version bump and changelog — see the `update-docs-plugin` skill.
