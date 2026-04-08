# Model user persona

People who run pre-built models or dashboards to answer concrete questions, without changing the underlying code.

## Who they are

Applied researchers, program analysts, and some LMIC technical public health professionals who need scenario results but don’t want to modify internal code. This persona is very common within IDM and with many of our external partners. 

## What they do

Use pre-calibrated models, notebooks, or apps to run scenarios, explore interventions, and generate outputs for reports or decisions; may format data into required templates and write analysis and plotting scripts but rarely edit core model code. 

## Skills/tools

Moderate scientific and analytical skills; basic scripting or notebook use is okay, but they prioritize usability, clear tutorials, and interpretable outputs over deep technical control.  Often they are familiar with R but not Python or other coding languages. 

## Key needs

Intuitive UIs/dashboards, step-by-step tutorials, clear guidance on data requirements and limitations, and help interpreting results for their context (for example, “Is this model right for my question?”). Model users often have a strong epidemiology or biology background but lack skills in programming and need guidance on coding best practices and fundamentals.

## Decision-making context

Model users make analytical decisions rather than policy decisions: which model to use, which scenarios to run, how to interpret results, and how to communicate findings to stakeholders. The policy question is usually set for them — their job is to translate it into model inputs and translate outputs back into meaningful results. Errors in either translation can propagate into bad policy recommendations without anyone noticing.

They work under time pressure, often with incomplete local data, and frequently on infrastructure with limited compute or unreliable internet. Many have strong epidemiology or biology backgrounds but limited programming experience, and they are often more comfortable in R than Python. They need enough methodological grounding to make defensible choices but are unlikely to engage deeply with mathematical derivations.

**For developers:** Prioritize usability over flexibility for features model users will interact with. Defaults should be sensible for common use cases so users aren't forced to understand the full parameter space before running their first simulation. Error messages should explain what went wrong in terms the user can act on, not just report internal state. Consider whether features require reliable internet or HPC access, and whether there are lower-resource alternatives for LMIC contexts.

**For writers:** Lead with the workflow, not the theory. Model users need to know what steps to follow and what to check at each step — not why the math works. Use concrete disease examples and realistic data scenarios. Include guidance on interpreting outputs and recognizing when results are unreliable, since this is where errors most often go undetected.

## Targeted content

The software documentation for using specific disease models should be targeted to the needs of model users. Specifically, describe the typical researcher workflow for that model including data ingestion, model configuration, and analysis of output. For GitHub landing pages for modeling frameworks, provide guidance on selecting the right model for your data and specific research question. 
