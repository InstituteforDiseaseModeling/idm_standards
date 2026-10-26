# Findings: the shared format for code-audit agents

Every code-audit agent (the quality, usability and safety scorers, and the file reviewers at max effort) reports what it found as a list of **findings** in this format. Scores are derived from findings, recommendations are written from findings, and `fix-code` works from findings, so a finding has to be specific enough that someone could fix it without redoing the audit.

## Format

Return findings as YAML:

```yaml
findings:
  - id: Q3                       # scorer prefix (Q quality, U usability, S safety, F file review) + number
    criterion: correct.2         # an ID from reference/criteria.yaml
    severity: high               # critical | high | medium | low (see below)
    location: sim/model.py:42-68 # path relative to the project root, with lines where possible; "project" for project-wide findings
    problem: "`step()` adds births before deaths, so deaths are drawn from a population that includes newborns; mortality is overstated by ~2% per year."
    fix: "Apply deaths before births, or draw deaths from `alive & ~newborn`. Add a test that a closed population with zero births keeps the expected mortality rate."
    effort: quick                # quick (minutes) | medium (hours) | large (days)
    automatable: yes             # yes if an AI agent could make the fix without domain input
```

- **problem** states what is wrong and why it matters, citing the evidence (the code, the test output, the missing file). Not "error handling could be improved", but which input fails and how.
- **fix** is a concrete change. If the fix needs domain knowledge (e.g. the correct parameter value), say what decision is needed.
- One finding per distinct problem. A pattern repeated across many places is one finding with all locations listed (or the first few plus a count), not dozens of copies.
- Only report concrete, observable problems, not theoretical ones. "This might be slow for large inputs" is not a finding unless the code is actually run on large inputs.

## Severity

- **critical**: the code should not be used until this is fixed. Exposed secrets or credentials, committed PII or proprietary data used without permission, license violations, or a bug that makes key scientific results wrong. A critical finding under `correct` or `compliant` fails the audit (that metric scores 0).
- **high**: a likely bug, a security problem, or a major gap for the tier (e.g. a Tier 1 library with no tests or CI).
- **medium**: materially hurts usability, readability or maintainability.
- **low**: minor; nice to fix.

## Strictness

- **Strictness 1** (default): report everything.
- **Strictness 2** (material only): do not report or penalize purely stylistic or convention findings (style-guide adherence, naming conventions, linter configuration, comment density, formatting, documentation phrasing). Report only what materially affects correctness, usability or safety.

## From findings to scores

- Score each applicable metric as an integer 0–10 using the tier's rubric from the scoring schema, and list the IDs of the findings that justify it.
- A score below 10 must be justified by at least one finding for that metric; if you cannot name a specific improvement, the score is 10.
- Criteria that don't apply at the audited tier (see `tiers` in `criteria.yaml`) are neither scored nor reported. Metrics whose rubric is "N/A" at this tier (Tier 3: `powerful`, `accessible`) are reported as `N/A`, not scored.

## Config directives and the hard floor

Respect the exclusions given in your prompt (project config directives, recorded user decisions, invocation instructions): don't report or penalize what they cover. The one exception is the **hard floor** defined in `reference/user-config.md`: a critical finding is always reported and scored, even if a directive seems to cover it; mark it `reported despite config directive`.

## Coverage

Every agent also returns `files_read`: the project-relative paths of the files it read in full. This is how the report states its coverage honestly. Don't list a file you only grepped or skimmed.
