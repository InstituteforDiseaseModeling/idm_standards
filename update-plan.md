# Update plan

Plan for implementing the seven items in `updates.md` (2026-06-10, revised after CK review). GitHub issues #66 ("Eng plugin should ask for tier confirmation") and #67 ("Update guidance on lockfile — too insistent") have no further detail, so `updates.md` is the spec.

Reminder of tier definitions (per `eng_guidance/engineering_quality_guidelines.md` and `eng-quality-checker/SKILL.md:28-31`): **Tier 1 = library/digital public good, Tier 2 = small shared project, Tier 3 = one-off/exploratory code.**

> File paths below refer to where content lives **today**; the structural merge (sequencing step 2) moves everything into the single plugin before the behavioral edits land.

## Decisions (per CK review)

1. **Lock artifacts**: keep **`requirements_locked.txt`** (via `pip freeze`) as the simple option, and add **`pylock.toml`** (via `pip lock`, PEP 751 — supported by pip ≥25.1 and exportable from uv) as the modern/advanced option. For Tier 2/3, ask the user which they want — `requirements_locked.txt` (recommended default for simple/Tier 3 projects), `pylock.toml` (recommended for more advanced/Tier 2 projects), or **None** (a valid choice that gets recorded in `code_audit.md` so re-runs don't nag). Tier 1 projects are never told to add one, but a `pylock.toml` is fine if present (no penalty either way).
2. **Strictness semantics**: strictness 2 affects **both** scores and recommendations — agents neither dock points nor write recommendations for purely stylistic/convention issues. Strictness is recorded in the report header so scores from different strictness levels aren't compared blindly.
3. **Renames are applied now**, not just proposed: this release is a breaking **2.0**, so the new verb-first names (table in item 5) ship with it.
4. **Plugin architecture**: merge all three plugins into **one plugin** so users install one thing and get the full suite, while every skill remains individually invocable (see item 5 for details and the subagent question).
5. **R guidance**: don't write a standalone R style guide. Mirror the Python model — `2_python.md` is "Google style guide + IDM deltas", so add a thin `eng_guidance/` R page that is "Tidyverse style guide (https://style.tidyverse.org/) + IDM deltas", where the deltas are engineering practice (renv, testthat, targets/here, r-lib/actions CI) rather than style, since IDM-specific R *style* conventions are likely nil. The R checker then scores against Tidyverse style plus the same language-neutral IDM tier metrics (usability, flexibility, reproducibility, testing) with R-specific evidence. If IDM-specific R conventions emerge later, the page grows.
6. **Audit→fix chaining**: every audit skill ends by asking whether to immediately invoke its fix counterpart — `audit-code`/`audit-r-code` → `fix-code`, `audit-project` → `fix-project`, `audit-docs` → `fix-project` (docs-only). Defaults to "no" in non-interactive contexts so headless/eval runs aren't blocked.
7. **Output files are normalized to match the skill names**:

   | Skill | Output file(s) |
   | -- | -- |
   | `audit-code` / `audit-r-code` | `code_audit.md` (was `engineering_score.md`) |
   | `audit-docs` | `docs_audit.md` (unchanged, now pinned to the project dir) |
   | `audit-project` | `project_audit.md` (combined summary) |
   | `audit-code-exhaustive` | `code_audit_exhaustive.md` (was `uplifter_report.md`); cache dir `.audit_cache/` (was `.uplifter_cache/`) |

   The fixers create no files of their own: they read the audit reports directly and update each report's **Proposed solutions** subsection in place (item 7). For backward compatibility, `fix-code`/`fix-project` fall back to reading `engineering_score.md` if `code_audit.md` is absent.
8. **Score consistency across re-runs**: scoring agents always score fresh — the prior report is *not* shown to them, so old findings don't anchor new ones. But before writing the report, the skill compares the new scores against the prior report (if present): any metric that went *down* must be justified in a **Score changes since last run** note, citing either (a) what actually got worse (concrete evidence, e.g. from `git log`/`git diff` since the prior report's date), or (b) what the previous run missed (the specific finding). If neither can be substantiated, the drop is stochastic noise — retain the prior score (this is just the existing "only concrete, observable problems" principle applied across runs). Users were seeing unexplained score drops after applying fixes far more often than stochasticity justifies; this is the fix.

---

## Item 1 — Lockfile guidance (issue #67)

**Rule to encode**:

- **Tier 1 (libraries)**: never suggest a lock artifact — loose deps in `pyproject.toml` (with `>=` bounds only where genuinely needed) are correct. A `pylock.toml` is optional and acceptable if present; don't penalize its presence or absence.
- **Tier 2/3 where reproducibility matters**: offer a choice and ask the user — `pip freeze > requirements_locked.txt` (simple; the default suggestion for Tier 3), `pip lock` → `pylock.toml` (advanced; the default suggestion for Tier 2), or **None**. The *checker* presents the options in its recommendation without insisting; the *fixer* asks via AskUserQuestion before implementing. A "None" answer is recorded in `code_audit.md`'s Proposed solutions section (see item 7) and respected on re-runs — no re-nagging and no score docking for a recorded opt-out (the existing user-instruction mechanism at `eng-quality-checker/SKILL.md:35` covers this, and the audit re-reads the prior report's recorded decisions before regenerating it).
- **R**: `renv.lock` remains the standard at Tier 2/3; a dated Posit Package Manager snapshot is the lightweight alternative. The locked/pylock choice is Python-specific.

**Files to change** (guidance first, then propagate to plugin per `idm_eng_plugin/admin/update_prompt.md`):

- `eng_guidance/2_python.md:395-400` — keep `requirements_locked.txt`; add `pip lock`/`pylock.toml` (PEP 751) to the options list; add explicit tier framing (never for Tier 1; user's choice of locked/pylock/None for Tier 2/3).
- `eng_guidance/engineering_quality_guidelines.md:113` — the lock-file item is currently tagged `[1,2,3]`; carve out Tier 1 (deps specified, no lock artifact expected) and rewrite Tier 2/3 as the locked/pylock/None choice.
- `idm_eng_plugin/agents/safety-scorer.md:78-87` — rewrite the dependency/lockfile checklist with the tier rules (add `pylock.toml` to the artifacts checked); line 123's 10-anchor ("version pins on key deps") must drop the pin requirement for Tier 1.
- `idm_eng_plugin/skills/eng-quality-checker/scoring-schema.yaml:126` — **fixes an internal contradiction**: the Tier 1 `reproducible` 10-anchor requires "version pins (>=) on key deps" while `safety-scorer.md:82` says don't penalize Tier 1 for missing pins. Relax the schema anchor. Also clean up lines 199-206 (Tier 2 anchors) to name the locked/pylock options, and stop calling `>=` bounds "pins" (terminology cleanup).
- `idm_eng_plugin/skills/eng-quality-checker/SKILL.md:144` (safety-scorer prompt template) — same tier framing.
- `idm_eng_plugin/skills/eng-quality-fixer/SKILL.md:43-44,193` — the example fix "Add version pinning to requirements.txt" becomes the locked/pylock/None question for Tier 2/3, and nothing for Tier 1.
- `idm_uplifter_plugin/agents/idm-repo-reviewer.md:108` — "environment/lock file … for non-library code" gets the same softening.

## Item 2 — Confirm the code tier (issue #66)

Current behavior (`eng-quality-checker/SKILL.md:26`): tier is prompted for only if not supplied, and never inferred or confirmed.

**Change**: In Step 1, if tier was *not* passed as an explicit argument, do a quick inspection (published package + CI → suggest Tier 1; tests + multiple contributors/README → Tier 2; scripts/notebooks only → Tier 3) and confirm with the user via **AskUserQuestion**, presenting the inferred tier as the recommended option with the three definitions as choices. An explicitly passed tier counts as confirmation — don't re-ask. Honor a "tier already confirmed" instruction so `audit-project` (item 4) can ask once and pass it through without double-prompting.

**Files**: `eng-quality-checker/SKILL.md` (→ `audit-code`) Step 1 (+ frontmatter `allowed-tools` line 5 gains `AskUserQuestion`, and `Skill` for the audit→fix chaining); `idm_eng_plugin/README.md` usage examples. Ask the tier and strictness (item 6) questions in a single AskUserQuestion call.

## Item 3 — Separate R engineering-quality skill

**New skill**: **`audit-r-code`** (named per item 5) with its own `SKILL.md` and `r-scoring-schema.yaml`. Reuse the three existing scorer agents — they already accept rubrics via the dispatch prompt, so the R skill injects R-specific rubrics rather than duplicating agents.

**Routing** ("invoked if and only if it's an R project"): add a language-detection step to *both* checkers — `DESCRIPTION`/`renv.lock`/majority `*.R`-files → R skill; otherwise Python skill. For genuinely mixed repos (both languages ≥25% of source files), ask the user which to run (or both). The Python checker's SKILL.md gets a one-line redirect ("if the project is R, invoke audit-r-code instead"), and its thin R mentions (`SKILL.md:71-72,143,147,314-315`) are pruned to point at the R skill.

**Scoring basis** (per decision 5): Tidyverse style guide for style (exempted at strictness 2 like all style findings), plus the language-neutral IDM tier metrics with R-specific evidence:

- *Tier 3 (one-off)*: git repo; README with purpose + entry point; deps discoverable (`library()` calls at top); no `setwd()`/`rm(list=ls())`/absolute paths (grep-checkable); `set.seed()` where randomness matters; no secrets (`.Renviron` gitignored).
- *Tier 2 (shared research code)*: + `renv` healthy (`renv.lock` + `.Rprofile` + `renv/` committed, `renv::status()` clean) *or* `DESCRIPTION` + dated P3M snapshot; functions factored into `R/`; `here::here()` for paths (or a `targets` pipeline); some `testthat` tests; Tidyverse style (`lintr`, Air or styler); LICENSE; raw vs derived data separated.
- *Tier 1 (package)*: + standard skeleton (`DESCRIPTION` with Imports-not-Depends, roxygen2-generated `NAMESPACE`, `man/`, `tests/testthat/` edition 3, `vignettes/`, `NEWS.md`); `R CMD check` 0/0/0; CI via `r-lib/actions@v2` (R-CMD-check, coverage, lint, pkgdown); pkgdown site; CRAN (or r-universe) publication; no `library()` calls inside `R/`; flag `packrat/` as deprecated (suggest `renv::migrate()`).

(External R tier checklists number tiers in the opposite direction — these are already transposed to IDM ordering.)

**Fixer**: keep the single `fix-code` (it already has roxygen2 templates and an "adapt to R" note); extend it with R scaffolds (testthat file, DESCRIPTION) rather than forking.

**Guidance**: add the thin Tidyverse-referencing R page to `eng_guidance/` (decision 5) so the schema derives from the guidelines doc.

## Item 4 — `audit-project` and `fix-project`

**New skill `audit-project`** (combined audits). Workflow:

1. Parse project path/GitHub URL; clone **once** if a URL (audit-docs has no URL support — audit-project passes the local path to everything it invokes).
2. Ask the user **which audits to run** — "Eng audit, docs audit, or both?" (default: both) — together with tier and strictness, in one AskUserQuestion call. Optionally offer `audit-code-exhaustive` (the per-file deep review) as an add-on choice, with a note that it's slower.
3. Invoke the selected skills via the Skill tool (`audit-code`, routing to `audit-r-code` if the project is R; `audit-docs`), passing tier/strictness with "already confirmed — don't re-prompt". With the merged plugin (item 5) there's no cross-plugin dependency to degrade around.
4. Write a short combined summary to `project_audit.md` that links the component reports (`code_audit.md`, `docs_audit.md`) and reconciles overlap (both check README/LICENSE/docstrings/CHANGELOG — cross-reference rather than duplicate).
5. End by asking whether to invoke `fix-project` now (decision 6).

**New skill `fix-project`** (combined fixes): the general fixer orchestrator. It reads whichever audit reports exist in the project (`code_audit.md`, `docs_audit.md`, `code_audit_exhaustive.md`), confirms with the user which to act on, then dispatches `fix-code` for the code report and implements docs-audit recommendations directly (the docs plugin has no fixer today; if a dedicated `fix-docs` skill is added later, it slots in here). Like `fix-code`, it presents its plan before changing anything and records skipped/unfixable items in each report's Proposed solutions subsection (item 7).

**Audit→fix chaining** (decision 6): every audit skill ends with an AskUserQuestion offering to run its fix counterpart immediately — `audit-code`/`audit-r-code` → `fix-code`; `audit-project` → `fix-project`; `audit-docs` → `fix-project` (docs-only). The offer is skipped in non-interactive contexts and when the audit was invoked *by* another skill (`audit-project` already handles the question itself). Audit skills gain `Skill` in their `allowed-tools` to support this.

**Supporting patches to `idm_docs_plugin/skills/docs_audit/SKILL.md`** (→ `audit-docs`): pin its `docs_audit.md` report to the *project* directory (currently unspecified at line 110, vs the code report which is explicitly project-dir); accept tier/strictness as structured instructions; fix the wrong cross-references `idm_docs_plugin:diataxis/personas/python-docstrings` at lines 75/83/92 (stale namespace — and these change again with the merge and renames anyway).

## Item 5 — Renames and single-plugin merge

Applied now as part of 2.0 (decision 3). Skill names are verb-first and chosen to read well standalone, since skills are typically invoked directly rather than with the plugin prefix:

| Current | New name |
| -- | -- |
| `eng-quality-checker` | `audit-code` |
| R checker (new) | `audit-r-code` |
| `eng-quality-fixer` | `fix-code` |
| combined skills (new) | `audit-project`; `fix-project` |
| `docs_audit` | `audit-docs` |
| `idm-code-uplifter` (uplifter plugin) | `audit-code-exhaustive` |
| `diataxis`, `personas`, `python-docstrings` | `audit-diataxis`, `audit-personas`, `audit-docstrings` |

**Merge architecture** (decision 4): combine all three plugins into **one plugin** so one install gets the full suite, with every skill still individually invocable.

- **Plugin name**: recommend **`idm-standards`** (matches the repo and marketplace — one name to remember; install is `idm-standards@idm-standards`). Alternative if that reads redundantly: `idm-tools`. Directory: `idm_standards_plugin/`.
- **Subagents: yes, this works.** Agents are plugin-level resources (both `idm_eng_plugin/agents/` and `idm_uplifter_plugin/agents/` already follow this layout), so all five agent files (`quality-scorer`, `safety-scorer`, `usability-scorer`, `idm-code-reviewer`, `idm-repo-reviewer`) move into the merged plugin's `agents/` directory. Skills reference them by namespaced agent type, so references update from `idm-uplifter-plugin:idm-code-reviewer` to `idm-standards:idm-code-reviewer` — a find/replace in the uplifter SKILL.md, nothing structural.
- **What moves**: all 7 existing skills (renamed per the table) + 3 new ones (`audit-r-code`, `audit-project`, `fix-project`) into `skills/`; the eng `admin/` folder comes along (its prompts updated for the new layout); the three CHANGELOGs are concatenated into one (with per-plugin history preserved under headings); `marketplace.json` shrinks to a single entry; the three plugin READMEs merge into one.
- **Migration**: the old plugin names disappear from the marketplace. Add a migration note to the repo README/`plugins_readme.md` ("the three former plugins are now one — uninstall old, install `idm-standards`"). Also recommend deprecating the legacy **project-improver** plugin in the starsim marketplace, which duplicates the eng plugin (the report rename to `code_audit.md` conveniently removes their `engineering_score.md` filename collision).
- **Cross-reference sweep** (rename + merge together): `eng-quality-fixer/SKILL.md:3,17,202`, `docs_audit/SKILL.md:75,83,92` (which also invokes the three renamed sub-skills `audit-diataxis`/`audit-personas`/`audit-docstrings`), `plugins_readme.md`, plugin READMEs, `.claude/skills/update-docs-plugin/SKILL.md` (it syncs `docs_guidance/` → docs plugin; must point at the merged plugin), `admin/update_prompt.md`, `eng_guidance/engineering_quality_guidelines.md:178`, and all skill `description:` frontmatter mentioning old invocation paths.

## Item 6 — Strictness setting

Add a second user setting alongside tier: **strictness 1 = strict** (current behavior, report everything) / **strictness 2 = material only** (skip findings that are purely stylistic or convention-based and don't materially affect correctness, usability, or safety).

- `eng-quality-checker/SKILL.md` (→ `audit-code`): frontmatter `argument-hint` becomes `[project] [tier] [strictness]`; Step 1 asks it together with tier (default 1 in non-interactive contexts); Step 3 forwards strictness into all three agent prompt templates; Step 7 records `**Strictness**: <n>` in the `code_audit.md` header.
- All three scorer agents: add a strictness rule next to the existing "General scoring principle" — at strictness 2, do not dock points or emit recommendations for stylistic items (style-guide adherence, naming conventions, linter configs, comment density); material issues (bugs, missing tests for key logic, broken installs, missing LICENSE, secrets, irreproducibility) are unaffected.
- `eng-quality-fixer/SKILL.md` (→ `fix-code`): read strictness from the report header and respect it when planning fixes.
- `audit-docs` and `audit-project` accept the same parameter ("the skills are too nitpicky" is plural); `audit-code-exhaustive` maps strictness 2 → report only CRITICAL/HIGH severities.

## Item 7 — Proposed solutions for unfixable issues

The checker already writes a recommendation for every sub-10 metric with an `automated: yes/no` tag — the gap is depth and fixer-side persistence:

- `audit-code` Step 6: for `automated: no` recommendations, require a brief **proposed solution** (concrete approach/steps/outline, not just a title).
- `fix-code` (and `fix-project`) Steps 2/5: items classified "Requires human input" or "Cannot implement" are written into a **Proposed solutions** subsection of the audit report itself (`code_audit.md`; docs items go in `docs_audit.md`) — for each: the issue, a concrete proposed approach (including code sketches/outlines where sensible), effort, and why it can't be automated. The fixers read the audit reports directly; no separate solutions files. User decisions also land in this subsection (e.g. lockfile choice "None" from item 1). Audit re-runs regenerate the report — acceptable by design — but the audit reads the prior report first and carries forward recorded user decisions and still-relevant proposed solutions so they aren't lost or re-nagged.
- Reading the prior report also powers the score-reconciliation step (decision 8): in `audit-code`'s SKILL.md this lands as a new step between computing scores (Step 4) and writing the report (Step 7) — diff per-metric scores against the prior report, justify every decrease with (a) concrete regression evidence or (b) a specific previously-missed finding, and revert unjustifiable drops; the justifications go in a **Score changes since last run** note in the report. The scorer agents themselves never see the prior report.

---

## Cross-cutting work

**Versions & changelogs**: the merged plugin ships as **`2.0_2026.06.10`** (set in its `plugin.json`, the single `marketplace.json` entry, and each SKILL.md version line). The merged CHANGELOG gets a 2.0 entry covering: the merge + renames, output-file renames (`engineering_score.md` → `code_audit.md`, `uplifter_report.md` → `code_audit_exhaustive.md`), lockfile guidance, tier confirmation, strictness, R skill, `audit-project`/`fix-project`, audit→fix chaining, the Proposed solutions report section, score reconciliation across re-runs. The `eng_guidance/engineering_quality_guidelines.md` version line bumps with the lockfile/R changes. `admin/update_prompt.md` is updated for the merged layout, decoupled from the guidelines-doc version (they've already drifted: guidelines 1.2 vs plugin 1.3), and its wrong CHANGELOG path fixed (`$ROOT/idm-eng-plugin/` → the merged plugin dir).

**Latent bugs to fix while in these files** (all found during review):

- `scoring-schema.yaml:126` Tier 1 pin-requirement contradiction (covered in item 1).
- `docs_audit/SKILL.md:75,83,92` stale namespace cross-references (covered in items 4/5).
- `eng-quality-fixer/SKILL.md:144`: `build-backend = "setuptools.backends.legacy:build"` is not a valid backend — should be `setuptools.build_meta`.
- `admin/update_prompt.md` wrong CHANGELOG path (above).

**Repo hygiene**: don't sweep the untracked merge artifacts (`docs_guidance/topic-types/notebook.ipynb.orig`, `docs_templates/mkdocs_template/README.md.orig`) into commits; delete them separately. `updates.md` and this plan are working files — decide whether they're committed or removed before the PR merges.

## Eval harness

New: an `evals/` directory at the repo root so skill behavior is testable rather than spot-checked.

- **Fixtures**: small deliberately-flawed sample projects — at minimum one Python Tier 1 (library-shaped, no lock artifact — must NOT be told to add one), one Python Tier 3 (script with seeded randomness, missing README sections, a stylistic-only flaw to exercise strictness), and one R Tier 2 (renv project with a failing `renv::status()` or missing tests). Each fixture ships with an `expected.yaml` (tier, score bounds, must-appear and must-NOT-appear recommendation patterns).
- **Runner** (`evals/run_evals.py`): copies a fixture to a temp dir, invokes the skill headlessly (`claude -p "/idm-standards:audit-code <dir> <tier> <strictness>" --permission-mode acceptEdits`), parses `code_audit.md` (header fields + per-metric scores + recommendation titles), and asserts against `expected.yaml`. Headless runs take the non-interactive defaults (strictness 1, no audit→fix chaining), so the runner invokes `fix-code` explicitly for the round-trip.
- **Round-trip check** (CK's two acceptance criteria): run `audit-code` → `fix-code` (auto-approve) → `audit-code` again, then assert **(a)** the overall score did not decrease (and strictly increased where automatable fixes existed), and **(b)** no recommendation that was implemented reappears — e.g. if `performant` was 9/10 with one identified issue and the fix was applied, `performant` must now be 10/10. (b) leans on the existing scoring principle "if no specific improvements can be identified, score 10/10" — the eval makes that principle enforceable. Also assert the score-reconciliation rule (decision 8): any per-metric decrease in the second report must come with a "Score changes since last run" justification; an unexplained drop is an eval failure.
- **Strictness/lockfile assertions**: strictness-2 reports contain no stylistic recommendations; Tier 1 reports never mention lock artifacts; a recorded "None" lockfile choice is not re-raised on a second run.
- **Practicalities**: LLM-driven scoring is nondeterministic and each run costs real tokens — assert on bounds and presence/absence patterns rather than exact scores, run on demand (a `make evals` target) rather than in CI, and document expected runtime/cost in `evals/README.md`.

## Suggested sequencing (on `usability-updates`, PR to `main`)

1. **Guidance first** (source of truth): lockfile updates to `2_python.md` + `engineering_quality_guidelines.md`; thin R page referencing the Tidyverse style guide (items 1, 3-guidance).
2. **Structural merge + renames** (item 5): create the merged plugin directory, move skills/agents/admin, apply new skill names, update `marketplace.json`, READMEs, CHANGELOG, and all cross-references. Do this *before* the behavioral edits so they land once, in final paths.
3. **Eng core behavior**: items 1 (propagation), 2, 6, 7 — one coherent change to checker/fixer/agents/schema, plus the audit→fix chaining prompt.
4. **R skill** (item 3): `audit-r-code` + R scoring schema + language routing.
5. **`audit-project` + `fix-project`** (item 4) + audit-docs patches.
6. **Uplifter touch-up**: lockfile softening + strictness mapping in `audit-code-exhaustive`; rename its outputs (`uplifter_report.md` → `code_audit_exhaustive.md`, `.uplifter_cache/` → `.audit_cache/`).
7. **Eval harness**: fixtures + runner + round-trip checks; run it against the finished skills and fix what it catches.
8. **Final sweep**: `plugins_readme.md`, repo README migration note, version stamps, changelog entry.
