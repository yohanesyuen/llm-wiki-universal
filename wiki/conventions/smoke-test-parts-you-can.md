---
Title: Smoke-Test the Parts You Can
Sources: session-reflection, 2026-06-25
Raw: [../../raw/conventions/smoke-test-parts-you-can.md](../../raw/conventions/smoke-test-parts-you-can.md)
Updated: 2026-06-27
---

# Smoke-Test the Parts You Can

"Can't test the live integration" doesn't excuse skipping verification of the parts that don't need it. A pure parsing/transform function with non-obvious edge cases deserves a cheap, dependency-free smoke test — a one-line inline call against each known input shape — before the work is reported done. Type-checking and compile-checks only prove the file parses; they say nothing about whether a non-obvious branch is correct.
