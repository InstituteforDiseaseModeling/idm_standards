# Updates

1. The skill is too insistent on including a lockfile -- it should never suggest one for a tier 1 project, and for tier 2 or 3 it should first suggest requirements_frozen.txt instead. See https://github.com/InstituteforDiseaseModeling/idm_standards/issues/67
2. Ask the user to confirm the code tier: https://github.com/InstituteforDiseaseModeling/idm_standards/issues/66
3. Overall, the engineering instructions are stronger for Python than R. Make a new, separate skill for R engineering quality that's invoked if and only if it's an R project.
4. Write a new skill that calls both the eng-checker and the docs-audit.
5. Suggest better names for the skills/plugins.
6. Overall, the skills are too nitpicky -- in addition to asking for tier, ask the user for strictness. 1 = strict, everything you find (current behavior). 2 = not strict, only things that materially affect usage (i.e., not just stylistic or convention differences).
7. For eng issues that can't be fixed automatically, at least write down proposed solutions.