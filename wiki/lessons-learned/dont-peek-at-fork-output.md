---
type: lesson
tags: [agents, forking, context-window, efficiency]
Title: Don't Peek at a Fork's output_file
Sources: superpowers/using-superpowers skill, 2026-06-30
Raw: "[../../raw/lessons-learned/2026-06-30-dont-peek-at-fork-output.md](../../raw/lessons-learned/2026-06-30-dont-peek-at-fork-output.md)"
Updated: 2026-06-30
---

# Don't Peek at a Fork's output_file

When a fork agent is dispatched, the tool result includes an `output_file` path. Do **not** Read or tail that file while the fork is running. Reading the transcript mid-flight pulls the fork's raw tool noise into your context window — which defeats the entire point of forking.

Wait for the completion notification (it arrives as a user-role message). Trust it. The fork's summary is in the notification; you do not need to inspect the file.

## Why it matters

Forks keep their raw tool output out of the coordinator's context. Peeking at `output_file` re-ingests exactly what you were trying to avoid: every intermediate tool call, file read, and search the fork made. This fills your context with noise you won't need again and erases the efficiency gain.

## Pattern

```
✓ dispatch fork → wait for notification → read summary in notification
✗ dispatch fork → Read/tail output_file → proceed
```

## See Also

- [Session Tool Efficiency](session-tool-efficiency.md) — same principle applied to in-session tool calls: avoid redundant reads
- [Parallel Agent Waves Need a Build Gate](parallel-agent-build-gate.md) — related discipline around agent completion signals
- [Confirm Before Escalating to a Destructive Op; Serialize Shared Writes; Background Long Jobs](destructive-op-confirmation-and-background-jobs.md) — same "wait for notification, don't poll" discipline applied to backgrounded shell jobs
- [Fork Resumption Is Unreliable for "Spawn, Then Follow Up" Patterns](fork-resumption-follow-up-unreliable.md) — a second fork-handling failure mode: forks can reject legitimate follow-up messages after their initial return
