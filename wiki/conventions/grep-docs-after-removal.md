---
Title: Grep Docs for Stale References After Any Removal Commit
Sources: session-reflection, 2026-06-25
Raw: [../../raw/conventions/grep-docs-after-removal.md](../../raw/conventions/grep-docs-after-removal.md)
Updated: 2026-06-27
---

# Grep Docs for Stale References After Any Removal Commit

A commit that removes or renames a script does not reliably update doc references to it. After any such commit, grep `*.md` and `CLAUDE.md` for the old path/name before trusting those docs. Don't just check that referenced files exist — grep file content for paths/commands/env-vars and verify each. If a referenced mechanism is gone, check whether something replaced it and describe the replacement rather than just deleting the section.
