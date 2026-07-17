---
type: lesson
tags: [subagents, observability, orchestration]
Title: Verify a Subagent Handoff Actually Chains; Query the Structured Log for Live Metrics, Don't Estimate
Sources: Session reflection, 2026-07-09
Raw: "[../../raw/lessons-learned/2026-07-09-parallel-subagent-ingest.md](../../raw/lessons-learned/2026-07-09-parallel-subagent-ingest.md)"
Updated: 2026-07-09
---

# Verify a Subagent Handoff Actually Chains; Query the Structured Log for Live Metrics, Don't Estimate

When one subagent's task is supposed to produce an artifact that a second subagent then consumes, "both finished" is not the same claim as "they worked together" — and for live operational metrics, a structured log sink beats reasoning from the visible conversation.

## An explicit interop check, not an assumed one

Two independently-decoupled tasks (a build task with no dependency on an ingest task) are correctly run as parallel background agents — that's the right call when they genuinely don't depend on each other. But when one agent's output *is* meant to feed another (a build-this-tool, then use-that-tool-elsewhere pattern), "do X in a subagent, then use X in another" needs an explicit interop check: either sequence them and pass the concrete artifact path as required input to the consumer, or accept they ran in parallel and state plainly that interop wasn't verified. Two deliverables completing independently should never be reported as if the wiring between them was demonstrated when it wasn't.

## Query the structured log sink for live metrics, not the transcript

When asked about a live operational metric (context usage, cost, token split), the authoritative answer comes from a structured log/telemetry sink (e.g. a statusline event stream), sorted by time descending for the newest record — not from estimating against the visible conversation. First inspect one representative record's fields before writing a precise filter; a broad free-text OR search over a log store tends to return echoed prompt text rather than the metric itself, costing extra round-trips that a quick schema check up front avoids.

## A subagent's token spend is not included in the parent's own metric

A main-loop usage metric typically reflects only the orchestrating session; subagents run on separate transcripts and their cost has to be added manually (from their own completion messages) for a true total. When reporting a usage figure, note explicitly whether it includes subagent spend or is orchestrator-only.

## Hold input for a task until its required input actually arrives

When a task's necessary input hasn't arrived yet (e.g. "ingest the next thing I paste"), launch any independent, ready-to-start task immediately and park the input-dependent one rather than guessing or proceeding on incomplete information — a clean separation of "can start now" from "needs input first."

## See Also

- [Don't Peek at a Fork's output_file](dont-peek-at-fork-output.md) — a companion discipline for background/forked agent work: trust the completion notification rather than reading intermediate state
- [Fork Resumption Is Unreliable for "Spawn, Then Follow Up" Patterns](fork-resumption-follow-up-unreliable.md) — a related pitfall when a background agent needs a second round of interaction after its first return
