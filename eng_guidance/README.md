# IDM engineering guidance

This repository contains style and community guidelines for IDM projects. The engineering guidance is divided into the following sections:

1. [Design philosophy](1_philosophy.md): common tasks should be simple, audience is scientists, and workload/readability matter.
2. [Python style](2_python.md): Google style plus house rules, including no type annotations, longer lines, etc.
3. [Testing](3_tests.md): focus on scientific correctness, and support triple execution (standalone scripts + pytest + GitHub Actions).
4. [Documentation](4_documentation.md): readmes, auto-generated API reference, and tutorials.
5. [Other principles](5_other.md): for example, be very careful not include sensitive data in repos.
6. [Zen of IDM](6_zen.md): short principles and credos for research and software (simplicity, docs, tests, change).

Note: although not part of the engineering guidance, the [IDM software engineering quality guidelines](engineering_quality_guidelines.md) are also included here for completeness. The engineering guidance and the engineering quality guidelines together give a (pretty) complete picture of what good IDM code looks like.

*Version: 2.1 | Last updated: 2026-04-02*