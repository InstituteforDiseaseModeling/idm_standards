# Considerations for Public Release

Christopher Lorton, Cliff Kerr, Claude - April 2026

This document describes the requirements and process for making a project public. It is intended for managers and directors considering making a project public and assessing what resources are required.

Goals:
- provide guidance on when to make projects public (and when _not_ to)
- define quality expectations for public projects
- highlight resources for assessing and addressing quality gaps
- estimate team size and time required for public release

## Public/private considerations

We want to make a project/repository public if it meets one or more of the following criteria:

- It amplifies IDM's scientific impact by enabling others to build on our work
- It builds trust through transparency in scientific methods
- It attracts collaborators, contributors, and feedback that improve quality
- It fulfills our mission to share knowledge for global health benefit

There are three main reasons why a project _is not_ made public:

1. It contains sensitive data or results, so it is not allowed to be made public.
2. We are not confident yet that the results are correct, so it could potentially be misleading or dangerous to make it public.
3. It is neither sensitive nor dangerous, but it is of interest to so few people that making it public would create noise rather than signal.

If a project meets one or more of these criteria and none of the disqualifying conditions, it should be considered for public release.

## Quality expectations

Quality expectations depend on the project's _tier_, which reflects its scope, intended audience, and expected lifetime. The [engineering quality guidelines](../eng_guidance/engineering_quality_guidelines.md) define the three tiers. Briefly, they are:

**Tier 1**: large-scale reusable library or “digital public good” (e.g., EMOD, Starsim, HPVSim) with many (10+) users, internal and external<br>
**Tier 2**: small-scale reusable code (e.g., calibrated country model, utility) with several (2-10) users, potentially external<br>
**Tier 3**: one-off or exploratory code (e.g., code for a paper or presentation) with a few (1-5) users, primarily internal

Tier 1 should meet the full set of engineering standards — correctness, structure, documentation, testing, and safety — with any exceptions clearly justified. Tier 2 and Tier 3 requirements are progressively lighter. The full details are in the [engineering quality guidelines](../eng_guidance/engineering_quality_guidelines.md).

Regardless of tier, **all public code must be:**

- **Correct**: The code does what it claims to do, supported by peer review. For modeling code, this includes reproducibility of key results and validation against known benchmarks where applicable.
- **Tested**: Appropriate test coverage for the tier. Tier 1 and Tier 2 require automated tests; Tier 3 may rely on usage-based validation where sufficient. For non-trivial code, "it looked right when I ran it" is not acceptable.
- **Documented**: Every public repository must include a README covering purpose, installation, and basic usage.
- **Safe**: *Under no circumstances* make a repository public if it contains sensitive data, personally identifiable information (PII), API keys, or other secrets.
- **Licensed**: By default, repositories use the [MIT License](https://opensource.org/license/MIT).

## Quality assessments

Before a project goes public, the team should perform the following actions to assess the state of a project with respect to the quality expectations and identify any gaps:

1. **Run automated review** (all tiers): Use the [IDM Engineering Plugin](https://github.com/institutefordiseasemodeling/idm_standards/tree/main/idm_eng_plugin) — a Claude Code plugin built directly from the engineering guidelines — to score the project and generate a prioritized list of gaps and improvements. _Estimate: 1 person, 1 hour._
2. **Perform peer code review** (T1 and T2, recommended for T3): At least one engineer who did not write the code reviews it against the [engineering quality guidelines](../eng_guidance/engineering_quality_guidelines.md). _Estimate: 1 person, 1 day – 1+ weeks._
3. **Perform documentation review** (T1 and T2, recommended for T3): The content team reviews docs for clarity and completeness. _Estimate: 1 person, 1 day – 1+ weeks._
4. **Get stakeholder sign-off**: All stakeholders confirm the project meets its success criteria. _Estimate: 1 day – 1 week depending on number of stakeholders and project size._
5. **Run history scan**: Verify the full commit history (not just the current state) contains no secrets, API keys, or sensitive data that were accidentally committed and later deleted. If found, these must be excised from history before the repository is made public. _Estimate: 1 person, 1 hour._

## Time and team size estimates for public release quality assurance

Effort depends on the project’s current state and target tier:

- **Tier 3 → public**: If the code is already correct and has a README, the main effort is typically documenting and removing any sensitive content. _Estimate: 1 person, 0.5–2 days._
- **Tier 2 → public**: Typically requires tests, improved documentation (README + examples), and reproducibility (pinned dependencies), and code review. _Estimate: several people, 2–5 days for a project in decent shape; more if significant gaps exist._
- **Tier 1 → public**: Tier 1 quality is a significant ongoing investment. Projects intended for public Tier 1 release should be designed to that standard from the start; retrofitting rarely is cost-effective. _Estimate: multi-person team, weeks to months._

The [IDM Engineering Plugin](https://github.com/institutefordiseasemodeling/idm_standards/tree/main/idm_eng_plugin) can provide a more specific estimate based on an actual assessment of the project.

## The release process

Once a project is ready to go public, follow the [launch checklist](processes.md) from the engineering processes guide:

1. Stakeholders confirm the project meets its success criteria.<br>_Estimate: “box checked” based on quality assessment (QA) above._
2. Quality assessment steps are completed (see above).<br>_Estimate: “box checked” based on the QA work._
3.	Ensure the main branch is the primary entry point (not a long-lived feature branch).<br>_Estimate: “box checked” based on preparation for review and testing._
4.	Publish to PyPI or CRAN if the project is a reusable library.<br>_Estimate: extra-small task, 1 hour._
5.	Optionally provide an AI tool (plugin, MCP server, or chatbot) to enhance documentation, streamline configuration, help customize etc. as appropriate to make the project more accessible.<br>_Estimate: **could be non-trivial – several days to several weeks.**_
6.	Optionally provide a dedicated documentation website.<br>_Estimate: small task, <1 week with coordination with EIT._
7.	Announce via appropriate channels (e.g., social media, partner networks).<br>_Estimate: small task, <1 week for content development and coordination with comms._

> **Ready for public release when:**
> - All baseline and tier-specific quality requirements are met
> - Quality assessment steps are complete
> - Stakeholder sign-off is documented

## Ongoing maintenance commitments

Making a project public is an ongoing commitment. Public repositories have users who depend on them. Plan for:

- **Technical debt**: Proactively managed to keep the codebase healthy over time.
- **Security maintenance**: Periodic vulnerability scanning and dependency updates.
- **Releases**: Frequent releases, especially for bug fixes.
- **Support**: User questions and bug reports receive a first response within 24 hours; resolution time depends on severity.
- **Docs sync**: Documentation kept in sync with code.

For Tier 1 projects, this typically requires dedicated engineering time on an ongoing basis. For Tier 2 and Tier 3 projects, maintenance can be lighter, but should still be explicitly planned and resourced before release.

## Roles and expectations

- management: go/no-go decision and allocation of time and resources
- research: sign-off on correctness, review research code, breadth and depth of test coverage, and accuracy of documentation for research usage
- software: run automated assessments, address quality gaps, support code review, testing, and technical documentation
- documentation: review documentation for quality and completeness and support public communications
