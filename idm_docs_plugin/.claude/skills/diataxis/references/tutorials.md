# Tutorial documentation reference

## Overview

A tutorial is a **learning-oriented, practical activity** where students learn by doing meaningful tasks toward achievable goals. It's a lesson, not a task completion guide.

## Core definition

Tutorials are experiences that enable learning through doing. The tutorial author bears primary responsibility for the learner's success. Tutorials prioritize skill and knowledge acquisition, not task completion.

## The teacher's contract

Nearly all responsibility falls on the teacher. The student's only obligation is attentiveness and following directions.

**The exercise must be:**
- **Meaningful**: Provides sense of achievement
- **Successful**: Completable by the learner
- **Logical**: Coherent progression that makes sense
- **Usefully complete**: Exposes all necessary actions, concepts, and tools

## Critical distinction: Tutorial vs how-to guide

This is the **most commonly confused distinction** in documentation. Both contain steps, but they serve fundamentally different purposes:

| Aspect | Tutorial | How-to guide |
|--------|----------|--------------|
| **User knowledge** | Learner may not know enough to even ask the right questions | Already knows what they want to achieve |
| **Approach** | Concrete and particular—specific, known tools and materials we've set before the learner | General: many things unknowable in advance or different in each case |
| **Path structure** | Single line, no choices or alternatives | Forks and branches, different routes to same destination |
| **Completeness** | Must be complete end-to-end guide | Doesn't need to be complete—starts/ends at reasonable points |
| **Safety** | Must be safe—no harm can come, always possible to go back and start again | Cannot promise safety—often only one chance to get it right |
| **Responsibility** | Teacher has responsibility: if learner gets in trouble, teacher must fix it | User has responsibility for getting in and out of trouble |
| **Focus** | Study—learning skills | Work—accomplishing tasks |

**Key insight**: You will revise tutorials far more than other docs. Unlike how-to guides (which only change when the product changes), you may completely rewrite a tutorial because you found a better learning experience.

## The 11 core principles

### 1. Don't try to teach

"Your job, as a teacher, is to provide the learner with an experience that will allow them to learn."

- Focus on enabling learning through doing, not explanation
- Provide experiences, not lectures
- Let understanding emerge from practice
- The learner learns by doing, not by being told

### 2. Show the destination upfront

**Orient the learner:**
- Inform learners what they'll accomplish at the start
- Example: "In this tutorial we will create and run a simulation"
- Avoid presumptuous "you will learn" phrasing
- Give learners confidence in where they're heading

**Why this matters:**
- Reduces anxiety and uncertainty
- Provides context for upcoming steps
- Helps learners see the value of the journey

### 3. Deliver visible results early and often

**Rapid feedback loops:**
- Every step must produce comprehensible results
- Learners should see changes after each action
- Enable cause-and-effect connections repeatedly
- Build confidence through immediate success

**The power of results:**
- Validates that learners are on track
- Reinforces correct actions
- Maintains engagement and motivation
- Allows learners to verify their progress

### 4. Maintain narrative expectations

**Guide what to expect:**
- Use phrases like "You will notice that [observation]"
- Show actual expected output
- Warn about likely confusion points
- Provide reassurance throughout

**Example patterns:**
- "The output should look like [specific output]"
- "Notice that the prompt has changed to [new prompt value]"
- "You should now see [expected output]"
- "This may take a few moments"

### 5. Point out what learners should notice

"Learning requires reflection."

**Active observation guidance:**
- Explicitly highlight environmental changes
- Point out important details
- Draw attention to significant results
- Don't assume learners notice things independently

**Examples:**
- "Notice that the prompt now shows `(venv)`"
- "The terminal output indicates success with [success indicator]"
- "Observe how the interface has changed [specific change]"

### 6. Target the feeling of doing

**Flow state creation:**
- Build tasks that connect: purpose -> action -> thinking -> result
- Create rhythmic, pleasurable progression
- Enable the satisfaction of skilled practice
- Let competence feel rewarding

**The doing experience:**
- Learners should feel actively engaged
- Each step should feel purposeful
- Progress should feel natural and inevitable
- Success should feel earned but achievable

### 7. Encourage repetition

**Repetition reinforces learning:**
- Allow steps to be repeated where possible
- Users naturally repeat successful steps
- Repetition confirms reliability
- Reinforcement builds confidence

**Why repetition works:**
- Solidifies new skills through practice
- Allows learners to internalize patterns
- Builds muscle memory for workflows
- Increases retention

### 8. Ruthlessly minimize explanation

"A tutorial is not the place for explanation."

**Keep explanations brief:**
- Learners are focused on correct execution
- Explanation distracts from doing
- Provide links to deeper explanation rather than embedding it
- Brief justifications only when absolutely necessary

**The distraction problem:**
- Explanation breaks the flow
- Diverts attention from the task
- Cognitive load increases
- Learners lose the thread

### 9. Focus on the concrete

**Concrete before abstract:**
- Lead "from step to concrete step"
- Use specific examples, not generalizations
- The mind learns concrete-to-abstract, never the reverse
- General patterns emerge naturally from concrete practice

**Concrete examples:**
- Use actual file names, not placeholders
- Show real commands, not templates
- Demonstrate with specific values
- Let abstraction emerge through experience

### 10. Ignore options and alternatives

**Single path only:**
- Exclude alternative commands or approaches
- No optional steps or variations
- Don't discuss different API methods
- Keep guidance focused on one successful path

**Why single path:**
- Prevents decision paralysis
- Reduces cognitive load
- Ensures tutorial reliability
- Allows focus on learning, not choosing

### 11. Aspire to perfect reliability

"Confidence builds incrementally and shatters quickly."

**Zero tolerance for failure:**
- Every promised result must materialize
- Tutorial must work every single time
- Test extensively with actual users
- Discover and eliminate hidden gaps

**The confidence factor:**
- One failure destroys trust
- Learners blame themselves for tutorial problems
- Unreliable tutorials create lasting negative impressions
- Perfect reliability is non-negotiable

## Anti-pedagogical temptations to avoid

These common patterns sabotage learning:

1. **Abstraction and generalization**: Stay concrete
2. **Explanation and exposition**: Link to it, don't embed it
3. **Presenting choices**: Provide one clear path
4. **Information overload**: Ruthlessly minimize content

## Language patterns

| Pattern | Purpose | Example |
|---------|---------|---------|
| "We..." | Affirm tutor-learner collaboration | "In this tutorial, we will build [what is being built]" |
| Imperative sequence | Remove ambiguity | "First, do x. Now, do y. Next, do z." |
| Minimal justification | Provide just enough rationale | "We must do x before y because [reason] (see Explanation)" |
| Expected output | Set clear expectations | "The output should look like: [example output]" |
| Observation cues | Guide attention | "Notice that [observation]" / "Remember that [key point]" / "Let's check [what to clarify]" |
| Achievement acknowledgment | Affirm accomplishment | "You have [accomplished the goal]" |

## Voice and tone

### Collaborative "we"

- "We will create a new file"
- "Now we'll add the configuration"
- "Let's run the command together"
- Emphasizes partnership in learning

### Confident, reassuring

- Maintain certainty throughout
- Assure learners they're on the right track
- Acknowledge achievements
- Build confidence incrementally

### Active and present

- Use present tense for actions
- Keep learners engaged in the moment
- Focus on immediate next step
- Maintain forward momentum

## Tutorial vs. how-to guide distinction

**Tutorials:**
- Emphasis on **acquisition and study**
- For learning new skills
- Teacher bears responsibility
- Complete learning journey
- Appropriate for novices
- Focus on education

**How-to guides:**
- Facilitate **task completion**
- For applying known skills
- User bears responsibility
- Focused problem-solving
- Assume competence
- Focus on productivity

## The cooking analogy

Teaching a person to cook illustrates tutorial principles perfectly:

**Success criteria:**
- Person learns skills and gains pleasure
- Not about perfect culinary output
- Learning happens "through the activities" together
- Not from instruction alone

**Incomplete is acceptable:**
- If the person achieved something
- If the person enjoyed it
- Skills will develop over time
- Foundation matters most

## Special challenges of tutorials

### Maintenance burden

- Tutorials cascade through documentation
- Changes ripple across entire narrative
- Product evolution requires ongoing updates
- Breaking changes are especially problematic
- Use executable formats (e.g. Jupyter notebooks) to automatically catch breakage during builds

### No instructor present

- Can't correct mistakes in real-time
- Can't check understanding
- Can't adapt to learner needs
- Must anticipate all problems

### Design complexity

- Balancing "what to learn" and "what to do"
- Requires careful sequencing
- Must maintain perfect reliability
- Needs extensive testing with real users

## When to write tutorials

Write tutorials when users need to:
- Get their first hands-on experience
- Learn fundamental concepts through practice
- Build confidence with a new tool or system
- Understand basic workflows
- Achieve an early success that motivates further learning

## When NOT to write tutorials

Don't write tutorials when users need to:
- Complete a specific task (use how-to guides)
- Look up technical information (use reference)
- Understand why things work (use explanation)
- Apply skills they already have (use how-to guides)

## Checklist for writing tutorials

- [ ] Learning-oriented, not task-oriented
- [ ] Shows destination at the beginning
- [ ] Every step produces visible results
- [ ] Maintains narrative expectations throughout
- [ ] Points out what learners should notice
- [ ] Creates the feeling of doing
- [ ] Allows repetition where possible
- [ ] Minimizes explanation (links to it instead)
- [ ] Focuses on concrete steps, not abstractions
- [ ] Ignores options and alternatives
- [ ] Tested for perfect reliability
- [ ] Uses "we" language to build partnership
- [ ] Acknowledges learner achievements
- [ ] No choices or decision points
- [ ] Complete learning experience from start to finish
- [ ] Links to how-to guides, reference, and explanation as needed

## Format and implementation

Where possible, write tutorials as Jupyter notebooks or other executable formats. This allows tutorials to be run automatically during documentation builds, surfacing broken steps or outdated outputs before learners encounter them. This directly supports the principle of perfect reliability.
