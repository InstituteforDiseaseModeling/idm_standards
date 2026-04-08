# Model extender persona 

People who adapt and calibrate existing models to new questions, countries, or datasets.

## Who they are

Technically strong public-health modelers and data scientists (often LMIC technical public health professionals or research partners) who extend existing frameworks rather than building from scratch. While this persona is common within IDM, a relatively small percentage of people within the global health field are model extenders. 

## What they do

Import existing models, calibrate to local data, tweak assumptions, add or modify modules, and create custom intervention scenarios for specific contexts. 

## Skills/tools

High scientific and quantitative skills; moderate-to-strong coding skills (Python/R); comfortable working with parameters, data pipelines, and calibration workflows but may not want to re-architect the core framework. 

## Key needs

Clear APIs and extension points, “how-to extend” documentation (for example, add a module, calibrate to a new context), templates, and examples that make local adaptation reliable and reproducible. 

## Decision-making context

Model extenders make technical decisions about how to adapt an existing framework to a new context: which parameters to calibrate, which structural assumptions to relax or change, and how to validate that the adapted model is fit for its intended purpose. These decisions require both quantitative judgment and local knowledge. An extender working in a new country needs to know not just how to run a calibration but whether the result is epidemiologically plausible for that setting.

They often work at the boundary between modeling teams and in-country partners, justifying choices to people with varying technical backgrounds — model builders who may scrutinize the code and policy influencers who only care about the output. In LMIC contexts, they frequently work with sparser, noisier data than the original model was designed for, and need to make judgment calls about which parameters to estimate versus fix to literature values. Reproducibility matters because results often need to be handed off, archived, or rerun when input data changes.

**For developers:** When building extension points, consider whether they are usable without full knowledge of the framework internals. Assume the extender is working with incomplete local data — calibration workflows and APIs should behave predictably and fail informatively when data is sparse or missing. Reproducibility should be a design consideration, not an afterthought: make it straightforward to version, archive, and rerun an adapted model.

**For writers:** Show calibration and extension workflows under realistic conditions, not just ideal ones. Include guidance on how to decide whether a parameter should be estimated or fixed to a literature value. Document what "good enough" looks like at each stage so extenders can make defensible judgment calls without needing to consult a model builder.

## Targeted content

The software documentation for modeling frameworks and disease models and the GitHub landing pages for modeling frameworks should be targeted to the needs of model extenders. Specifically, describe how to add new modules to existing models to add functionality to simulate desired disease, healthcare, or population dynamics. 