# Knowledge Base Index

## lessons-learned
Session retrospectives compiled into reusable process insights.

| Article | Summary | Updated |
|---|---|---|
| [Wiki Ingest and Cleanup Discipline](lessons-learned/wiki-ingest-and-cleanup-discipline.md) | One concept per article regardless of source; clean up content not config; check for self-referential staleness | 2026-06-27 |
| [Named Size in a Spec Means Example, Not Constraint](lessons-learned/named-size-means-example-not-constraint.md) | Treat specific sizes ("2x2", "3-tier") as illustrative, not fixed; ask before implementing; keep thin wrappers for backward compat | 2026-06-27 |
| [Public Repo Setup Discipline](lessons-learned/public-repo-setup-discipline.md) | Ordered checklist before `gh repo create --public`: confirm target, write .gitignore, grep for confidential info | 2026-06-27 |

## conventions
Operating rules and confidentiality requirements.

| Article | Summary | Updated |
|---|---|---|
| [No Confidential Information in Code or Git History](conventions/no-confidential-leak.md) | Never put names of persons or orgs in source code, commits, or issue messages | 2026-06-27 |
| [Sign Off as Claude When Filing Externally](conventions/sign-off-as-claude.md) | Identify authorship as Claude in body text when filing issues, PRs, or comments on the user's behalf | 2026-06-27 |
| [Numbered Lists for Referenceable Items](conventions/numbered-lists-for-referenceable-items.md) | Use numbered lists (not bullets) for anything the user might refer back to by index | 2026-06-27 |
| [Defensive Habits Can Outlive Their Cost-Justification](conventions/defensive-habits-outlive-cost.md) | Periodically re-examine whether a standing verification habit still needs its expensive path | 2026-06-27 |
| [Write Home-Directory Paths as ~/... in Text Output](conventions/home-dir-path-notation.md) | Use ~/... in chat/docs; real resolved paths only in tool call arguments | 2026-06-27 |
| [Subagent Trust Boundary](conventions/subagent-trust-boundary.md) | After a subagent rejects for a stated reason, change the input shape — don't rephrase and resend | 2026-06-27 |
| [Smoke-Test the Parts You Can](conventions/smoke-test-parts-you-can.md) | Can't test the full integration? Still smoke-test the pure logic parts with a cheap inline call | 2026-06-27 |
| [Ask for Domain Rules Before Deriving Proxies](conventions/ask-for-domain-rules-before-proxies.md) | When ordering/grouping depends on domain logic not visible in data, ask for the rule before computing | 2026-06-27 |
| [Targeted Grep Over Reading Full Sibling Files](conventions/targeted-grep-over-full-reads.md) | Grep for a specific signal rather than reading entire files end-to-end to answer a narrow question | 2026-06-27 |
| [Grep Docs for Stale References After Any Removal Commit](conventions/grep-docs-after-removal.md) | After removing or renaming a script, grep docs for the old name before trusting them | 2026-06-27 |
