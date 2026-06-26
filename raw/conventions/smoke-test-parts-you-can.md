---
source: https://github.com/session-reflection (wiki/meta/claude-code-agent-workflow-lessons.md)
collected: 2026-06-27
published: 2026-06-25
---

"I can't test the live integration" doesn't excuse skipping verification of the parts that don't need that integration. A pure parsing/transform function with non-obvious edge cases deserves a cheap, dependency-free smoke test — a one-line inline call against each known shape — before the work is reported done, even when the larger feature genuinely can't be exercised end-to-end. Type-checking and py_compile only prove the file parses; they say nothing about whether a non-obvious branch is correct.
