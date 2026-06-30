---
type: lesson
tags: [tooling, docs, llm, cli]
Title: Verify CLI Install Commands from Official Docs
Sources: Session reflection, 2026-06-29
Raw: "[../../raw/lessons-learned/2026-06-29-verify-cli-install-from-docs.md](../../raw/lessons-learned/2026-06-29-verify-cli-install-from-docs.md)"
Updated: 2026-06-29
---

# Verify CLI Install Commands from Official Docs

## Never Write an Install Command from Memory

Install commands (package manager, registry name, binary name, flags) are highly specific to each tool and change between releases. Training-data priors about "how tools are usually installed" will produce plausible-looking but wrong commands.

Before writing any install snippet for a CLI tool, fetch the official README or install guide:

```
ctx_fetch_and_index(url: "<repo>/README.md") → ctx_search(queries: ["install", "prerequisites"])
```

Two tool calls answer: which package manager, which package name, and what the binary is called.

## A Rejected Edit with a Doc Pointer Is a Research Task, Not a Rewrite Task

When an edit is rejected with "check the docs / check the README," the error is factual — not stylistic. Rephrasing the same guess will produce the same wrong answer.

The correct response:
1. Fetch the referenced documentation
2. Extract the exact install command and binary name
3. Only then write the edit

## Package Manager ≠ Language Assumption

A tool living in a GitHub repo does not default to npm, pip, or brew based on its apparent domain. Verify the ecosystem from the README prerequisites section.

Example: a general-purpose developer CLI might use `uv` (Python tool manager) while having nothing to do with Python from the user's perspective — the README prerequisites section is the only authoritative source.

## See Also

- [Pre-Flight Checks Before Building](preflight-checks-before-building.md) — related pattern: verify architecture/config before investing in a stack
