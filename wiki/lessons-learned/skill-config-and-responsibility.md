---
Title: Skill Configuration and Responsibility Boundaries
Sources: Session reflection, 2026-06-28
Raw: "[../../raw/lessons-learned/2026-06-28-skill-file-location-and-responsibility.md](../../raw/lessons-learned/2026-06-28-skill-file-location-and-responsibility.md)"
Updated: 2026-06-28
---

# Skill Configuration and Responsibility Boundaries

Rules for locating, editing, and reasoning about skill files in a multi-skill Claude Code setup.

## The skill base directory is ground truth for its SKILL.md

Every skill invocation prints a header: `Base directory for this skill: <path>`. The SKILL.md to read or edit is always `<path>/SKILL.md`. Do not search for skill files by keyword — you will find stale marketplace copies, plugin snapshots, or documentation mirrors that are not the active file. Only the path in the invocation header is authoritative.

## Format and behavior specs belong in the skill that does the work

When skill A delegates to skill B, any spec about *how B behaves* (output format, file naming, log entry format) belongs in B's SKILL.md — not in A's. A's only job is to say "invoke B." If the format spec lives in A, it will drift out of sync as B evolves, and B won't know about it.

Concrete example: the log entry format for `wiki/log.md` belongs in `karpathy-llm-wiki` SKILL.md, not in `reflect` SKILL.md, because karpathy-llm-wiki is the skill that writes the log.

## Each skill owns a clearly scoped output boundary

The `reflect` skill's output is `raw/lessons-learned/YYYY-MM-DD-slug.md` and nothing else. The `karpathy-llm-wiki` skill owns everything downstream: compiling the wiki article, updating `wiki/index.md`, and appending to `wiki/log.md`. Crossing those boundaries (e.g., reflect manually updating the index) duplicates work and creates inconsistencies when the delegated skill later runs with different conventions.

See also: [Session Tool Efficiency](session-tool-efficiency.md)
