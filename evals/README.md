# Eval harness

End-to-end behavioral tests for the `idm-standards` plugin's audit and fix skills. They check that the skills *behave* as intended — not that they produce a specific number — by running them against small, deliberately-flawed fixture projects and asserting on score bounds and the presence/absence of specific recommendations.

## What it checks

| Fixture | Tier | Asserts |
| -- | -- | -- |
| `python_tier1` | 1 (library) | Scores well; flags missing CHANGELOG/CI; **never suggests a lock file** (the core item-1 rule). |
| `python_tier3` | 3 (one-off script) | Flags missing README and duplicated code; at **strictness 2** the stylistic findings disappear while the material ones remain. |
| `r_tier2` | 2 (shared R research code) | Routes to `audit-r-code` (Version line names it); flags missing tests and the renv gap; suggests **renv**, never the Python lock artifacts. |
| `python_tier3_config` | 3 (with committed config) | Ships `.claude/idm-standards.md`. The suppressed duplication finding disappears from recommendations; the missing-README finding still surfaces; the hardcoded API key still tanks `compliant` (≤3) — proving a directive **cannot** waive the hard floor. |

With `--roundtrip`, each fixture also runs **audit → fix-code → audit** and asserts CK's two acceptance criteria:

1. The overall score does not decrease after fixes are applied.
2. No per-metric score drops without a justification — i.e. the second report either holds/raises each metric or carries a "Score changes since last run" section explaining the drop (the score-reconciliation rule).

## Running

```bash
# from the repo root
make evals                      # all fixtures, audit-only
make evals-roundtrip            # all fixtures, including the fix round-trip

# or directly
python evals/run_evals.py                       # all fixtures
python evals/run_evals.py python_tier1          # one fixture
python evals/run_evals.py --roundtrip           # include round-trip
python evals/run_evals.py --cli "claude --model claude-fable-5"
```

Requires PyYAML (`pip install pyyaml`) and the `claude` CLI on PATH with the `idm-standards` plugin installed (or run from this repo as a marketplace source).

## Cost and runtime

Each audit dispatches three scorer subagents over a small project, so a single fixture audit is roughly **3–6 subagent invocations** and completes in a couple of minutes. The full audit-only suite is well under ten minutes. `--roundtrip` roughly triples that (audit + fix + re-audit per fixture) and consumes meaningfully more tokens.

Because scoring is **nondeterministic**, the assertions are deliberately loose (bounds and substring patterns). An occasional borderline failure on a tight bound is expected noise — re-run before treating it as a regression. This is why the harness is run **on demand, not in CI**.

## Adding a fixture

1. Create `fixtures/<name>/project/` with the smallest project that exercises the behavior you want to test (include a deliberate flaw or a deliberate *absence* of one).
2. Add `fixtures/<name>/expected.yaml`:
   - `project_subdir`, `language` (`python`/`r`), `tier`, `strictness`
   - `overall_score: {min, max}` and per-metric `metrics: {<name>: {min, max}}` bounds
   - `must_appear` / `must_not_appear`: case-insensitive substrings checked against the Recommendations + Proposed solutions text (the "Suppressed by config" section is excluded, so a `must_not_appear` for a config-suppressed item isn't tripped by the directive quoted there)
   - to test a user config, commit a config file into `fixtures/<name>/project/.claude/idm-standards.md` (the harness's `git add -A` commits it); assert suppression via `must_not_appear` and the hard floor via a metric bound like `compliant: {max: 3}`
   - optional `report_version_contains` (routing assertion)
   - optional `strictness2: {strictness, must_appear, must_not_appear}` for a second-pass strictness check
3. Run `python evals/run_evals.py <name>` and tune the bounds.
