---
type: lesson
tags: [git, security, documentation]
Title: Public Repo Setup Discipline
Sources: Session reflection, 2026-06-27
Raw: "[../../raw/lessons-learned/2026-06-27-public-repo-setup.md](../../raw/lessons-learned/2026-06-27-public-repo-setup.md)"
Updated: 2026-06-27
---

# Public Repo Setup Discipline

Lessons from publishing llm-wiki-universal to GitHub (2026-06-27): three ordered steps before any `gh repo create --public`.

## Clarify the target directory first

A multi-directory workspace has several candidate directories. Always ask (or infer unambiguously) which one before running `gh repo create`. A public repo cannot be trivially unpublished — making this the first gate matters.

## Write `.gitignore` before `git add -A`

Tool-specific config directories (`.obsidian/`, `.vscode/`, `.idea/`) belong in `.gitignore` before the first `git add`. Unstaging after the fact works but dirtier commit history and risks pushing config to remote if you forget. Default order: write `.gitignore` → then stage.

## Run a confidential info grep before `git push`

For any repo going public, grep for email addresses, real names, and org names before pushing. It takes seconds and cannot be undone once the repo is public (even if later deleted, content may be cached). See also: [[no-confidential-leak]].

## Ordered checklist

For any new public repo:
1. Confirm target directory
2. Write `.gitignore` (tool config dirs, secrets, etc.)
3. `grep -r` for confidential info
4. `git add`, commit, `gh repo create --public --source=. --remote=origin --push`

## Add an uppercase disclaimer to the README for non-obvious content

If the repo contains AI-generated, auto-sanitized, or otherwise non-standard content, add a short uppercase disclaimer near the top of the README. The register shift signals importance and sets expectations before the reader gets into the body. Place it after the intro paragraph but before the structure/usage sections.

Example:

> DISCLAIMER: ALL CONTENT IN THIS REPO IS GENERATED AND SANITIZED BEFORE PUBLICATION. USE AT YOUR OWN DISCRETION.

The uppercase reads differently from a prose note — readers who scan READMEs are more likely to catch it.

## One-liner to create and push

```bash
gh repo create <name> --public --source=. --remote=origin --push
```

Single command: creates the GitHub repo, sets origin remote, and pushes. No separate `git remote add` step needed.
