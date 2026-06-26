---
Title: Wiki Ingest and Cleanup Discipline
Sources: Session reflection, 2026-06-27
Raw: [../../raw/lessons-learned/2026-06-27-universal-wiki-setup.md](../../raw/lessons-learned/2026-06-27-universal-wiki-setup.md)
Updated: 2026-06-27
---

# Wiki Ingest and Cleanup Discipline

Lessons from the universal wiki bootstrap session (2026-06-27): importing rules from a project-specific wiki, wiring up the reflect→ingest flow, and restructuring skills.

## One concept per article, regardless of source co-location

When ingesting multiple rules or lessons from a single source file, create one raw file and one wiki article per concept — not one file per source. Batching by source origin violates the "one concept per page" principle and forces a split later. This applies equally to wiki articles and raw ingest files.

See also: [conventions/](../conventions/) articles, all created one-per-concept.

## "Clean up" means content files, not config directories

When asked to clean up auto-generated files from a tool (Obsidian, IDE, etc.), remove only generated *content* files. Config directories (`.obsidian/`, `.git/`, `.vscode/`, etc.) are intentional and should be left alone unless explicitly named for removal. When in doubt, list what will be deleted and confirm before acting.

## Check for self-referential staleness within the same session

When a session modifies a skill, rule, or reference that is itself cited elsewhere (e.g. renaming a skill from `/handbook-extras:reflect` to `/reflect`), grep for old references before closing out the work. A stale reference written in the same session it was superseded is the most embarrassing kind.

## Effective patterns from this session

- **`gh api repos/.../contents`** — browse GitHub repo structure without WebFetch auth issues. Recursive flag (`-F recursive=1`) may 404 on some repos; fall back to directory-by-directory listing.
- **Numbered ranked list with emojis** — for multi-turn selection flows, a numbered + ranked list lets the user pick by index across turns without re-explaining context. Rankings reduce the user's cognitive load when prioritizing.
- **Incremental import loop** — show full candidate list → user picks → ingest → re-list remaining. Clean multi-turn pattern for selective knowledge transfer.
