# Reference

Reference topics provide **technical descriptions** that are **information-oriented**. They contain factual knowledge for users to consult during work, not to learn from sequentially.

Reference documentation serves as the authoritative source of technical truth about the product. Users consult it to look up specific information they need while working, not to learn sequentially or complete tasks.

## Critical distinction: Reference vs explanation

Both provide knowledge (cognition), but for fundamentally different contexts:

| Test question | If yes → reference | If no → explanation |
|---------------|-------------------|---------------------|
| Would someone turn to this **while actively working**? | ✓ | |
| Is it **lists, tables, or technical specs**? | ✓ | |
| Could you imagine **reading this while not actively working**? | | ✓ |
| Does it primarily answer **"why?" questions**? | | ✓ |

**Key insight**: A tables of command-line options for git is reference. A topic explaining conceptually how git works is explanation.

**Reference examples:**

- Classes and functions
- Configuration option lists
- Error code tables
- Command syntax specifications

**Explanation examples:**

- "How contact heterogeneity shapes transmission dynamics"
- "Why age-stratification matters for intervention modeling"
- "Network vs. compartmental approaches to transmission modeling"

## Key principles

### 1. Describe and only describe

**Austere, uncompromising style:**

- Maintain **neutral, objective, factual** language
- Prioritize accuracy, precision, completeness, and clarity
- No opinions, no marketing, no speculation

**Pure description:**

- Avoid instruction, explanation, opinion, or discussion
- Link to tutorials, how-to guides, or explanation rather than embedding them
- State what something **is** and what it **does**, and **when** to use it
- Be complete, make sure to include relevant dependencies for model parameters and usage examples

**Mirror the machinery:**

- Structure content to mirror the product's structure itself, not user tasks
- Document the architecture as it exists
- Help users navigate code and documentation in parallel

### 2. Adopt standard patterns

"Reference material is useful when it is consistent."

**Consistency requirements:**

- Use standardized formatting throughout
- Place information where users expect it
- Maintain familiar formats across all reference pages
- Create predictable patterns users can rely on

**Standard elements:**

- Function/method signatures
- Parameter descriptions
- Return values
- Error conditions
- Examples of usage

### 3. Provide examples

**Illustrative, not pedagogical:**

- Use examples to illustrate usage succinctly
- Show context without explaining or teaching
- Demonstrate syntax and format
- Keep examples minimal and focused
- Include necessary dependencies

## Content to include

### Essential elements

**For functions/methods:**

- Name and signature
- Purpose (what it does including necessary context, but not how to use it)
- Parameters with types and descriptions
- Return values and types
- Required dependencies
- Exceptions/errors that may occur
- Brief usage example

**For commands:**

- Command syntax
- Available options and flags
- Arguments and their formats
- Output format
- Exit codes
- Error conditions

**For configuration:**

- Setting names
- Valid values and types
- Default values
- Scope and applicability
- Dependencies and interactions

### Warnings and constraints

Include appropriate warnings about:

- **Requirements**: Prerequisites, dependencies
- **Restrictions**: What cannot be done
- **Limitations**: Boundaries and constraints
- **Deprecated features**: Status and migration paths
- **Breaking changes**: Version-specific behavior

## Common mistakes to avoid

1. **Mixing in instructions**
   - Don't include "how to" steps
   - Link to how-to guides instead

2. **Including explanations**
   - Don't explain why things work this way
   - Link to explanation documentation instead

3. **Marketing language**
   - Avoid subjective claims
   - Stick to objective facts

4. **Inconsistent structure**
   - Maintain the same format throughout
   - Don't reorganize by user needs

5. **Incomplete coverage**
   - Document everything, not just common cases
   - Include all parameters and options

6. **Opinion and recommendation**
   - Don't tell users what they should do
   - Present facts, not guidance
