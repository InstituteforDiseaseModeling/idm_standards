# Public release

This document describes the requirements and procedure for making a repository public. It is written for managers and directors who are deciding whether to make a project public and what resources that decision requires.

## Why make code public?

In general, we want code to be public so the world can benefit from it. Public code:

- Amplifies IDM's scientific impact by enabling others to build on our work
- Builds trust through transparency in scientific methods
- Attracts collaborators, contributors, and feedback that improve quality
- Fulfills our mission to share knowledge for global health benefit

However, there are three main reasons why something *isn't* public:

1. It contains sensitive data or results, so is not allowed to be made public.
2. We are not confident yet that the results are correct, so it could potentially be misleading or dangerous to make it public.
3. It is neither sensitive nor dangerous, but it is of interest to so few people that making it public would create noise rather than signal.

If your project doesn't fall into any of these three categories, consider making it public.

## What quality level is required?

Quality expectations depend on the project's *tier*, which reflects its scope, intended audience, and expected lifetime. The [engineering quality guidelines](../eng_guidance/engineering_quality_guidelines.md) define three tiers:

| | Tier 1 | Tier 2 | Tier 3 |
|:--|:--|:--|:--|
| **What is it?** | Large-scale reusable library or "digital public good" (e.g., EMOD, Starsim, HPVsim) | Small-scale reusable code (e.g., calibrated country model, utility) | One-off or exploratory code (e.g., code for a paper or presentation) |
| **Expected users** | Many (>10), internal and external | Several (2–10), potentially external | Often only 1–5, typically internal |
| **Typical timeline** | >12 months | >3 months | <3 months |
| **Public by default?** | Yes | Usually | Sometimes |

Tier 1 code must meet the full set of engineering quality standards — correctness, clear structure, comprehensive documentation, testing, and safety. Tier 2 and Tier 3 requirements are progressively lighter. The full details are in the [engineering quality guidelines](../eng_guidance/engineering_quality_guidelines.md).

Regardless of tier, **all public code must be:**

- **Correct**: The code does what it claims to do. Peer review and colleague second opinions strengthen this.
- **Tested**: Appropriate test coverage for the tier. For non-trivial code, "it looked right when I ran it" is not sufficient.
- **Documented**: Every public repo needs at minimum a README explaining purpose, installation, and basic usage.
- **Safe**: *Under no circumstances* make a repo public if it contains sensitive data, personally identifiable information (PII), API keys, or other secrets.

## How is quality assessed?

Before a project goes public, the team should:

1. **Automated review**: Use the [IDM Engineering Plugin](https://github.com/institutefordiseasemodeling/idm_standards/tree/main/idm_eng_plugin) — a Claude Code plugin built directly from the engineering guidelines — to score the project and generate a prioritized list of gaps and improvements.
2. **Peer code review**: At least one engineer who did not write the code reviews it against the [engineering quality guidelines](../eng_guidance/engineering_quality_guidelines.md).
3. **Documentation review**: The content team reviews docs for clarity and completeness.
4. **Stakeholder sign-off**: All stakeholders confirm the project meets its success criteria.
5. **History scan**: Verify the full commit history (not just the current state) contains no secrets, API keys, or sensitive data that were accidentally committed and later deleted. If found, these must be excised from history before the repo is made public.

## What is the effort to reach public-release quality?

Effort depends heavily on the project's current state and target tier. Rough guidance:

- **Tier 3 → public**: If the code is already correct and has a README, the main effort is typically documenting and removing any sensitive content. *Estimate: 0.5–2 days.*
- **Tier 2 → public**: Typically requires adding tests, improving documentation (README + example scripts or tutorial), ensuring reproducibility (pinned dependencies), and passing a code review. *Estimate: 2–5 days for a project in decent shape; more if significant gaps exist.*
- **Tier 1 → public**: Full Tier 1 quality is a significant ongoing investment. Projects intended for public Tier 1 release should be designed to that standard from the start; retrofitting rarely is cost-effective. *Estimate: Weeks to months depending on gaps.*

The [IDM Engineering Plugin](https://github.com/institutefordiseasemodeling/idm_standards/tree/main/idm_eng_plugin) can provide a more specific estimate based on an actual assessment of the project.

## The release process

Once a project is ready to go public, follow the [launch checklist](processes.md) from the engineering processes guide:

1. All stakeholders confirm the project meets its success criteria.
2. Full codebase is reviewed by an engineer and AI tool against the quality guidelines.
3. Docs are reviewed by the content team for clarity and completeness.
4. Ensure the `main` branch is the primary entry point (not a long-lived feature branch).
5. Publish to PyPI or CRAN if the project is a reusable library.
6. Optionally pair with an AI tool (plugin, MCP server, or chatbot) to make the project more accessible.
7. Optionally pair with a dedicated documentation website.
8. Announce via social media, websites, and partner channels as appropriate.

## Ongoing maintenance commitments

Making a project public is a commitment, not a one-time action. Public repositories have users who depend on them. Plan for:

- **Technical debt**: Proactively managed to keep the codebase healthy over time.
- **Releases**: Frequent releases, especially for bug fixes.
- **Support**: User questions and bug reports addressed within 24 hours.
- **Docs sync**: Documentation kept in sync with code.

For Tier 1 projects, this typically requires dedicated engineering time on an ongoing basis. For Tier 2 and Tier 3 projects, maintenance can be lighter, but should still be explicitly planned and resourced before release.
