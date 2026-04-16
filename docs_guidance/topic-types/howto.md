# How-to guide documentation reference

## Overview

How-to guides are **goal-oriented directions** that help users accomplish specific tasks or solve real problems. They guide action through practical steps focused on what users want to achieve.

## Core definition

How-to guides assume competence and focus exclusively on helping users accomplish a specific, known goal. They are about **action and only action** no teaching, no explanation, no reference material.

## Critical distinction: How-to guide vs tutorial

This is the **most commonly confused distinction** in documentation. Both contain steps, but they serve fundamentally different purposes:

| Aspect | How-to guide | Tutorial |
|--------|--------------|----------|
| **User knowledge** | Already knows what they want to achieve | Learner may not know enough to even ask the right questions |
| **Approach** | General: many things unknowable in advance or different in each case | Concrete and particular: specific, known tools and materials we've set before the learner |
| **Path structure** | Forks and branches, different routes to same destination | Single line, no choices or alternatives |
| **Completeness** | Doesn't need to be complete: starts/ends at reasonable points | Must be complete end-to-end guide |
| **Safety** | Cannot promise safety: often only one chance to get it right | Must be safe: no harm can come, always possible to go back and start again |
| **Responsibility** | User has responsibility for getting in and out of trouble | Teacher has responsibility: if learner gets in trouble, teacher must fix it |
| **Focus** | Work—accomplishing tasks | Study—learning skills |

**Good how-to guide examples:**
- "How to calibrate transmission parameters to surveillance data"
- "How to add a waning immunity compartment to an SEIR model"
- "How to structure age-stratified contact matrices for a population"
- "Troubleshooting oscillating or unstable model outputs"



**NOT how-to guides** (too broad, really need tutorials):
- "How to build an SIR model"
- "How to use the API"

## Key principles

### 1. Focus on user goals, not tools

**User-centered perspective:**
- "How-to guides must be written from the perspective of the user, not of the machinery"
- Address real-world human needs and purposes
- Tools should be incidental to the larger human goal
- Think about what users want to accomplish, not what the software can do

**Omit the obvious:**
- Skip trivial technical steps users should already know
- Don't include foundational concepts or basic operations
- Assume baseline competence with the tools

**Example distinction:**
- Poor: "How to use the API" (tool-centered)
- Good: "How to add complex migration into your model" (user-centered goal)

### 2. Assume competence

**Target audience:**
- Serve already-competent users who know what they want to achieve
- Users understand their goal and have chosen to pursue it
- Don't include teaching or foundational explanations
- Expect readers can follow instructions correctly

**Not for beginners:**
- How-to guides are not tutorials
- They don't teach from scratch
- They guide practitioners toward specific outcomes

### 3. Maintain targeted focus

**Action only:**
- Stay centered on the specific task or problem
- Avoid digression, explanation, or reference material
- Every sentence must advance the user toward their goal
- Remove anything that doesn't directly serve task completion

**What to exclude:**
- Teaching moments or conceptual explanations
- Complete reference material or option catalogs
- Historical context or design rationale
- Exploration of alternatives (unless directly relevant)

**Linking out:**
- If additional context matters, link to it externally
- Point to explanation documentation for "why"
- Reference API docs for complete option lists
- Link to tutorials for foundational learning

### 4. Embrace key characteristics

**Task/problem focus:**
- Each guide addresses one specific goal or problem
- Title clearly states what will be accomplished
- Content delivers on that promise exclusively

**Practical usability over completeness:**
- Better to be useful for real scenarios than theoretically complete
- Address actual use cases, not every possible variation
- Optimize for practitioners doing real work

## Structural guidelines

### Sequence and logic

**Temporal order:**
- Organize steps in the order they must be performed
- Each step builds meaningfully on previous ones
- Include all steps needed to accomplish goal
- Follow natural workflow progression

**Meaningful progression:**
- Consider how users think about the task
- Structure reflects practical necessity
- Anticipate mental model and workflow

### Flow

**Smooth progress:**
- Anticipate user needs like a helpful assistant
- Minimize context-switching between tools
- Structure thinking progression naturally
- "Seek flow: smooth progress"

**Rhythm:**
- Maintain consistent pacing
- Balance detail with forward momentum
- Keep users moving toward completion

### Adaptability

**Real-world flexibility:**
- Address real-world complexity and variation
- Allow users to adapt guidance to their situations
- Don't over-specify narrow use cases
- Acknowledge when choices depend on context

**Conditional guidance:**
- "If you want x, do y"
- "When z is true, use approach a"
- Provide decision points where relevant

## Naming and language

### Title guidelines

**Clear statement of outcome:**
- State exactly what the guide accomplishes
- Use "How to..." format
- Avoid ambiguous titles that leave purpose unclear

**Good examples:**
- "How to calibrate transmission parameters to surveillance data"
- "How to add waning immunity to a model"
- "How to configure age-stratified contact networks"
- "How to configure seasonal migration in your population"

**Poor examples:**
- "Working with parameters" (unclear intent, tutorial? reference?)
- "Model calibration" (too vague)
- "Interventions" (what about them?)

### Voice and phrasing

**Conditional imperatives:**
- "If you want x, do y"
- "To accomplish z, follow these steps"
- "When a happens, perform b"

**Opening patterns:**
- "This guide shows you how to [specific task]"
- "Follow these steps to [accomplish the goal]"
- "To [accomplish goal], you need to [do these tasks]"

**Reference to other materials:**
- "Refer to the x reference guide for full options"
- "See the y tutorial for an introduction"
- "For background on z, consult the explanation documentation"

### Imperative tone

- Direct, action-oriented language
- "Configure the settings "
- "Run the command..."
- "Add the following code..."

## What NOT to include

### Tutorials are different

- Don't try to teach concepts while guiding tasks
- Don't include learning exercises
- Don't explain foundational principles

### Avoid procedural-only thinking

- Problems need adaptability, not just procedures
- Allow for variation in user context
- Don't be so rigid that guides fail in real scenarios

### No teaching moments

- Resist the urge to explain while instructing
- Keep foundational explanations out
- Link to explanation docs instead

### Not a complete reference

- Don't document every option or parameter
- Include only what's needed for the task
- Link to reference docs for completeness

### Minimize digression

- No historical context (that's explanation)
- No exploration of alternatives (unless directly relevant)
- No tangential information
- Stay on the path to goal completion

## The Recipe model

Cooking recipes exemplify strong how-to documentation:

**Clear problem statement:**
- Recipe title tells you what you'll make
- Ingredients list shows what you need

**Focused instructions:**
- Steps directed at the goal
- No tangents about history of the dish
- No explanation of why techniques work

**Required baseline competence:**
- Assumes you can chop, stir, measure
- Doesn't teach basic kitchen skills
- Focuses on this specific dish

**Established format:**
- Consistent structure across recipes
- Users know what to expect
- Easy to scan and follow

**Practical orientation:**
- Real-world cooking, not culinary theory
- Adaptable to your kitchen and ingredients
- Gets you to edible result

## Common pitfalls

1. **Mixing teaching with tasks**
   - Don't explain concepts while giving instructions
   - Keep learning and doing separate

2. **Tool-centered writing**
   - Don't organize around software features
   - Focus on what users want to accomplish

3. **Over-specification**
   - Don't make guides so narrow they're not adaptable
   - Allow for real-world variation

4. **Scope creep**
   - Don't let guides expand into tutorials or reference
   - Stay focused on the single task

5. **Missing the goal**
   - Don't forget to state what will be accomplished
   - Make the outcome crystal clear

## When to write how-to guides

Write how-to guides when users need to:
- Accomplish a specific, defined task
- Solve a particular problem
- Integrate your product with another system
- Configure something for a specific use case
- Perform a known operation successfully

## When NOT to write how-to guides

Don't write how-to guides when users need to:
- Learn concepts from scratch (use tutorials)
- Look up technical details (use reference)
- Understand why things work (use explanation)
- Get their first experience with the product (use tutorial)

## Checklist for writing how-to guides

- [ ] Focuses on a specific, clearly-stated goal
- [ ] Title uses "How to..." format and states outcome
- [ ] Assumes user competence with basics
- [ ] User-centered, not tool-centered
- [ ] Steps in logical, temporal order
- [ ] Action-oriented with minimal explanation
- [ ] Adaptable to real-world variations
- [ ] No teaching or foundational concepts
- [ ] No complete reference material (links instead)
- [ ] No historical context or design rationale
- [ ] Maintains flow and forward momentum
- [ ] Each step advances toward the goal
- [ ] Links to tutorials, reference, and explanation as needed