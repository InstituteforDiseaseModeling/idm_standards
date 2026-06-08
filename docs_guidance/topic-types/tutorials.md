# Tutorials

A tutorial is a **learning-oriented, practical activity** where students learn by doing meaningful tasks toward achievable goals. It's a lesson, not a task completion guide.

Tutorials are experiences that enable learning through doing. The tutorial author bears primary responsibility for the learner's success. Tutorials prioritize skill and knowledge acquisition, not task completion.

## Critical distinction: Tutorial vs how-to

This is the **most commonly confused distinction** in documentation. Both contain steps, but they serve fundamentally different purposes:

| Aspect | Tutorial | How-to       |
|--------|----------|--------------|
| **User knowledge** | Learner may not know enough to even ask the right questions | Already knows what they want to achieve |
| **Approach** | Concrete and particular—specific, known tools and materials we've set before the learner | General: many things unknowable in advance or different in each case |
| **Path structure** | Single line, no choices or alternatives | Forks and branches, different routes to same destination |
| **Completeness** | Must be complete end-to-end guide | Doesn't need to be complete—starts/ends at reasonable points |
| **Safety** | Must be safe—no harm can come, always possible to go back and start again | Cannot promise safety—often only one chance to get it right |
| **Responsibility** | Teacher has responsibility: if learner gets in trouble, teacher must fix it | User has responsibility for getting in and out of trouble |
| **Focus** | Study—learning skills | Work—accomplishing tasks |

**Key insight**: You will revise tutorials far more than other docs. Unlike how-tos (which only change when the product changes), you may completely rewrite a tutorial because you found a better learning experience.

## Tutorial core principles

### 1. Minimize explanation--focus on doing

**Keep explanations brief:**

- Focus on enabling learning through doing, not explanation
- Explanation distracts from doing
- Provide links to deeper explanation rather than embedding it
- Brief justifications only when absolutely necessary

**The distraction problem:**

- Explanation breaks the flow
- Diverts attention from the task
- Cognitive load increases

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

### 5. Ignore options and alternatives

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

### 6. Aspire to perfect reliability

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

**Format and implementation**

Where possible, write tutorials as Jupyter notebooks or other executable formats. This allows tutorials to be run automatically during documentation builds, surfacing broken steps or outdated outputs before learners encounter them. This directly supports the principle of perfect reliability.

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

## Special challenges of tutorials

### Maintenance burden

- Tutorials cascade through documentation
- Changes ripple across entire narrative
- Product evolution requires ongoing updates
- Breaking changes are especially problematic
- Use executable formats (for example, Jupyter notebooks) to automatically catch breakage during builds

### No instructor present

- Can't correct mistakes in real-time
- Can't check understanding
- Can't adapt to learner needs
- Must anticipate all problems
