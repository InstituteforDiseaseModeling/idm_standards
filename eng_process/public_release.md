# Considerations for Public Release

Christopher Lorton, Cliff Kerr, Claude - April 2026

This document describes the requirements and procedure for making a repository public. It is written for managers and directors who are deciding whether to make a project public and what resources that decision requires.

Goals:
- provide guidance on making projects public and when _not_ to make them public
- lay out expectations for quality for public projects
- highlight resources for assessing quality and addressing quality issues
- provide estimates on team and time commitments for making projects public

## Public/private considerations

We want to make a project/code public if it meets one or more of the following criteria:

- It amplifies IDM's scientific impact by enabling others to build on our work
- It builds trust through transparency in scientific methods
- It attracts collaborators, contributors, and feedback that improve quality
- It fulfills our mission to share knowledge for global health benefit

There are three main reasons why a project _is not_ made public:

1. It contains sensitive data or results, so it is not allowed to be made public.
2. We are not confident yet that the results are correct, so it could potentially be misleading or dangerous to make it public.
3. It is neither sensitive nor dangerous, but it is of interest to so few people that making it public would create noise rather than signal.

If your project satisfies one or more of the criteria above and does not fall into any of these three disqualifying categories, consider making it public.

## Quality expectations

Quality expectations depend on the project's _tier_, which reflects its scope, intended audience, and expected lifetime. The [engineering quality guidelines](../eng_guidance/engineering_quality_guidelines.md) define the three tiers. Briefly, they are:

**Tier 1**: large-scale reusable library or “digital public good” (e.g., EMOD, Starsim, HPVSim) with many (10+) users, internal and external<br>
**Tier 2**: small-scale reusable code (e.g., calibrated country model, utility) with several (2-10) users, potentially external<br>
**Tier 3**: one-off or exploratory code (e.g., code for a paper or presentation) with a few (1-5) users, primarily internal

Tier 1 should meet the full set of engineering quality standards — correctness, clear structure, comprehensive documentation, testing, and safety with any exceptions clearly identified and justified. Tier 2 and Tier 3 requirements are progressively lighter. The full details are in the [engineering quality guidelines](../eng_guidance/engineering_quality_guidelines.md).

Regardless of tier, **all public code must be:**

- **Correct**: The code does what it claims to do. Peer review and colleague second opinions strengthen this.
- **Tested**: Appropriate test coverage for the tier. Tier 1 and Tier 2 code are expected to have automated tests appropriate to their scope; Tier 3 code may instead be validated through usage when that is appropriate for the work. For non-trivial code, "it looked right when I ran it" is not sufficient.
- **Documented**: Every public repo needs at minimum a README explaining purpose, installation, and basic usage.
- **Safe**: *Under no circumstances* make a repo public if it contains sensitive data, personally identifiable information (PII), API keys, or other secrets.
- **Licensed**: By default we are using the [MIT License](https://opensource.org/license/MIT).

## Quality assessments

Before a project goes public, the team should perform the following actions to assess the state of a project with respect to the quality expectations and identify any gaps:

1. **Run automated review** (all tiers): Use the [IDM Engineering Plugin](https://github.com/institutefordiseasemodeling/idm_standards/tree/main/idm_eng_plugin) — a Claude Code plugin built directly from the engineering guidelines — to score the project and generate a prioritized list of gaps and improvements. _Estimate: 1 person, 1 hour._
2. **Perform peer code review** (T1 and T2, recommended for T3): At least one engineer who did not write the code reviews it against the [engineering quality guidelines](../eng_guidance/engineering_quality_guidelines.md). _Estimate: 1 person, 1 day – 1+ weeks depending on project size._
3. **Perform documentation review** (T1 and T2, recommended for T3): The content team reviews docs for clarity and completeness. _Estimate: 1 person, 1 day – 1+ weeks depending on project size._
4. **Get stakeholder sign-off**: All stakeholders confirm the project meets its success criteria. _Estimate: 1 day – 1 week depending on number of stakeholders and project size._
5. **Run history scan**: Verify the full commit history (not just the current state) contains no secrets, API keys, or sensitive data that were accidentally committed and later deleted. If found, these must be excised from history before the repo is made public. _Estimate: 1 person, 1 hour._

## Time and team size estimates for public release quality assurance

Effort depends heavily on the project's current state and target tier. Rough guidance:

- **Tier 3 → public**: If the code is already correct and has a README, the main effort is typically documenting and removing any sensitive content. _Estimate: 1 person, 0.5–2 days._
- **Tier 2 → public**: Typically requires adding tests, improving documentation (README + example scripts or tutorial), ensuring reproducibility (pinned dependencies), and passing a code review. _Estimate: several people, 2–5 days for a project in decent shape; more if significant gaps exist._
- **Tier 1 → public**: Full Tier 1 quality is a significant ongoing investment. Projects intended for public Tier 1 release should be designed to that standard from the start; retrofitting rarely is cost-effective. _Estimate: multi-preson team, weeks to months depending on gaps._

The [IDM Engineering Plugin](https://github.com/institutefordiseasemodeling/idm_standards/tree/main/idm_eng_plugin) can provide a more specific estimate based on an actual assessment of the project.

## The release process

Once a project is ready to go public, follow the [launch checklist](processes.md) from the engineering processes guide:

1.	All stakeholders confirm the project meets its success criteria.<br>_Estimate: “box checked” based on quality assessment (QA) above._
2.	Full codebase is reviewed by an engineer and AI tool against the quality guidelines.<br>_Estimate: “box checked” based on the QA work._
3.	Docs are reviewed by the content team for clarity and completeness.<br>_Estimate: “box checked” based on the QA work._
4.	Ensure the main branch is the primary entry point (not a long-lived feature branch).<br>_Estimate: “box checked” based on preparation for review and testing._
5.	Publish to PyPI or CRAN if the project is a reusable library.<br>_Estimate: extra-small task, 1 hour._
6.	Optionally pair with an AI tool (plugin, MCP server, or chatbot) to make the project more accessible.<br>_Estimate: **could be non-trivial – several days to several weeks.**_
7.	Optionally pair with a dedicated documentation website.<br>_Estimate: small task, <1 week with coordination with EIT._
8.	Announce via social media, websites, and partner channels as appropriate.<br>_Estimate: small task, <1 week for content development and coordination with comms._


## Ongoing maintenance commitments

Making a project public is a commitment, not a one-time action. Public repositories have users who depend on them. Plan for:

- **Technical debt**: Proactively managed to keep the codebase healthy over time.
- **Releases**: Frequent releases, especially for bug fixes.
- **Support**: User questions and bug reports receive a first response within 24 hours, with resolution time depending on severity.
- **Docs sync**: Documentation kept in sync with code.

For Tier 1 projects, this typically requires dedicated engineering time on an ongoing basis. For Tier 2 and Tier 3 projects, maintenance can be lighter, but should still be explicitly planned and resourced before release.

## Roles and expectations

- management: go/no go decision for making projects public including allocating time and resources for meeting IDM quality expectations
- research: sign-off on correctness, review research code, breadth and depth of test coverage, and accuracy of documentation for research usage
- software: help with or run automated tools for quality assessment and addressing quality gaps, assist with code reviews, help with implementing necessary test coverage, generate technical documentation
- documentation: review documentation for quality and completeness according to tier expectations and public comms as appropriate
