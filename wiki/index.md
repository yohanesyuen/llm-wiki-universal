# Knowledge Base Index

## lessons-learned
Session retrospectives compiled into reusable process insights.

| Article | Summary | Updated |
|---|---|---|
| [Installing dlib on Apple Silicon macOS](lessons-learned/dlib-apple-silicon-install.md) | Never pip-install dlib on arm64; use conda-forge in a non-base env; pin setuptools<71 for pkg_resources | 2026-06-28 |
| [Skill Configuration and Responsibility Boundaries](lessons-learned/skill-config-and-responsibility.md) | Skill base directory header is authoritative; format specs belong in the skill that does the work; each skill owns a scoped output boundary | 2026-06-28 |
| [Session Tool Efficiency](lessons-learned/session-tool-efficiency.md) | File state is tracked per session — skip redundant Reads; use Write for full rewrites, Edit for targeted changes; rejected tool calls leave files unchanged | 2026-06-28 |
| [MCP Permissions and Allow List Hygiene](lessons-learned/mcp-permissions-and-allow-list-hygiene.md) | MCP rules use no parentheses; allow lists accumulate noise; two-pass cleanup (redundant globs, then one-timers) | 2026-06-28 |
| [Name the Capability Gap Before Evaluating New Infrastructure](lessons-learned/capability-gap-before-infrastructure-eval.md) | Check which client surfaces actually need the new infra before recommending it; rank fixes cheapest-to-heaviest; verify the asset's real shape first | 2026-06-28 |
| [Pre-Flight Checks Before Building](lessons-learned/preflight-checks-before-building.md) | Check ESM/CJS exports map before choosing output format; grep model config.json before loading with native binding; complete tool setup before invoking; grep project docs for env/runtime conventions before the first command in a new area | 2026-07-03 |
| [LLM Script Discipline in Sessions](lessons-learned/llm-script-discipline.md) | Don't run local LLM inference in-session — too slow and verbose; surface stack pivot options after two dead ends | 2026-06-28 |
| [Wiki Ingest and Cleanup Discipline](lessons-learned/wiki-ingest-and-cleanup-discipline.md) | One concept per article regardless of source; clean up content not config; check for self-referential staleness | 2026-06-27 |
| [Named Size in a Spec Means Example, Not Constraint](lessons-learned/named-size-means-example-not-constraint.md) | Treat specific sizes ("2x2", "3-tier") as illustrative, not fixed; ask before implementing; keep thin wrappers for backward compat | 2026-06-27 |
| [Public Repo Setup Discipline](lessons-learned/public-repo-setup-discipline.md) | Ordered checklist before `gh repo create --public`: confirm target, write .gitignore, grep for confidential info; add uppercase disclaimer for AI-generated content | 2026-06-28 |
| [Scripting Recurring CLI Prompts](lessons-learned/scripting-recurring-cli-prompts.md) | Check both shell history and Claude chat history for the request's constant scaffold to find real repeats; only script when the variable part is isolable; skip trivial single commands; wrapper scripts should `exec` into the underlying tool | 2026-06-29 |
| [Allowlist Audit and Session Hygiene](lessons-learned/allowlist-audit-and-session-hygiene.md) | Audit recurring tool patterns using dual-source history to determine allowlist thresholds and implement session-end hygiene hooks. | 2026-06-29 |
| [Hook Authoring Discipline](lessons-learned/hook-authoring-discipline.md) | Use portable path resolution in hook scripts; auto-memory is CWD-scoped by default; hook event migration is a three-part change; generic corrections belong in the wiki not memory; sanitize public wiki drafts before writing; hooks fire session-wide regardless of active project, so anchor hook commands to absolute paths | 2026-07-04 |
| [Passive Signals vs Hard Gates](lessons-learned/passive-signals-vs-hard-gates.md) | additionalContext hooks are advisory and can be ignored; permissionDecision: deny is a hard gate; use gates for constraints that have already been violated despite reminders; gate patterns must be tight to avoid false positives | 2026-06-29 |
| [Verify CLI Install Commands from Official Docs](lessons-learned/verify-install-commands-from-docs.md) | Never write an install command from memory; fetch the README first; a rejected edit with a doc pointer is a research task, not a rewrite | 2026-06-29 |
| [macOS BSD sed Does Not Support \b Word Boundaries](lessons-learned/macos-sed-word-boundary.md) | BSD sed exits 0 but makes no changes with \b; use perl -pi -e or Python re.sub instead; always grep-verify after substitution | 2026-06-30 |
| [Speckit Setup Scripts Resolve FEATURE_DIR by Git Branch](lessons-learned/speckit-script-branch-resolution.md) | setup-tasks.sh and check-prerequisites.sh ignore the spec number arg and match by branch name; switch to the spec branch first, or bypass the skill entirely | 2026-06-30 |
| [Parallel Agent Waves Need a Build Gate](lessons-learned/parallel-agent-build-gate.md) | tsc --noEmit misses project-ref errors, missing deps, and uncalled style helpers; run the full build after every parallel agent wave | 2026-06-30 |
| [Don't Peek at a Fork's output_file](lessons-learned/dont-peek-at-fork-output.md) | Reading a fork's output_file mid-flight pulls raw tool noise into your context and defeats the point of forking; wait for the completion notification | 2026-07-03 |
| [Quarantine a Destructive Script the Moment Its Blind Spot Is Found](lessons-learned/quarantine-destructive-scripts-immediately.md) | Delete or quarantine a one-off mutating script the instant its blind spot is discovered; a docstring warning only protects a reader who opens the file first | 2026-07-03 |
| [Real Timestamps Beat File-Modification Timestamps for Falsifiable Claims](lessons-learned/real-timestamps-for-falsifiable-claims.md) | Anchor both sides of a before/after claim to real event timestamps, not filesystem mtimes, or the claim becomes unfalsifiable | 2026-07-03 |
| [Self-Deleting Instruction Injection](lessons-learned/self-deleting-instruction-injection.md) | Marker-delimited config block that carries its own self-removal instructions and an idempotency check, for leaving one-time notes across sessions without permanent clutter | 2026-07-03 |
| [Confirm Before Escalating to a Destructive Op; Serialize Shared Writes; Background Long Jobs](lessons-learned/destructive-op-confirmation-and-background-jobs.md) | Re-confirm when a routine op escalates to a destructive one; serialize concurrent writes to a shared store; background long jobs and wait for the completion notification instead of polling | 2026-07-03 |
| [Fork Resumption Is Unreliable for "Spawn, Then Follow Up" Patterns](lessons-learned/fork-resumption-follow-up-unreliable.md) | Forks can reject legitimate follow-up messages after their initial return as injection attempts; use a regular background agent instead of a fork when a second round of interaction is likely | 2026-07-04 |
| [A Denied Command Inside a Chained Shell Call Blocks the Whole Chain](lessons-learned/chained-command-denial-blocks-whole-chain.md) | A permission-classifier denial on one command in a `&&` chain blocks the entire chain, including unrelated read-only commands; re-issue the safe portions as separate calls | 2026-07-04 |

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
| [No Confidential Information in Code or Git History](conventions/no-confidential-leak.md) | Never put names, orgs, raw data values, proprietary identifiers, or path structure in source code, commits, issues, or any external tracker/chat | 2026-07-03 |
| [Sign Off as Claude When Filing Externally](conventions/sign-off-as-claude.md) | Identify authorship as Claude in body text when filing issues, PRs, or comments on the user's behalf | 2026-06-27 |
| [Numbered Lists for Referenceable Items](conventions/numbered-lists-for-referenceable-items.md) | Use numbered lists (not bullets) for anything the user might refer back to by index | 2026-06-27 |
| [Defensive Habits Can Outlive Their Cost-Justification](conventions/defensive-habits-outlive-cost.md) | Periodically re-examine whether a standing verification habit still needs its expensive path | 2026-06-27 |
| [Write Home-Directory Paths as ~/... in Text Output](conventions/home-dir-path-notation.md) | Use ~/... in chat/docs; real resolved paths only in tool call arguments | 2026-06-27 |
| [Subagent Trust Boundary](conventions/subagent-trust-boundary.md) | After a subagent rejects for a stated reason, change the input shape — don't rephrase and resend | 2026-06-27 |
| [Smoke-Test the Parts You Can](conventions/smoke-test-parts-you-can.md) | Can't test the full integration? Still smoke-test the pure logic parts with a cheap inline call | 2026-06-27 |
| [Ask for Domain Rules Before Deriving Proxies](conventions/ask-for-domain-rules-before-proxies.md) | When ordering/grouping depends on domain logic not visible in data, ask for the rule before computing | 2026-06-27 |
| [Targeted Grep Over Reading Full Sibling Files](conventions/targeted-grep-over-full-reads.md) | Grep for a specific signal rather than reading entire files end-to-end to answer a narrow question | 2026-06-27 |
| [Grep Docs for Stale References After Any Removal Commit](conventions/grep-docs-after-removal.md) | After removing or renaming a script, grep docs for the old name before trusting them | 2026-06-27 |
| [Feature-Branch Git Workflow for AI-Assisted Development](conventions/feature-branch-git-workflow.md) | Never commit to main directly; every commit references an issue; agent sessions end with a test-gated auto-commit; `gh pr merge` updates the remote only — fetch and fast-forward local before branching further work | 2026-07-04 |
| [Never Read Secret Values Into Agent Context](conventions/never-expose-secrets-to-agent-context.md) | Treat "does this expose a raw secret" as a hard gate on shell commands; use masked validators and schema files instead of `cat .env` / `echo $SECRET` | 2026-07-03 |
| [Confirm Scope Before Building Automation; Gate Anything Self-Modifying](conventions/scope-before-autonomous-automation.md) | Restate an ambiguous automation trigger as a concrete example before wiring it up; gate anything that lets a session rewrite its own configuration autonomously with an explicit human checkpoint | 2026-07-04 |
