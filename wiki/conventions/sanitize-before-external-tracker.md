---
type: convention
tags: [security, sanitization]
Title: Sanitize Content Before Writing to an External Tracker
Sources: User instruction, 2026-07-03
Raw: "[../../raw/conventions/2026-07-03-sanitize-before-external-tracker.md](../../raw/conventions/2026-07-03-sanitize-before-external-tracker.md)"
Updated: 2026-07-03
---

# Sanitize Content Before Writing to an External Tracker

Before writing anything into an external tracker — a GitHub issue, a chat channel, a ticket, or any system outside the local repo/session — sanitize the content first.

## What to keep vs. strip

- Keep structural and diagnostic information: counts, dimensions, error messages, call paths, stack traces, timing.
- Strip raw data values, proprietary identifiers, and file paths that could leak project- or org-specific detail.

## Broader than name-scrubbing

This is broader than "don't leak names" — it also covers raw data payloads and path structure that can indirectly identify a project or organization even without naming it directly. An absolute file path can leak an org or project identity through its directory segments alone, even when no name ever appears in prose.

**Applies to:** GitHub issues/PRs, chat messages (Slack, Discord, etc.), support tickets, any content leaving the local working environment for a shared/external system.

## See Also

- [No Confidential Information in Code or Git History](no-confidential-leak.md) — narrower rule specifically about names of persons/orgs; this article extends it to data values and path structure
