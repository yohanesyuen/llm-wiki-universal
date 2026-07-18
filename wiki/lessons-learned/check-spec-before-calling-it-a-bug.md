---
type: lesson
tags: [audit, spec-compliance, subagent-verification, handoff]
Title: Check Whether the Spec Already Documents a Behavior as Intentional Before Calling It a Bug
Sources: Session reflection, 2026-07-18
Raw: "[../../raw/lessons-learned/2026-07-18-pm-audit-fix-handoff.md](../../raw/lessons-learned/2026-07-18-pm-audit-fix-handoff.md)"
Updated: 2026-07-19
---

# Check Whether the Spec Already Documents a Behavior as Intentional Before Calling It a Bug

An external symptom (a hardcoded value, an ignored parameter) can look identical whether it's an oversight or a documented design constraint — the tell is always in the contract/spec file, one grep away. Skipping that check turns a design decision into a false-positive "known bug" that then has to be walked back.

## What happened

A hardcoded pagination size was flagged as a defect based on an ad-hoc test where an unrecognized query parameter was silently ignored. The project's own API contract document explicitly specified that fixed page size as intentional — and the request-side type never even declared the parameter being tested. The mistake was only corrected when directly asked to explain the "bug," which prompted the re-check that should have happened before the original claim was made.

## A subagent's audit findings still need direct verification

A delegated audit returned several findings; each was re-read directly from the relevant source (schema defaults, an authorization guard's actual scope, exact database-query call sites) before writing any fix, rather than trusting the subagent's summary at face value. Treat this as a required step before opening issues or shipping fixes based on delegated findings, even when the subagent was explicitly told to be conservative.

## A handoff prompt needs a "confirmed absent" section

A self-contained handoff to a fresh session explicitly listed what was confirmed absent from the codebase (with citations), what NOT to touch (unrelated already-filed work), and the exact recent commit whose patterns must not be regressed. Recording dead-end searches up front means the next session doesn't have to re-run that search — the negative result is exactly as valuable to hand off as the positive ones.

## Root-causing a production crash from a bare error message

Given only a JS error and a route, the crash was traced to a UI library being initialized into a hidden (`display:none`) container — found by reading the library's actual internal call sites and cross-checking the diagnosis against the library's own documentation, not just pattern-matching the stack trace text.

## See Also

- [A Request Built on a False Premise Deserves a Correction, Not Silent Compliance or Refusal](false-premise-scoping-and-diff-before-git-reconcile.md) — sibling lesson on verifying assumed intent/state before acting
- [Verify a Subagent Handoff Actually Chains; Query the Structured Log for Live Metrics, Don't Estimate](verify-subagent-handoffs-and-query-structured-logs.md) — related discipline for trusting delegated work
