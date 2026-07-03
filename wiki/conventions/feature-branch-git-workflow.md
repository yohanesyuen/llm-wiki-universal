---
Title: Feature-Branch Git Workflow for AI-Assisted Development
Sources: Internal project workflow doc; 2026-06-29
Raw: "[2026-06-29-feature-branch-git-workflow.md](../../raw/conventions/2026-06-29-feature-branch-git-workflow.md)"
Updated: 2026-06-29
---
	
# Feature-Branch Git Workflow for AI-Assisted Development

## Core Rules

**Never commit directly to `master`/`main`.** All work goes on a feature branch, gets PR'd, squash-merged, and the branch deleted. This applies to AI agents as much as human developers.

**Every commit references a GitHub issue.** If no issue exists, create one before committing. The issue number appears in the commit message and the PR body (`Closes #N`).

## Branch Lifecycle

```
git checkout -b <type>/<issue>-<short-desc>   # e.g. feat/100-new-feature
# ... work ...
git push -u origin <branch>
gh pr create --title "type(scope): summary (#N)" --body "Closes #N"
gh pr merge --squash --delete-branch
git checkout master && git pull
```

Types follow Conventional Commits: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`, `perf`.

## Commit Discipline

- Stage specific files by name — never `git add .` or `git add -A` (risk of committing secrets or large binaries).
- Commit message format: `type(scope): short summary (#issue)`.
- One logical unit of work per commit. Independent changes get separate commits.
- Push immediately after committing (avoids local-only drift).

## Issue Tracking

```
gh issue list --state open --json number,title   # check first
gh issue create --title "<type>(<scope>): <summary>" --label "<labels>"
```

Reference the issue in every commit message. Use `Closes #N` in the PR body so GitHub auto-closes on merge.

## Agent Auto-Commit Rule

When an AI agent session ends with uncommitted tracked changes:

1. Run the project's test suite first.
2. Tests pass → stage, commit with issue ref, push.
3. Tests fail → do NOT commit; leave unstaged and report.

This prevents committing broken state that a human will have to untangle later.

## Staying Current

Before starting any new work:

```
git fetch origin
git pull          # if behind on master
git rebase main   # if on a feature branch behind main
```

## Pitfalls

- `gh pr create` with special characters in `-b` can mis-parse; use `-F <file>` (body from file) instead.
- Exit code -1 from `gh`/shell can be a false negative — if the output contains a URL or hash with no error text, the command succeeded.

## See Also

- [No Confidential Information in Code or Git History](no-confidential-leak.md)
