# How-to

How-tos are **goal-oriented directions** that help users accomplish specific tasks or solve real problems. They guide action through practical steps focused on what users want to achieve.

How-tos assume competence and focus exclusively on helping users accomplish a specific, known goal. They are about **action and only action** no teaching, no explanation, no reference material.

## Critical distinction: How-to vs tutorial

This is the **most commonly confused distinction** in documentation. Both contain steps, but they serve fundamentally different purposes:

| Aspect | How-to       | Tutorial |
|--------|--------------|----------|
| **User knowledge** | Already knows what they want to achieve | Learner may not know enough to even ask the right questions |
| **Approach** | General: many things unknowable in advance or different in each case | Concrete and particular: specific, known tools and materials we've set before the learner |
| **Path structure** | Forks and branches, different routes to same destination | Single line, no choices or alternatives |
| **Completeness** | Doesn't need to be complete: starts/ends at reasonable points | Must be complete end-to-end guide |
| **Safety** | Cannot promise safety: often only one chance to get it right | Must be safe: no harm can come, always possible to go back and start again |
| **Responsibility** | User has responsibility for getting in and out of trouble | Teacher has responsibility: if learner gets in trouble, teacher must fix it |
| **Focus** | Work—accomplishing tasks | Study—learning skills |

**Good how-to examples:**

- "How to calibrate transmission parameters to surveillance data"
- "How to add a waning immunity compartment to an SEIR model"
- "How to structure age-stratified contact matrices for a population"
- "Troubleshooting oscillating or unstable model outputs"

**NOT how-tos** (too broad, really need tutorials):

- "How to build an SIR model"
- "How to use the API"

## Key principles

### 1. Focus on user goals, not tools

- How-tos must be written from the perspective of the user, not of the machinery
- Address real-world human needs and purposes
- Tools should be incidental to the larger human goal
- Think about what users want to accomplish, not what the software can do

### 2. Assume competence

- Serve already-competent users who know what they want to achieve
- Users understand their goal and have chosen to pursue it
- Don't include teaching or foundational explanations
- Expect readers can follow instructions correctly

### 3. Maintain targeted focus on action

- Stay centered on the specific task or problem
- Every sentence must advance the user toward their goal
- Remove anything that doesn't directly serve task completion
- Link to related explanation, reference, or tutorials

## Structural guidelines

Within the table of contents organization, how-to topics are organized within user guides that usually have explanation topics as the parent topics for a given subject.

### Sequence and logic

**Temporal order:**

- Organize steps in the order they must be performed
- Each step builds meaningfully on previous ones
- Include all steps needed to accomplish goal

**Conditional guidance:**

- "If you want x, do y"
- "When z is true, use approach a"
- Provide decision points where relevant

## Naming and language

### Title guidelines

- State exactly what the guide accomplishes
- Use "How to..." format
- Avoid ambiguous titles that leave purpose unclear

### Imperative tone in steps

- Direct, action-oriented language
- "Configure the settings "
- "Run the command..."
- "Add the following code..."

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
   - Make the outcome clear