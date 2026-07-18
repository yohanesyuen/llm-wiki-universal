---
type: lesson
tags: [vendor-library, debugging, git-worktree, concurrent-editing]
Title: Grep the Vendor's Compiled Source for Real Event Wiring Before Guessing at a Fix
Sources: Session reflection, 2026-07-18
Raw: "[../../raw/lessons-learned/2026-07-18-vendor-lib-source-diagnosis-isolated-push.md](../../raw/lessons-learned/2026-07-18-vendor-lib-source-diagnosis-isolated-push.md)"
Updated: 2026-07-19
---

# Grep the Vendor's Compiled Source for Real Event Wiring Before Guessing at a Fix

When a third-party UI library "silently doesn't work" on some input class (touch, a different browser, a device), grep its actual compiled/shipped bundle for the event types it wires up before hypothesizing about CSS or app-level causes. Docs and TypeScript types describe the *intended* surface; the compiled bundle is the only reliable source for what's *actually* listened for.

## The pattern that found the real bug

A mobile drag-to-pan interaction silently did nothing. Rather than guessing at a `touch-action` CSS fix, grepping the installed dependency's compiled bundle for its `addEventListener` calls showed the library only ever listened for `mousemove`/`wheel`, never any touch event, in any shipped version — turning a vague bug into a precise, cited root cause before writing a line of fix code.

## Read the whole conditional, not just the line that handles the symptom

A follow-up bug ("vertical scroll doesn't work") traced to the same vendor function already read for the first patch — an `if (event.deltaX) { ... } else { ... }` branch meant any synthetic event carrying both deltaX and deltaY (which real finger movement almost always produces) always took the horizontal branch. The axis-priority bug was sitting in the same function already being read to build the first fix; reading only enough source to make the immediate symptom go away, rather than the whole relevant function, cost a second bug report.

## An isolated detached worktree is the safe move around a concurrent editor

When a routine commit's push was rejected because the remote had moved, `git status` revealed another concurrent session's uncommitted, unrelated changes sitting in the same working tree. Rather than running any repo-wide `pull`/`merge`/`rebase` (any of which risk touching or stashing someone else's in-flight work), a fully isolated detached `git worktree` was created at the one commit that needed to move, rebased and pushed from there, and removed afterward — guaranteeing zero risk to the other session's dirty files at the cost of a few extra commands.

## Log a bypassed approval gate at the same layer the gate lives in

When asked to bypass a documented human-approval gate on a stakeholder's informal go-ahead, the spec file itself was updated to record why the gate was being bypassed (a verbal go-ahead, not a formal one) as part of the same change — giving the bypass an audit trail instead of letting it vanish into a commit message.

## See Also

- [A Request Built on a False Premise Deserves a Correction, Not Silent Compliance or Refusal](false-premise-scoping-and-diff-before-git-reconcile.md) — sibling git-reconciliation lesson (diff-before-rebase) from the same project window
- [Check Bundle Budget as Part of the Initial Library Comparison, Not After Implementation](bundle-budget-check-before-library-migration.md) — same session's earlier vendor-library research (license verification) for the same feature area
