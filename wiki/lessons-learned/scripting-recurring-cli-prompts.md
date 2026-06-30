---
type: lesson
tags: [scripting, cli, automation, shell-history, chat-history]
Title: Scripting Recurring CLI Prompts
Sources: Session reflection, 2026-06-29
Raw: "[../../raw/lessons-learned/2026-06-29-script-recurring-cli-prompts.md](../../raw/lessons-learned/2026-06-29-script-recurring-cli-prompts.md); [../../raw/lessons-learned/2026-06-29-claude-chat-history-as-repetition-source.md](../../raw/lessons-learned/2026-06-29-claude-chat-history-as-repetition-source.md)"
Updated: 2026-06-29
---

# Scripting Recurring CLI Prompts

How to find and automate a command pattern that's been typed or requested several times, without over- or under-scripting.

## Use shell history AND Claude chat history as evidence, not memory

Don't guess at how often something has been done — check two sources, not one:
- **Shell history** (`.zsh_history` / `.bash_history`) for commands the user typed directly. Grep for the literal *shape* of the recurring command — match the constant scaffold (e.g. `qwen-code -p "Evaluate @`), not the full string, since variable parts (filenames, flags) differ between occurrences.
- **Claude chat/session histories** for recurring requests made *to* Claude rather than typed as raw shell commands. A pattern can repeat entirely inside chat sessions — the same kind of multi-step ask, phrased similarly, with Claude issuing the underlying tool calls each time — and that repetition leaves no trace in shell history at all. Search past session transcripts/logs for repeated request shapes to catch these.

Both sources are necessary, not interchangeable: shell history misses delegated work, and chat history misses commands the user runs themselves outside of Claude.

## Only script patterns where the variable part is isolable

A repeated command is worth wrapping in a script only when:
- The scaffold (constant text) is identical or near-identical across occurrences, and
- The parts that differ (a filename, a flag, a target) can be cleanly captured as script arguments.

If the "variation" is actually a different task each time, it isn't a repeated pattern — it's coincidental surface similarity, and scripting it would hardcode the wrong assumption.

## Trivial single commands don't qualify

High-frequency single commands (`cd`, `ls`, `git status`) are not "sub-tasks" even if they appear dozens of times in history — they're already as short as they can be. The bar for proposing a script is a multi-token command or prompt template with a constant scaffold plus a variable slot, where the scaffold is long/error-prone enough that re-typing it has real cost.

## Wrapper script conventions

- `#!/bin/sh` shebang, a one-line purpose comment, a `Usage:` comment.
- Derive defaults for optional args rather than requiring every flag.
- End with `exec` into the underlying tool/binary rather than a bare call — this propagates signals and exit codes correctly and avoids leaving an extra shell process around.

## See Also

- [Session Tool Efficiency](session-tool-efficiency.md) — similar theme of cutting repeated/wasted work, but at the level of in-session tool calls rather than cross-session shell commands.
