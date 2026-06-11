---
name: audit-personas
description: Checks that project documentation is written appropriately for its target IDM personas (policy-maker, policy-influencer, model-user, model-extender, model-builder). Use when reviewing, auditing, or writing documentation for any IDM modeling project. Also use when the user mentions personas, audience appropriateness, documentation tone, or asks who a doc section is written for. Different doc sections target different personas — this skill knows the mapping and loads the relevant persona definitions to evaluate fit.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Persona documentation check

Skill version: 1.0_2026.04.13

IDM documentation targets five distinct personas, each with different technical backgrounds, needs, and decision-making contexts. Different sections of documentation serve different personas. This skill checks whether each documentation section is written appropriately for its intended audience.

## Persona-to-section mapping

| Doc section | Target personas |
|---|---|
| Docs landing page / beginning of README.md | policy-maker, policy-influencer |
| Rest of README.md | model-user, model-extender, model-builder |
| Overview, case studies, etc. | policy-influencer, model-user |
| Tutorials | model-user, model-extender, model-builder |
| User guide | model-extender, model-builder |
| API reference (docstrings) | model-extender, model-builder |

For technical projects without direct policy relevance, the docs landing page or beginning of the readme does NOT need to be accessible to policy-makers and policy-influencers, but should still be written in plain language where possible.

## Workflow

### Step 1: Identify which doc sections exist

Scan the project for documentation. Look for:

- `README.md` (split mentally into the opening/landing section vs. the rest)
- A docs site or `docs/` folder containing overviews, case studies, tutorials, user guides, API reference
- Docstrings in Python or R source files
- Any `mkdocs.yml` or `_quarto.yml` that reveals doc structure

If the user has asked about a specific section, focus there. Otherwise, check all sections that exist.

### Step 2: Load the relevant persona definitions

Before evaluating any section, read the persona file(s) for that section's target audience. The persona files are in the `idm_standards` repo:

- `docs_guidance/personas/policy-maker.md`
- `docs_guidance/personas/policy-influencer.md`
- `docs_guidance/personas/model-user.md`
- `docs_guidance/personas/model-extender.md`
- `docs_guidance/personas/model-builder.md`

If these files are not in the current repo, read them from the `idm_standards` repo at https://github.com/InstituteforDiseaseModeling/idm_standards/tree/main/docs_guidance/personas. Each persona file contains sections on who they are, what they do, their skills/tools, key needs, decision-making context, and targeted content guidance.

Pay close attention to:
- **Skills/tools** -- what technical level can you assume?
- **Key needs** -- what should the writing prioritize?
- **"For writers" / "For docs"** -- direct guidance on how to write for this persona
- **Targeted content** -- what belongs where

### Step 3: Evaluate each section against its target personas

For each doc section, read the actual content and assess it against the persona definitions. Consider these dimensions:

**Language and technical level**
- Does the vocabulary match what the target persona would understand?
- Policy-makers and policy-influencers need plain language with uncertainty framed in decision terms, not statistical terms.
- Model-users need workflow-oriented language without deep mathematical derivations.
- Model-extenders need clear API and extension-point language with realistic (not idealized) examples.
- Model-builders need architectural rationale and contribution guidance.

**Content focus**
- Does the section address what the persona actually needs to know?
- Landing pages should convey trust, applicability, and real-world policy relevance -- not implementation details.
- Tutorials should lead with workflow steps and concrete disease examples, not theory.
- User guides should show calibration and extension under realistic conditions, including sparse data.
- API reference should explain design intent, not just interface signatures.

**LMIC context**
- All personas prioritize LMIC users. Check whether the writing acknowledges infrastructure constraints (limited internet, limited HPC), data sparsity, and local relevance. This is especially important for tutorials and user guides.

**Appropriate framing of uncertainty**
- For policy-facing sections: uncertainty should be framed as decision risk, not confidence intervals.
- For technical sections: statistical language is fine but should be actionable.

### Step 4: Report findings

Produce a structured report organized by doc section. For each section:

1. **Target personas** -- who this section should serve
2. **Current fit** -- brief assessment of how well the writing matches persona needs (Good / Needs work / Missing)
3. **Specific issues** -- concrete examples of mismatches, with line references or quotes where possible
4. **Suggestions** -- actionable recommendations to improve persona fit

Keep the report concise and actionable. Prioritize the most impactful issues -- a tutorial that reads like an API reference is a bigger problem than a minor vocabulary choice.

## What good looks like per persona

### Policy-maker, policy-influencer (landing pages, overviews)
- Plain language, no jargon or code
- Frames models in terms of policy questions they can answer
- Shows real-world applications and track record
- Conveys trustworthiness and validation
- Connects outputs to programmatic decisions and investment choices

### Model-user (README body, overviews, tutorials)
- Leads with workflow, not theory
- Uses concrete disease examples and realistic data scenarios
- Step-by-step with clear checkpoints
- Explains how to interpret outputs and recognize unreliable results
- Assumes moderate scripting ability, basic Python or R

### Model-extender (README body, tutorials, user guide)
- Documents extension points and how to use them without full framework knowledge
- Includes guidance on judgment calls (estimate vs. fix to literature values)
- Shows calibration and extension with realistic (not ideal) data and policy complexity
- Addresses reproducibility of results and handoff to downstream workflows

### Model-builder (README body, tutorials, user guide, API reference)
- Explains architectural *why*, not just *what*
- Documents contribution process and standards
- Assumes strong coding and software engineering skills
- Addresses framework-level design decisions and their downstream effects

## Edge cases

- **A section targets multiple personas**: evaluate against each persona separately. The writing should serve the least technical persona in the group without being so shallow that it frustrates the more technical ones. For example, the body of README.md targets model-users, model-extenders, and model-builders -- it should be accessible to model-users while still being substantive enough for builders.
- **A section is missing entirely**: flag it. If a project has no tutorials, that is a gap for model-users, model-extenders, and model-builders.
- **Content exists but in the wrong place**: flag misplaced content. For example, API details on a landing page, or policy framing buried in a user guide.
- **Content is duplicated**: flag redundancy. For example, if the same policy framing appears in multiple places, it may be better to centralize it on the landing page and link to it from technical sections.
