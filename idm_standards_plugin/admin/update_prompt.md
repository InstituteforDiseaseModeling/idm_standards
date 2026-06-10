Your task is to update the code-audit skills of the IDM-Standards plugin (comprising the `audit-code`, `audit-r-code`, and `fix-code` skills and the scorer agents) based on updates to the engineering quality guidelines.

1. The engineering quality guidelines document ("guidelines doc") is in `$ROOT/eng_guidance/engineering_quality_guidelines.md`, where `$ROOT` is the IDM Standards root folder. Python-specific guidance is in `$ROOT/eng_guidance/2_python.md` and R-specific guidance is in `$ROOT/eng_guidance/2b_r.md`.
2. Read the guidelines doc and check for updates since the plugin was last updated (compare against the plugin changelog). 2a. If there are no updates, exit. 2b. If there are updates, make a list of these changes.
3. Bump the plugin version in `$ROOT/idm_standards_plugin/.claude-plugin/plugin.json` and the matching entry in `$ROOT/.claude-plugin/marketplace.json`, using the format `<major.minor>_<YYYY.MM.DD>` (e.g. "2.1_2026.07.01"). Note that the plugin version is independent of the guidelines doc version. Also update the "Skill version:" line near the top of each modified SKILL.md file.
4. Update the skills, agents, and any other necessary files based on the list of changes in the guidelines document.
5. Verify that every metric and tier described in the current version of the guidelines doc is covered in the scoring schemas (`audit-code/scoring-schema.yaml` and `audit-r-code/r-scoring-schema.yaml`) and agent prompts.
6. Update the changelog (`$ROOT/idm_standards_plugin/CHANGELOG.md`) with key changes made (no more than 5-10 points max, 1 or 2 is fine).
7. If the behavioral contract of the skills changed (output files, report sections, question flow), update the eval harness in `$ROOT/evals/` to match, and consider running it.
