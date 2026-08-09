---
type: convention
tags: [context-efficiency, session]
title: Targeted Grep Over Reading Full Sibling Files
sources: session-reflection, 2026-06-25
raw: "[../../raw/conventions/targeted-grep-over-full-reads.md](../../raw/conventions/targeted-grep-over-full-reads.md)"
updated: 2026-06-27
---

# Targeted Grep Over Reading Full Sibling Files

When the question is specific ("is convention X used elsewhere?"), grep for the specific signal — a dispatcher table, an import line, a decorator — rather than reading entire sibling files end-to-end. Reading large files in full to answer a question a single targeted grep would have resolved is avoidable context cost.
