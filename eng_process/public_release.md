# Public release

This document describes the procedure for making a repo public.

## Principles

In general, we want code to be public, so the world can benefit from it. However, there are three main reasons why something *isn't* public:

1. It contains sensitive data or results, so is not allowed to be made public.
2. We are not confident yet that the results are correct, so it could potentially be misleading or dangerous to make it public.
3. It is neither sensitive nor dangerous, but it is of interest to so few people that making it public would create noise rather than signal.

If your code doesn't fall into any of these three categories, consider making it public.

## Guidance

Before being made public, code should follow the relevant [engineering guidelines](../eng_guidance/engineering_quality_guidelines.md). These differ depending on the "tier" of project, e.g. simple plotting or data analysis scripts have less strict requirements than large-scale reusable disease models.

However, all code should be:

- **Correct**. The best guard against code being incorrect is still your brain. Use it. It also doesn't hurt to ask a colleague, even if that colleague is an LLM, for a second opinion.
- **Tested**. It's not usually enough to *think* your code is correct; unless it is doing something trivial (e.g. plotting), there is usually room to write at least some tests for it.
- **Documented**. Not every repo needs full docs, but all should have a README at minimum.
- **Safe**. As noted above, *under no circumstances* make a repo public if it contains sensitive data, such as personally identifiable information (PII), API keys, etc.
