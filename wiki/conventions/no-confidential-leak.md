---
type: convention
tags: [security, git]
Title: No Confidential Information in Code or Git History
Sources: User instruction
Raw: "[../../raw/conventions/no-confidential-leak.md](../../raw/conventions/no-confidential-leak.md)"
Updated: 2026-06-27
---

# No Confidential Information in Code or Git History

Never include names of persons or organizations in source code, commit messages, PR descriptions, or GitHub issue content.

Git history is permanent and hard to purge. Use placeholders — `<organization>`, `User A`, `client` — whenever a stand-in is needed.

**Applies to:** source code, inline comments, commit messages, PR titles/bodies, issue messages.
