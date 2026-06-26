---
source: https://github.com/session-reflection (wiki/acad-mediator/acad-mediator-conventions.md)
collected: 2026-06-27
published: 2026-06-25
---

A commit that removes or renames a script or tool does not reliably update doc references to it. After any such commit, grep docs (*.md, CLAUDE.md) for the old path/name before trusting those docs. When auditing for staleness generally, don't just check that referenced files exist — grep file content for paths/commands/env-vars and verify each. If a referenced mechanism is gone, check whether something replaced it and describe the replacement rather than just deleting the section.
