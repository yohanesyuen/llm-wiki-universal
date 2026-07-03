---
type: convention
tags: [security, git]
Title: No Confidential Information in Code or Git History
Sources: User instruction
Raw: "[../../raw/conventions/no-confidential-leak.md](../../raw/conventions/no-confidential-leak.md)"
Updated: 2026-07-03
---

# No Confidential Information in Code or Git History

Never include names of persons or organizations in source code, commit messages, PR descriptions, or GitHub issue content.

Git history is permanent and hard to purge. Use placeholders — `<organization>`, `User A`, `client` — whenever a stand-in is needed.

**Applies to:** source code, inline comments, commit messages, PR titles/bodies, issue messages.

## See Also

- [Sanitize Content Before Writing to an External Tracker](sanitize-before-external-tracker.md) — broader rule covering raw data values and path structure, not just names
