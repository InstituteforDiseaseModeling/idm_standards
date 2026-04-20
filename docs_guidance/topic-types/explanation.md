# Explanation

Explanation is **understanding-oriented** documentation that deepens reader comprehension through reflective, discursive treatment of conceptual topics. It answers: "Can you tell me about [topic]?"

Explanation operates at a higher, broader perspective than tutorials, how-tos, or reference material. It focuses on theoretical knowledge and context rather than immediate application, best consumed away from active work (not during task execution).

## Critical distinction: Explanation vs reference

Both provide knowledge (cognition), but for fundamentally different contexts:

| Test Question | If Yes → Explanation | If No → Reference |
|---------------|---------------------|-------------------|
| Could you imagine **reading this while not actively working**? | ✓ | |
| Does it primarily answer **"why?" questions**? | ✓ | |
| Would someone turn to this **while actively working**? | | ✓ |
| Is it **lists, tables, or technical specs**? | | ✓ |

**Key insight**: A tables of command-line options for git is reference. A topic explaining conceptually how git works is explanation.

**Explanation examples:**

- "Compartmental vs agent-based models: assumptions, trade-offs, and appropriate use" (why you would select one)
- "The trade-off between agent resolution and computational tractability"
- "How population heterogeneity shapes transmission dynamics"
- "The relationship between network structure and epidemic spread"

**Reference examples (NOT explanation):**

- API documentation
- Configuration option lists
- Error code tables
- Command syntax specifications

## Essential guidelines

### Make connections

- Link topics to related concepts, even beyond immediate scope
- Link to how-to or reference content related to the concepts discussed
- Weave understanding across domains
- Draw relationships between different parts of the system
- Connect to broader technical or domain concepts

### Provide context

Explanation should illuminate:

- **Design decisions**: Why was this approach chosen?
- **Historical reasons**: How did this evolve over time?
- **Technical constraints**: What limitations influenced this design?
- **Implications**: What does this mean for users/developers?
- **Specific examples**: Concrete illustrations of abstract concepts

### Address the bigger picture

Discussion topics should include:

- **History and evolution**: How did we get here?
- **Choices and alternatives**: What other approaches exist?
- **Reasons and justifications**: Why this way and not another?
- **Multiple perspectives**: Different viewpoints on the same question
- **Trade-offs**: What are the costs and benefits?

## Structural principles

Within the table of contents organization, explanation topics often serve as the parent topics for user guides that include related explanation and how-to topics for a given subject.

### Maintain clear boundaries

- Prevent explanation from absorbing instructional or reference content
- Keep material focused on the defined topic area
- Use "why questions" as prompts to define scope
- Don't let explanation become a tutorial or how-to
- Don't include detailed technical specifications (that's reference material)

### Naming convention

- Use titles that allow an implicit "About" prefix

  - Good: "User authentication" (reads as "About user authentication")
  - Good: "The request-response cycle"
  - Good: "Database normalization"
- Reflects the discursive nature of the material
- Avoids action-oriented or task-oriented phrasing

## Common mistakes to avoid

1. **Don't underestimate explanation's importance**
   - While less immediately urgent, it's crucial for deep understanding
   - Without explanation, users have fragmented, surface-level knowledge

2. **Don't allow instructional content to infiltrate**
   - Keep "how to do things" in how-to topics
   - Don't provide step-by-step instructions
   - Link to related reference or how-tos rather than embedding them

3. **Don't allow technical reference to infiltrate**
   - Keep detailed API specs, parameters, and technical descriptions in reference
   - Link to reference material rather than duplicating it

