---
name: diataxis
description: Centralizes Diataxis documentation framework guidance so Claude can write, review, or improve documentation following the four distinct topic types (tutorials, how-to guides, reference, explanation). Also includes guidance on how to organize those topics within the table of contents (TOC).
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Documentation skill

Unifies all Diataxis documentation guidance into one Skill. Claude activates this Skill whenever documentation is written, reviewed, or improved, and new topics are added within the table of contents. It then "lazy loads" the exact documentation type guidance by opening the reference docs linked below.

Diataxis framework by Daniele Procida. See [diataxis.fr](https://diataxis.fr/colophon/) for full attribution. Framework for the skill and reference file based on the work by [thewodapp](https://github.com/wodsmith/thewodapp).

## Critical workflow

**REQUIRED**: Before writing or reviewing ANY documentation, you MUST load the relevant documentation type reference file(s) using the Read tool.

1. **Use the compass** to identify the documentation type needed (see below)
2. **Read the matching reference file(s)** BEFORE writing/reviewing:
   - Learning experiences → Read `references/tutorials.md`
   - Task-oriented guides → Read `references/how-to-guides.md`
   - Information lookup → Read `references/reference.md`
   - Understanding & context → Read `references/explanation.md`
3. **Apply the documentation type's principles** from the loaded reference
4. Write or review documentation according to that type's standards
5. Add the topic to the documentation set table of contents and include cross-references → Read `references/toc.md`

**DO NOT attempt to write or review documentation without first loading the appropriate reference file(s).**

## The Diataxis compass

The compass is your primary decision-making tool. Consider the user's goals and needs, and ask two questions:

### Question 1: Action or cognition?

- **Action** = Practical steps, doing things, hands-on tasks
- **Cognition** = Theoretical knowledge, thinking, conceptual understanding

### Question 2: Acquisition or application?

- **Acquisition** = Study, learning something new
- **Application** = Work, using skills to accomplish tasks

### The four quadrants

```
                    ACQUISITION              APPLICATION
                    (Study)                  (Work)
              ┌─────────────────────┬─────────────────────┐
              │                     │                     │
   ACTION     │     TUTORIALS       │    HOW-TO GUIDES    │
   (Doing)    │   Learning-oriented │    Task-oriented    │
              │   "Teach me"        │    "Help me do X"   │
              │                     │                     │
              ├─────────────────────┼─────────────────────┤
              │                     │                     │
   COGNITION  │    EXPLANATION      │     REFERENCE       │
   (Knowing)  │ Understanding-      │  Information-       │
              │    oriented         │     oriented        │
              │   "Help me          │    "What is the     │
              │    understand"      │     spec for X?"    │
              └─────────────────────┴─────────────────────┘
```

### Quick decision guide

| User need | Action/Cognition | Acquisition/Application | → Type |
|-----------|------------------|-------------------------|--------|
| "How do I get started?" | Action | Acquisition | Tutorial |
| "How do I deploy to prod?" | Action | Application | How-to |
| "What parameters does X accept?" | Cognition | Application | Reference |
| "Why does the system work this way?" | Cognition | Acquisition | Explanation |

## Key distinctions (critical!)

### Tutorial vs how-to Guide

Both contain steps, but serve fundamentally different purposes:

| Aspect | Tutorial | How-to guide |
|--------|----------|--------------|
| **User** | Learner, may not know enough to ask questions | Competent practitioner who knows their goal |
| **Responsibility** | Teacher bears responsibility for success | User bears responsibility for outcomes |
| **Approach** | Concrete, specific, controlled environment | General, adaptable to real-world variation |
| **Path** | Single path, no choices | Multiple routes, branching options |
| **Completeness** | Must be complete end-to-end | Can start/end at reasonable points |
| **Safety** | Must be safe, can always restart | Cannot promise safety |
| **Focus** | Learning through doing | Getting work done |

### Reference vs explanation

Both provide knowledge, but for different contexts:

| Test question | If yes → | If no → |
|---------------|----------|---------|
| Would someone turn to this while actively working? | Reference | Explanation |
| Could you imagine reading this in the bath? | Explanation | Reference |
| Is it lists, tables, or technical specs? | Reference | Explanation |
| Does it answer "why?" questions? | Explanation | Reference |

## Applying Diataxis: Iterative approach

**Do NOT create empty structures.** Don't create `/tutorials`, `/how-to`, `/reference`, `/explanation` folders with nothing in them.

**Start small:**
1. Pick any existing documentation
2. Apply compass to determine what type it should be
3. Improve it according to that type's principles
4. Repeat

**Let structure emerge:** As you improve individual pieces, patterns will emerge that suggest organizational structure. The top-level structure forms from the inside out. For guidance on organizing the TOC, read `references/toc.md`.

## Documentation type references (load on demand)

- **[Tutorials](references/tutorials.md)** - Learning-oriented experiences enabling skill acquisition through guided practice
- **[How-to guides](references/how-to-guides.md)** - Task-oriented directions for accomplishing specific goals
- **[Reference](references/reference.md)** - Information-oriented technical descriptions for authoritative lookup
- **[Explanation](references/explanation.md)** - Understanding-oriented discussions providing context and answering "why?"
- **[Table of contents](references/toc.md)** - Guidance on organizing documentation topics within the TOC and adding cross-references

## Key principles

1. **Different contexts need different documentation** - Users learning need tutorials; users working need how-to guides or reference; users seeking understanding need explanation
2. **Separation of concerns** - Keep documentation types distinct to prevent confusion
3. **User-centered approach** - Consider what the user is trying to accomplish and in what context
4. **Iterative improvement** - Enhance documentation incrementally by applying Diataxis principles
5. **Purpose-driven structure** - Each type has specific characteristics that make it effective for its intended purpose