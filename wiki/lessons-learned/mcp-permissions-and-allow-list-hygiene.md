# MCP Permissions and Allow List Hygiene

**Topic**: lessons-learned
**Updated**: 2026-06-28

---

## MCP Permission Syntax Is Different from Bash

Bash rules use parentheses with interior wildcards: `"Bash(git *)"`.
MCP rules use no parentheses at all: `"mcp__server__tool"` or `"mcp__server__*"` for all tools on a server.

Mixing the two patterns either fails immediately (the settings validator catches it) or silently does nothing. Always use the `mcp__server__*` form for MCP tools — never wrap in parentheses.

**The settings validator gives actionable error messages.** When a settings write is rejected, the error output includes the exact correct syntax. Read it before guessing.

---

## Allow Lists Accumulate Noise by Default

Every new permission prompt that gets approved adds one entry. Without periodic review, the list fills with:

- **Redundant entries**: a specific subdirectory path when a parent `/**` glob already covers it
- **One-time commands**: exact commands with hardcoded data from investigations that will never recur — `find / -iname "compile-wiki.py"`, `__CMDSUB_OUTPUT__` artefacts, specific `mkdir` for a test scaffold

### Two-Pass Cleanup

1. **Redundant pass**: remove any entry where a broader glob already in the list covers it
2. **One-time pass**: remove exact commands that were approved for a specific investigation and have no recurring use

Doing both at once is harder to reason about; separate passes keep the logic clean.

---

## Prefer Pattern Entries Over Instance Entries

`"Bash(pip3 show *)"` is more durable than five specific `pip3 show <package>` approvals. When approving a recurring workflow at a prompt, consider whether the glob form is more appropriate than the exact command.

---

## Verification Before Claiming Success

For MCP connections specifically: make a real API call to confirm authentication and data return, not just "the server is connected". A live query (e.g., `search_repositories`) is the right bar.

---

*Sources: session-reflection 2026-06-28*
