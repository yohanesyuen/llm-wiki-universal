# Knowledge Base Index

## lessons-learned

Session retrospectives compiled into reusable process insights.

See the [full index](lessons-learned/index.md) (66 articles).

## knowledge-formats

Specifications and standards for representing and distributing structured knowledge.

| Article | Summary | Updated |
|---|---|---|
| [Open Knowledge Format (OKF)](knowledge-formats/open-knowledge-format.md) | Markdown files + YAML frontmatter as the distribution unit for machine- and human-readable knowledge bundles; covers structure, fields, cross-linking, conformance, and distribution | 2026-06-28 |

## conventions

Operating rules and confidentiality requirements.

| Article | Summary | Updated |
|---|---|---|
| [When to Consult the Wiki](conventions/when-to-consult-wiki.md) | Trigger table only — read fresh each non-trivial task; links to procedure detail | 2026-06-28 |
| [Wiki Consult Procedure](conventions/wiki-consult-procedure.md) | Scan depth limits, material pivot definition, and what to do after reading an article | 2026-06-28 |
| [No Confidential Information in Code or Git History](conventions/no-confidential-leak.md) | Never put names, orgs, raw data values, proprietary identifiers, or path structure in source code, commits, issues, or any external tracker/chat; naming the *category* of sensitive data removed can itself be over-disclosure in a cross-session broadcast | 2026-07-06 |
| [Sign Off as Claude When Filing Externally](conventions/sign-off-as-claude.md) | Identify authorship as Claude in body text when filing issues, PRs, or comments on the user's behalf | 2026-06-27 |
| [Numbered Lists for Referenceable Items](conventions/numbered-lists-for-referenceable-items.md) | Use numbered lists (not bullets) for anything the user might refer back to by index | 2026-06-27 |
| [Defensive Habits Can Outlive Their Cost-Justification](conventions/defensive-habits-outlive-cost.md) | Periodically re-examine whether a standing verification habit still needs its expensive path | 2026-06-27 |
| [Write Home-Directory Paths as ~/... in Text Output](conventions/home-dir-path-notation.md) | Use ~/... in chat/docs; real resolved paths only in tool call arguments | 2026-06-27 |
| [Subagent Trust Boundary](conventions/subagent-trust-boundary.md) | After a subagent rejects for a stated reason, change the input shape — don't rephrase and resend | 2026-06-27 |
| [Smoke-Test the Parts You Can](conventions/smoke-test-parts-you-can.md) | Can't test the full integration? Still smoke-test the pure logic parts with a cheap inline call; a moved bind-mount path isn't verified until the consumer is recreated and inspected | 2026-07-06 |
| [Ask for Domain Rules Before Deriving Proxies](conventions/ask-for-domain-rules-before-proxies.md) | When ordering/grouping depends on domain logic not visible in data, ask for the rule before computing | 2026-06-27 |
| [Targeted Grep Over Reading Full Sibling Files](conventions/targeted-grep-over-full-reads.md) | Grep for a specific signal rather than reading entire files end-to-end to answer a narrow question | 2026-06-27 |
| [Grep Docs for Stale References After Any Removal Commit](conventions/grep-docs-after-removal.md) | After removing or renaming a script, grep docs for the old name before trusting them | 2026-06-27 |
| [Feature-Branch Git Workflow for AI-Assisted Development](conventions/feature-branch-git-workflow.md) | Never commit to main directly; every commit references an issue; agent sessions end with a test-gated auto-commit; `gh pr merge` updates the remote only — fetch and fast-forward local before branching further work; a merge can report local failure after already succeeding remotely — verify remote merge state via the platform's API/CLI before concluding | 2026-07-06 |
| [Never Read Secret Values Into Agent Context](conventions/never-expose-secrets-to-agent-context.md) | Treat "does this expose a raw secret" as a hard gate on shell commands; use masked validators and schema files instead of `cat .env` / `echo $SECRET` | 2026-07-03 |
| [Confirm Scope Before Building Automation; Gate Anything Self-Modifying](conventions/scope-before-autonomous-automation.md) | Restate an ambiguous automation trigger as a concrete example before wiring it up; gate anything that lets a session rewrite its own configuration autonomously with an explicit human checkpoint | 2026-07-04 |
| [Use `curl --data @file` for Payloads with Shell-Special Characters](conventions/curl-payload-temp-file-for-special-chars.md) | Write unpredictable payload text (apostrophes, quotes) to a temp file and send with `--data @file` instead of inline `-d '...'` to sidestep shell-quoting breakage entirely | 2026-07-07 |
| [Standing Rules Get Sharper Through Live Pushback, Not First-Draft Phrasing](conventions/standing-rules-sharpen-through-pushback.md) | Treat a newly-written standing rule as a first draft; expect its first real test to expose a loophole and revise the rule's own wording, not just the one instance | 2026-07-07 |
