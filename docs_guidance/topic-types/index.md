# Topic types and structure

IDM documentation borrows much of the guidance from the [Diátaxis](https://diataxis.fr/) framework, which classifies each topic within the documentation into four distinct topic types based on what the reader needs:

+-------------+-----------------------+-----------------------+
|             |  ACQUISITION          |    APPLICATION        |
|             |  (Study)              |    (Work)             |
+-------------+-----------------------+-----------------------+
|             |                       |                       |
|  ACTION     |  TUTORIAL             |    HOW-TO             |
|  (Doing)    |  (Learning-oriented)  |    (Task-oriented)    |
|             |                       |                       |
+-------------+-----------------------+-----------------------+
|             |                       |                       |
|  COGNITION  |  EXPLANATION          |  REFERENCE            |
|  (Knowing)  |  (Understanding-      |  (Information-        |
|             |    oriented)          |     oriented)         |
+-------------+-----------------------+-----------------------+

- **[Tutorial](tutorial.md)** -- Learning-oriented experiences that guide a beginner through a series of steps to build skills and confidence.
- **[How-to](howto.md)** -- Task-oriented directions that help a practitioner accomplish a specific goal.
- **[Reference](reference.md)** -- Information-oriented technical descriptions for looking up specifications, parameters, and APIs.
- **[Explanation](explanation.md)** -- Understanding-oriented discussions that provide context, background, and answer "why?" questions.

Each topic type serves a different user need. Focusing each individual topic on a single user need makes the documentation as a whole easier to navigate, write, and maintain. All topics should aim to be self-contained and describe a single subject, linking away to related topics but not duplicating their content. When content must appear in multiple topics (such as common warnings), create a snippet of reusable text rather than duplicating that content.

How you organize and group individual topics into the table of contents should follow the typical user journey. Generally, place API reference and tutorials as top-level sections in the TOC and group explanation and how-to topics into "user guides." See [table of contents](toc.md) for detailed guidance on organizing topics within your documentation's TOC.