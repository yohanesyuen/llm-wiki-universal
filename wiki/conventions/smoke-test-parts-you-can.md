---
type: convention
tags: [testing]
Title: Smoke-Test the Parts You Can
Sources: session-reflection, 2026-06-25; Session reflection, 2026-07-06
Raw: "[../../raw/conventions/smoke-test-parts-you-can.md](../../raw/conventions/smoke-test-parts-you-can.md), [../../raw/lessons-learned/2026-07-06-cross-session-repo-cleanup.md](../../raw/lessons-learned/2026-07-06-cross-session-repo-cleanup.md)"
Updated: 2026-07-06
---

# Smoke-Test the Parts You Can

"Can't test the live integration" doesn't excuse skipping verification of the parts that don't need it. A pure parsing/transform function with non-obvious edge cases deserves a cheap, dependency-free smoke test — a one-line inline call against each known input shape — before the work is reported done. Type-checking and compile-checks only prove the file parses; they say nothing about whether a non-obvious branch is correct.

The same principle extends to config/path changes: editing a bind-mount source or a pointer to a moved directory only proves the edit is textually correct. If something (a container, a running process) resolved that path once at startup, the change isn't verified until that consumer is recreated/restarted and inspected directly — see [Git History Scrubbing Has Two Leak Surfaces; a Moved Mount Isn't Done Until the Consumer Restarts](../lessons-learned/git-history-scrubbing-and-mount-verification.md).

## See Also

- [Git History Scrubbing Has Two Leak Surfaces; a Moved Mount Isn't Done Until the Consumer Restarts](../lessons-learned/git-history-scrubbing-and-mount-verification.md) — same principle applied to a moved bind mount
