---
Title: Session Tool Efficiency
Sources: Session reflection, 2026-06-28
Raw: "[../../raw/lessons-learned/2026-06-28-file-state-tracking-and-readme-authoring.md](../../raw/lessons-learned/2026-06-28-file-state-tracking-and-readme-authoring.md); [../../raw/lessons-learned/2026-06-28-skill-file-location-and-responsibility.md](../../raw/lessons-learned/2026-06-28-skill-file-location-and-responsibility.md)"
Updated: 2026-06-28
---

# Session Tool Efficiency

Small habits that prevent wasted tool calls within a session.

## File state is tracked within a session — skip redundant Reads

The harness tracks which files have been read and whether anything has modified them since. If you Read a file and no intervening tool could have changed it, re-reading returns a "Wasted call" warning and adds nothing. Before issuing a Read, check whether the file is already in context from earlier in the same session.

Rule of thumb: Read once per file per session unless you have reason to believe the file changed (e.g., a Write, Edit, or Bash command targeted it in between).

## Use Write for full-file rewrites, Edit for targeted changes

- **Write** — replaces the entire file. Use when the structure changes substantially or the file is short enough that rewriting is cleaner than diffing.
- **Edit** — sends only a diff. Use for targeted, surgical changes to specific sections of an existing file.

Choosing the wrong tool is mostly a style issue for short files, but for long files, multiple Edit calls beat a single Write for both readability and safety — a failed Write discards everything, a failed Edit leaves the rest intact.

## Rejected tool calls leave files unchanged

When the user rejects an Edit or Write, the file is completely unmodified — the rejection is total, not partial. Don't chain a follow-up edit on top of a rejected one assuming any part of it landed. If unsure about the current file state after a rejection, re-read it before proceeding.
