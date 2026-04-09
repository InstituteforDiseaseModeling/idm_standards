# Processes

The processes listed here can help projects achieve the guidelines listed above. In fact, [studies have shown](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10372494) that "process-based metrics are more predictive of defects than code quality metrics." However, as above, the processes should always be in service of the project and its aims, and should never become a burden; not all processes are applicable to all projects.

1. **Project planning & design**  
   1. Identify project scope, project goals, and audience, with clearly defined success criteria.  
   2. Identify a prioritized list of user stories and functional requirements.  
   3. Decide project timeline and determine resources required.  
   4. Create feature roadmap.  
   5. Decide and implement project structure, including:  
      1. Roles & responsibilities, including software/research leads and project manager  
      2. Repository location and conventions (e.g., public vs. private, branch vs. fork)  
      3. Docs setup (e.g. MkDocs, Quarto)  
      4. Communication platform and approach (e.g. Teams channels, Slack, GitHub))  
      5. Cadence for meetings and async updates  
2. **Project workflow**  
   1. Engineers and researchers talk frequently and are in sync on plans.  
   2. Issues, next steps, and progress are documented in a consistent, accessible place (e.g. GitHub project board or shared doc).  
   3. Risks and dependencies are identified and tracked.  
   4. Code is delivered on time (both in terms of need and promises made).  
3. **Code development**  
   1. Code uses test-driven or docs-driven development where possible; if the code is written first, the docs and tests are written immediately after.  
   2. Code follows the project's style guide.  
   3. Where possible, perform automatic linting to ensure consistency with the style guide.  
   4. Developers use the IDE of their choice (e.g. RStudio, VS Code, Cursor, PyCharm, Spyder, Neovim), and leverage AI integration where possible.  
   5. Developers use a modern environment manager of their choice (conda, uv, or none).  
4. **Code reviews**  
   1. All code is submitted via PR (for Tier 1 and 2 projects; optional for Tier 3 projects).  
   2. PRs are small and focused (aim for \<100 lines), except when major new features are being introduced.  
   3. PRs are reviewed by at least one other person (and optionally also an AI) prior to merge.  
   4. PR reviews are timely, thorough, honest, and polite.  
5. **Launch**  
   1. All stakeholders review the project and confirm that it meets its success criteria.  
   2. The full codebase is reviewed by an engineer and AI tool against the quality guidelines.  
   3. Docs are reviewed by the content team for clarity and completeness.  
   4. Code is easy to find and use on GitHub ("main" branch, not long-lived feature branches).  
   5. Code is pushed to an industry standard repository (e.g. PyPI, CRAN) where appropriate.  
   6. Where applicable, the project is paired with an AI tool (plugin, MCP server, or chatbot).  
   7. Where applicable, the project is paired with a dedicated website.  
   8. Where applicable, the launch is publicized via social media, websites, and announcements.  
6. **Maintenance**  
   1. Technical debt is proactively managed.  
   2. Releases are frequent, especially if bugs are found.  
   3. Code and docs are always kept in sync.  
   4. Users' questions and bugs are addressed promptly (first response \<24 h).