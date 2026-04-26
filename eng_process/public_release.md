# Considerations for Public Release

Christopher Lorton, Cliff Kerr, Claude - April 2026

This document describes the requirements and process for making a project public. It is intended to help managers and directors decide whether to make a project public and determine required resources.

---

# Summary

## When to make a project public

We want to make a project/repository public if it meets one or more of the following criteria:

* It amplifies IDM's scientific impact by enabling others to build on our work
* It builds trust through transparency in scientific methods
* It attracts collaborators, contributors, and feedback that improve quality
* It fulfills our mission to share knowledge for global health benefit

There are three main reasons why a project *is not* made public:

1. It contains sensitive data or results, so it is not allowed to be made public.
2. We are not confident yet that the results are correct, so it could potentially be misleading or dangerous to make it public.
3. It is neither sensitive nor dangerous, but it is of interest to so few people that making it public would create noise rather than signal.

If a project meets one or more of these criteria and none of the disqualifying conditions, it should be considered for public release.

---

## Quality expectations (summary)

Quality expectations depend on the project's *tier*, which reflects its scope, intended audience, and expected lifetime:

* **Tier 1**: large-scale reusable library or “digital public good” with many users
* **Tier 2**: small-scale reusable code with several users
* **Tier 3**: one-off or exploratory code with few users

**All public code must be:**

* **Correct**: The code does what it claims to do, supported by peer review. For modeling code, this includes reproducibility of key results and validation against known benchmarks where applicable.
* **Tested**: Appropriate test coverage for the tier. Tier 1 and Tier 2 require automated tests; Tier 3 may rely on usage-based validation where sufficient. For non-trivial code, "it looked right when I ran it" is not acceptable.
* **Documented**: Every public repository must include a README covering purpose, installation, and basic usage.
* **Safe**: *Under no circumstances* make a repository public if it contains sensitive data, personally identifiable information (PII), API keys, or other secrets.
* **Licensed**: By default, repositories use the MIT License.

---

## Effort estimates

Effort depends on the project’s current state and target tier:

* **Tier 3 → public**: ~0.5–2 days, 1 person
* **Tier 2 → public**: ~2–5 days, several people
* **Tier 1 → public**: weeks–months, multi-person team

---

> **Ready for public release when:**
>
> * All baseline and tier-specific quality requirements are met
> * Quality assessment steps are complete
> * Stakeholder sign-off is documented

---

## Ongoing commitments

Making a project public is an ongoing commitment. Plan for:

* Technical debt management
* Security maintenance (vulnerability scanning and dependency updates)
* Frequent releases, especially for bug fixes
* User support (first response within 24 hours)
* Documentation kept in sync with code

---

# Appendices

## Appendix A: Quality expectations (detailed)

Quality expectations depend on the project's *tier*, which reflects its scope, intended audience, and expected lifetime. The [engineering quality guidelines](../eng_guidance/engineering_quality_guidelines.md) define the three tiers. Briefly, they are:

**Tier 1**: large-scale reusable library or “digital public good” (e.g., EMOD, Starsim, HPVSim) with many (10+) users, internal and external

**Tier 2**: small-scale reusable code (e.g., calibrated country model, utility) with several (2-10) users, potentially external

**Tier 3**: one-off or exploratory code (e.g., code for a paper or presentation) with a few (1-5) users, primarily internal

Tier 1 should meet the full set of engineering standards — correctness, structure, documentation, testing, and safety — with any exceptions clearly justified. Tier 2 and Tier 3 requirements are progressively lighter. The full details are in the [engineering quality guidelines](../eng_guidance/engineering_quality_guidelines.md).

---

## Appendix B: Quality assessments

Before a project goes public, the team should perform the following actions:

1. **Run automated review** (all tiers): Use the IDM Engineering Plugin to score the project and generate a prioritized list of gaps and improvements. *Estimate: 1 person, 1 hour.*
2. **Perform peer code review** (T1 and T2, recommended for T3): At least one engineer who did not write the code reviews it against the guidelines. *Estimate: 1 person, 1 day – 1+ weeks.*
3. **Perform documentation review** (T1 and T2, recommended for T3): The content team reviews docs for clarity and completeness. *Estimate: 1 person, 1 day – 1+ weeks.*
4. **Get stakeholder sign-off**: All stakeholders confirm the project meets its success criteria. *Estimate: 1 day – 1 week depending on number of stakeholders and project size.*
5. **Run history scan**: Verify the full commit history contains no secrets or sensitive data. *Estimate: 1 person, 1 hour.*

---

## Appendix C: Time and team size estimates (detailed)

Effort depends on the project's current state and target tier:

- **Tier 3 → public**: If the code is already correct and has a README, the main effort is documenting and removing sensitive content. *Estimate: 1 person, 0.5–2 days.*
- **Tier 2 → public**: Typically requires tests, improved documentation (README + examples), reproducibility (pinned dependencies), and code review. *Estimate: several people, 2–5 days for a project in decent shape; more if significant gaps exist.*
- **Tier 1 → public**: Tier 1 quality is a significant ongoing investment. Projects should be designed to that standard from the start. *Estimate: multi-person team, weeks to months.*

The IDM Engineering Plugin can provide a more specific estimate.

---

## Appendix D: Release process

Once a project is ready to go public, follow the launch checklist:

1. Stakeholders confirm the project meets its success criteria.
2. Quality assessment steps are completed (see above).
3. Ensure the main branch is the primary entry point.
4. Publish to PyPI or CRAN if the project is a reusable library.
5. Optionally provide an AI tool (e.g., plugin or chatbot) to improve usability.
6. Optionally provide a dedicated documentation website.
7. Announce via appropriate channels.

---

## Appendix E: Roles and expectations

* **management**: go/no-go decision and allocation of time and resources
* **research**: sign-off on correctness, review research code, test coverage, and documentation accuracy
* **software**: run automated assessments, address quality gaps, support code review, testing, and technical documentation
* **documentation**: review documentation for quality and completeness and support public communications
