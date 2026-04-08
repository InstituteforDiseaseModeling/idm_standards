# Model builder persona

People who design and implement new disease modeling frameworks and core methods.

## Who they are

Advanced modelers and software engineers (often in IDM or academic teams) who create flexible, extensible frameworks others can build on. While this persona is common within IDM, only a small percentage of people within the global health field are model builders. 

## What they do

Architect model structure, implement core algorithms, define parameters, and set standards for code quality and interoperability. They often own the GitHub repo and contribute major new modules and capabilities. 

## Skills/tools

Advanced epidemiology/statistics and strong coding and software engineering (testing, packaging, repo hygiene), comfort with high-performance compute and complex workflows. Model builders
have strong programming skills but may lack a detailed understanding of the mechanisms of disease transmission or policy implementation challenges. 

## Key needs

Framework-level documentation, clear architecture diagrams, contribution guides, and stable infrastructure for building, testing, and releasing models as reusable assets to enable the broader global health modeling community. 

## Decision-making context

Model builders make architectural decisions that affect everyone downstream: what abstractions to expose, which behaviors to hard-code versus make configurable, how to structure APIs so that model extenders can work with them without needing to understand the full framework internals. They are also responsible for quality and stability — a change merged by a model builder may affect dozens of downstream users and extenders who had no visibility into it.

Given IDM's focus on leaving reusable global public good assets, model builders are effectively designing for handoff: frameworks need to be legible and maintainable by people who weren't part of the original team.

**For code:** Consider whether your API decisions require deep framework knowledge to use correctly. Prefer extension points that are explicit and documented over patterns that rely on internal conventions. Assume future maintainers won't have context you take for granted. When adding compute-intensive features, consider whether they can run within LMIC infrastructure constraints (limited HPC, slow or unreliable internet).

**For docs:** Prioritize documenting the *why* behind architectural decisions, not just the *what*. A model builder reading architecture docs needs to understand design intent well enough to make consistent decisions — not just replicate existing patterns. Contribution guides should address how to evaluate whether a change is backward-compatible and what the review process expects.

## Targeted content

Target the software documentation for the core packages of modeling frameworks and the GitHub landing pages for modeling frameworks primarily to the needs of model builders. Specifically, describe the software architecture and how to build new disease models using the core package functionality. 