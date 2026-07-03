---
type: convention
tags: [security, sanitization, git]
Title: No Confidential Information in Code or Git History
Sources: "User instruction"
Raw: "[../../raw/conventions/no-confidential-leak.md](../../raw/conventions/no-confidential-leak.md), [../../raw/conventions/2026-07-03-sanitize-before-external-tracker.md](../../raw/conventions/2026-07-03-sanitize-before-external-tracker.md)"
Updated: 2026-07-03
---

# No Confidential Information in Code or Git History

Never include names of persons or organizations in source code, commit messages, PR descriptions, or GitHub issue content.

Git history is permanent and hard to purge. Use placeholders — `<organization>`, `User A`, `client` — whenever a stand-in is needed.

## Broader than name-scrubbing

The same discipline applies to anything else written to a system outside the local repo/session — a GitHub issue, a chat channel, a ticket, or any external tracker:

- Keep structural and diagnostic information: counts, dimensions, error messages, call paths, stack traces, timing.
- Strip raw data values, proprietary identifiers, and file paths that could leak project- or org-specific detail — even when no name ever appears in prose. An absolute file path can leak an org or project identity through its directory segments alone.

**Applies to:** source code, inline comments, commit messages, PR titles/bodies, issue messages, chat messages (Slack, Discord, etc.), support tickets, any content leaving the local working environment for a shared/external system.

## See Also

- [Never Read Secret Values Into Agent Context](never-expose-secrets-to-agent-context.md) — same spirit applied to secret values, but stricter: it gates reading into the agent's context at all, not just writing out to an external system
