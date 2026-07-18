---
type: lesson
tags: [multi-agent, verification, workflow-orchestration]
Title: A Subagent's Self-Report Is a Claim, Not a Verification
Sources: Session reflection, 2026-07-18
Raw: "[../../raw/lessons-learned/2026-07-18-multi-agent-workflow-verification.md](../../raw/lessons-learned/2026-07-18-multi-agent-workflow-verification.md)"
Updated: 2026-07-19
---

# A Subagent's Self-Report Is a Claim, Not a Verification

Even when a multi-agent workflow includes its own review-agent stage, the orchestrator should independently re-run the actual verification commands (tests, typecheck) and read the actual diff for any flagged critical finding — especially when everything reportedly passed, since that's precisely when it's easiest to skip the check.

## Evidence-based pushback before building

Before implementing a request that implied finer granularity than the underlying data model actually stored, the real schema and real UI capabilities were checked first, and the request was plainly said to rest on a false premise — rather than faking a result that would silently fail.

## Treat a confused resumed fork as terminal, not recoverable with a nudge

A forked/delegated subagent got confused about its own role when resumed mid-task and produced more confusion instead of useful output on a second nudge. The fork inherits full parent context, which can bleed ambiguity from the parent conversation into a confused "who am I" reply. For cheap tasks, the first confused reply should be treated as a signal to abandon that path and do the task directly, rather than spending another round-trip trying to recover it.

## Diagnose concurrent-edit collisions with concrete evidence

An unexpected concurrent-edit collision was diagnosed using process list and git commit metadata rather than guessing, then confirmed via a direct message to the other active process. Turning "something changed unexpectedly" into a specific, checkable claim resolves ambiguity in one step instead of several rounds of guessing.

## Self-application is a workflow step, not an afterthought

Subagents completed real implementation work but left status-tracking bookkeeping unfinished, and a related dogfooding step (using the new feature on the project's own tracking data) was missed entirely until pointed out. Self-applying a newly built capability to a project's own tracking/meta-data should be a scripted step of the workflow, not a separate manual follow-up.

## See Also

- [Verify a Subagent Handoff Actually Chains; Query the Structured Log for Live Metrics, Don't Estimate](verify-subagent-handoffs-and-query-structured-logs.md) — sibling lesson on not assuming subagent coordination worked
- [Fork Resumption Is Unreliable for "Spawn, Then Follow Up" Patterns](fork-resumption-follow-up-unreliable.md) — earlier instance of the same resumed-fork confusion risk
