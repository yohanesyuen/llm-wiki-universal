---
source: superpowers/using-superpowers skill (loaded via plugin)
collected: 2026-06-30
published: Unknown
---

# Don't Peek at a Fork's output_file

When a fork agent is dispatched, the tool result includes an `output_file` path. Do not Read or tail that file while the fork is running. Reading the transcript mid-flight pulls the fork's raw tool noise into your context window, which defeats the entire point of forking (keeping that output out of context).

The completion notification arrives as a user-role message in a later turn. Trust it — wait for the notification, then act on the result. You do not need to poll or inspect the file to know when the fork is done.

## Why it matters

Forks are cheap because they share the prompt cache and keep their raw tool output out of the coordinator's context. Peeking at `output_file` mid-flight re-ingests exactly what you were trying to avoid: every intermediate tool call, file read, and search result the fork made. This fills your context window with noise you won't need again and erases the efficiency gain.

## Rule

- Dispatch fork → wait for notification → read the fork's summary in the notification.
- Never: dispatch fork → Read/tail `output_file` → proceed.
