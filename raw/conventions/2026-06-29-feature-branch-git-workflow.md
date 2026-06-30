---
Source: internal project CLAUDE.md / GIT_WORKFLOW.md
Collected: 2026-06-29
Published: Unknown
---

# Feature-Branch Git Workflow for AI-Assisted Development

## Branching

All work happens on a feature branch, never directly on `master`/`main`:

1. Create branch: `git checkout -b <type>/<issue>-<short-desc>` (e.g. `feat/100-new-feature`, `fix/121-coercion`).
2. Do all commits on this branch.
3. Push and create PR: `git push -u origin <branch>` then open a PR referencing the issue.
4. Merge immediately if no conflicts: squash merge + delete branch.
5. After merge: `git checkout master && git pull`.

## Issue Tracking

Every commit must reference a GitHub issue:

1. Check if a relevant issue exists before starting.
2. If none, create one: `gh issue create --title "<type>(<scope>): <summary>" --label "<labels>"`.
3. Reference in commit message: `type(scope): short summary (#<issue>)`.
4. Use `Closes #<issue>` in PR body.

## Commits

- Stage only changed files — never `git add .` / `git add -A`.
- Conventional-commit messages: `type(scope): short summary (#<issue>)`.
- Push immediately after committing.
- One coherent unit of work per commit. Multiple independent changes get separate commits.

## Auto-commit on Agent Stop

Before an agent session ends, if uncommitted tracked changes exist:

1. Run the project's test suite.
2. If tests pass: stage, commit (with issue ref), and push.
3. If tests fail: do NOT commit — leave unstaged and report.

## Staying Current

Before starting any new work:

1. `git fetch origin`
2. If the local branch is behind origin: pull or rebase as appropriate.
3. If on a feature branch behind main: `git rebase main`.

## Notes

- For multi-argument `gh` commands with special characters, use `-F` (body file) instead of inline `-b` to avoid shell quoting issues.
- When a `gh` or shell command returns exit code -1 but the output contains a success indicator (URL, hash, no error text), treat it as successful.
