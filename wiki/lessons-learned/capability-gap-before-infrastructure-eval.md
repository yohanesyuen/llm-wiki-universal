---
Title: Name the Capability Gap Before Evaluating New Infrastructure
Sources: Session reflection, 2026-06-28
Raw: "[../../raw/lessons-learned/2026-06-28-mcp-conversion-eval.md](../../raw/lessons-learned/2026-06-28-mcp-conversion-eval.md)"
Updated: 2026-06-28
---

# Name the Capability Gap Before Evaluating New Infrastructure

When asked "should we wrap X as a server/protocol," the right answer depends entirely on which client environments need to use X. Evaluating against the wrong baseline — e.g. "this user already has zero-cost local access" — produces a confident but incomplete answer if a different client (one without that access) is the actual reason the question came up.

## The pattern

1. A tool already works well in its native environment (e.g., a filesystem-native knowledge base that a coding agent reads/writes directly via git).
2. Someone asks whether to add a server/protocol layer around it.
3. The instinctive answer is "no — you already have free, simple access," which is correct *for that one environment*.
4. The real trigger turns out to be a different client surface that lacks that access entirely (e.g., a web-based session with no filesystem). The infrastructure question reframes completely once that's named.

Ask early which client surfaces must be supported (filesystem vs. none, local vs. remote) before recommending for or against new infrastructure. The cost/benefit of the same proposal can flip entirely depending on the answer.

## Order remedies by cost, not by generality

Once a real gap is confirmed, don't jump to the most general fix (build a bespoke server). Rank options cheapest-to-heaviest and recommend trying the cheapest first:

1. **Reuse an existing remote connector** if the underlying asset is already (or could be) hosted somewhere with a connector that solves the gap directly (e.g., a git-hosting API/MCP connector for a git-backed asset). Zero new code.
2. **Build a custom remote server** only if the existing connector's interface is too coarse for the actual workflow. This re-implements transport and likely still shells out to the same underlying system (e.g., git) underneath.
3. **Tunnel the local environment** to the remote client as a last resort — avoids re-hosting content elsewhere but adds an always-on tunnel to trust and maintain.

Building a bespoke server before checking for an existing connector is the most common over-engineering trap here: it re-implements a transport layer that already exists elsewhere for no new capability.

## Verify the asset's actual shape before evaluating it

Before reasoning about whether to wrap something, check what it actually is rather than inferring from its name or README. A quick check (e.g. `gh api repos/<owner>/<repo>` plus the contents endpoint) can reveal that a repo is, say, an Agent Skill (filesystem-native, git-backed) rather than a generic library or service — and that distinction changes which of the above remedies apply.

## See also

- [Wiki Ingest and Cleanup Discipline](wiki-ingest-and-cleanup-discipline.md)
