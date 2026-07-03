---
source: user-instruction
collected: 2026-07-03
---

# Sanitize Content Before Writing to an External Tracker

Before writing anything into an external tracker (a GitHub issue, a chat channel, a ticket, or any system outside the local repo/session), sanitize the content first:

- Keep structural and diagnostic information: counts, dimensions, error messages, call paths, stack traces, timing.
- Strip raw data values, proprietary identifiers, and file paths that could leak project- or org-specific detail.

This is broader than "don't leak names" (see the no-confidential-info convention) — it also covers raw data payloads and path structure that can indirectly identify a project or organization even without naming it directly.

**Applies to:** GitHub issues/PRs, chat messages (Slack, Discord, etc.), support tickets, any content leaving the local working environment for a shared/external system.
