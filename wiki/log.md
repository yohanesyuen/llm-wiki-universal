# Wiki Log

## [2026-07-19] lint | 2 issues found, 16 auto-fixed
- Auto-fixed: added missing index.md entry for [Git-Based Isolation Can't Isolate What Git Doesn't Track; a Directory-Change Hook Can Silently Revert a Workaround Edit](lessons-learned/worktree-isolation-untracked-files-and-shell-hook-race.md)
- Auto-fixed: appended `Wiki:` memory backlinks for 15 high-confidence matches in ~/.claude/memory/ (feedback_audit_log_trace_before_code, feedback_browser_automation_false_positive, feedback_bundle_budget_before_migration, feedback_db_gated_tests_checkbox_not_proof, feedback_dry_run_independent_verification, feedback_flag_unexpected_fields_separately, feedback_isolated_worktree_push_concurrent_session, feedback_migration_before_push_causes_outage, feedback_shell_rc_debug_false_positive, feedback_stale_clarifying_question_resumption, feedback_toggle_at_bundler_boundary, feedback_vendor_lib_source_before_patch, feedback_verify_contract_before_bug_claim, feedback_verify_db_env_before_writes, feedback_workflow_dogfood_self_use_and_status_updates)
- Reported (no auto-fix, heuristic): ~25 orphan wiki pages with no inbound See-Also/body links from other articles (mostly standalone conventions/ entries plus several 2026-07-19-batch lessons-learned articles not yet cross-referenced)
- Reported (no auto-fix, low-confidence memory matches): feedback_concurrent_edit_reverify_fresh.md and feedback_concurrent_file_edit_reload.md have plausible but non-exact overlapping wiki candidates (stale-mutable-state-reread-discipline.md, concurrent-session-shared-file-collision.md) — left unlinked per "multiple plausible matches" rule

## [2026-07-19] ingest | 14 articles compiled from 12 previously-uncompiled raw lessons-learned files (2026-07-17/07-18 batch)
- Created: [A "Grant/Revoke" Field Must Be Derived From Both Sides of a Transition, Never One](lessons-learned/derive-transition-fields-from-before-after-diff.md) (raw: 2026-07-17-audit-log-classification-bug.md)
- Created: [Statutory and Legal Figures Need a Live Citation, Not Recalled Confidence](lessons-learned/verify-statutory-legal-claims-live.md) (raw: 2026-07-17-statutory-fact-hallucination.md)
- Created: [Check Bundle Budget as Part of the Initial Library Comparison, Not After Implementation](lessons-learned/bundle-budget-check-before-library-migration.md) + [Toggle at the Bundler's Code-Splitting Boundary for a Reversible Migration](lessons-learned/toggle-at-bundler-code-splitting-boundary.md) (raw: 2026-07-18-bundle-size-verification-pluggable-fallback.md, split into two articles)
- Created: [An "Is the Variable Still Defined" Check Proves Nothing If the Script Deliberately Deletes It](lessons-learned/shell-rc-absence-check-and-quoting-hazards.md) (raw: 2026-07-18-debugging-shell-rc-false-positives.md)
- Created: [A Request Built on a False Premise Deserves a Correction, Not Silent Compliance or Refusal](lessons-learned/false-premise-scoping-and-diff-before-git-reconcile.md) (raw: 2026-07-18-evidence-based-scoping-and-concurrent-git-conflicts.md)
- Created: [Reason About the Worst-Case Node Before Running a Bulk Rollup; Search for Prior Art Before Building a Second Implementation](lessons-learned/rollup-safety-reasoning-and-check-for-prior-art.md) + [Browser Automation False Positives Look Exactly Like Confirmed Bugs](lessons-learned/browser-automation-false-positive.md) (raw: 2026-07-18-hierarchical-status-rollup-tooling.md, split into two articles)
- Created: [A Tool's Success Message Describes Intent, Not Effect — Diff the Actual Before/After](lessons-learned/verify-mutating-tool-diffs-not-success-messages.md) (raw: 2026-07-18-managed-block-trust-and-drift-detection.md)
- Created: [A Subagent's Self-Report Is a Claim, Not a Verification](lessons-learned/subagent-self-report-is-not-verification.md) (raw: 2026-07-18-multi-agent-workflow-verification.md)
- Created: [Check Whether the Spec Already Documents a Behavior as Intentional Before Calling It a Bug](lessons-learned/check-spec-before-calling-it-a-bug.md) (raw: 2026-07-18-pm-audit-fix-handoff.md)
- Created: [A Destructive Live Migration and Its Matching Code Deploy Are One Atomic Unit](lessons-learned/migration-deploy-atomicity-and-real-data-default.md) (raw: 2026-07-18-schema-migration-sequencing-and-real-data-preference.md)
- Created: [A Rejected Clarifying Question Doesn't Stay "Live" Context Across a Topic Shift](lessons-learned/stale-clarifying-question-resumption.md) (raw: 2026-07-18-stale-context-and-live-verification.md)
- Created: [Grep the Vendor's Compiled Source for Real Event Wiring Before Guessing at a Fix](lessons-learned/vendor-source-diagnosis-and-isolated-worktree-push.md) (raw: 2026-07-18-vendor-lib-source-diagnosis-isolated-push.md)
- Cross-linked new articles against existing related lessons-learned entries (verify-invariants-and-validate-debugging-signals, verify-subagent-handoffs-and-query-structured-logs, fork-resumption-follow-up-unreliable, calibrating-when-to-ask, stale-mutable-state-reread-discipline, schema-and-ingestion-audit-checklist, macos-sed-word-boundary, worktree-liveness-check-before-destructive-cleanup, concurrent-session-shared-file-collision, guard-scope-vs-verbal-override, layer-boundary-configs-and-staged-cutover, verify-install-commands-from-docs, resolve-targets-test-through-own-api) — existing articles themselves not modified, only new articles' See Also sections
- Updated: `wiki/index.md` (14 new rows added to lessons-learned)

## [2026-07-07] ingest | [Prompt Caching Can Invalidate "Fresh Session" A/B Experiments](lessons-learned/prompt-caching-invalidates-fresh-session-experiments.md)
- Created: [Fire-and-Forget Background Threads in Short-Lived Scripts Need a Bounded Join](lessons-learned/fire-and-forget-thread-needs-bounded-join.md)
- Created: [Use `curl --data @file` for Payloads with Shell-Special Characters](conventions/curl-payload-temp-file-for-special-chars.md)
- Created: [Standing Rules Get Sharper Through Live Pushback, Not First-Draft Phrasing](conventions/standing-rules-sharpen-through-pushback.md)
- Updated: [Real Timestamps Beat File-Modification Timestamps for Falsifiable Claims](lessons-learned/real-timestamps-for-falsifiable-claims.md)
- Updated: [Session Tool Efficiency](lessons-learned/session-tool-efficiency.md)
- Updated: [Root-Cause UI Bugs to the Shared Primitive Behind Them](lessons-learned/root-cause-shared-styling-primitives.md)
- Updated: [Hook Authoring Discipline](lessons-learned/hook-authoring-discipline.md)
- Updated: [Wiki Ingest and Cleanup Discipline](lessons-learned/wiki-ingest-and-cleanup-discipline.md)

## [2026-07-06] ingest | [Git History Scrubbing Has Two Leak Surfaces; a Moved Mount Isn't Done Until the Consumer Restarts](lessons-learned/git-history-scrubbing-and-mount-verification.md)
- Updated: [No Confidential Information in Code or Git History](conventions/no-confidential-leak.md)
- Updated: [Smoke-Test the Parts You Can](conventions/smoke-test-parts-you-can.md)

## [2026-07-06] ingest | [A Guard's Enforcement Scope Doesn't Automatically Match an Override's Conversational Scope](lessons-learned/guard-scope-vs-verbal-override.md)
- Created: [Root-Cause UI Bugs to the Shared Primitive Behind Them](lessons-learned/root-cause-shared-styling-primitives.md)
- Updated: [Feature-Branch Git Workflow for AI-Assisted Development](conventions/feature-branch-git-workflow.md)
- Updated: [Parallel Agent Waves Need a Build Gate](lessons-learned/parallel-agent-build-gate.md)
- Updated: [Check a Helper's Contract Before Printing Its Output to Inspect Shape; Isolate Shared Namespaces by Default](lessons-learned/debug-print-secret-leak.md)
- Updated: [Confirm Scope Before Building Automation; Gate Anything Self-Modifying](conventions/scope-before-autonomous-automation.md)
- Updated: [Uncommitted State Is Not the Same as "In Use" — Worktree Cleanup Needs a Liveness Check](lessons-learned/worktree-liveness-check-before-destructive-cleanup.md)

## [2026-07-06] ingest | [Probe Sibling APIs Directly; Plausible-Small Numbers Are a Bug Smell](lessons-learned/api-capability-probing-and-plausible-wrong-values.md)
- Updated: [Pre-Flight Checks Before Building](lessons-learned/preflight-checks-before-building.md)

## [2026-07-05] ingest | [Uncommitted State Is Not the Same as "In Use" — Worktree Cleanup Needs a Liveness Check](lessons-learned/worktree-liveness-check-before-destructive-cleanup.md)
- Updated: [Confirm Before Escalating to a Destructive Op; Serialize Shared Writes; Background Long Jobs](lessons-learned/destructive-op-confirmation-and-background-jobs.md)
- Updated: [Confirm Scope Before Building Automation; Gate Anything Self-Modifying](conventions/scope-before-autonomous-automation.md)
- Updated: [Check a Helper's Contract Before Printing Its Output to Inspect Shape; Isolate Shared Namespaces by Default](lessons-learned/debug-print-secret-leak.md)
- Updated: [Quarantine a Destructive Script the Moment Its Blind Spot Is Found](lessons-learned/quarantine-destructive-scripts-immediately.md)

## [2026-07-04] ingest | [Layer-Boundary Config Bugs and Staged Service Cutover](lessons-learned/layer-boundary-configs-and-staged-cutover.md)
- Updated: [Never Read Secret Values Into Agent Context](conventions/never-expose-secrets-to-agent-context.md)

## [2026-07-04] ingest | [Fork Resumption Is Unreliable for "Spawn, Then Follow Up" Patterns](lessons-learned/fork-resumption-follow-up-unreliable.md)
- Created: [A Denied Command Inside a Chained Shell Call Blocks the Whole Chain](lessons-learned/chained-command-denial-blocks-whole-chain.md)
- Created: [Confirm Scope Before Building Automation; Gate Anything Self-Modifying](conventions/scope-before-autonomous-automation.md)
- Updated: [Hook Authoring Discipline](lessons-learned/hook-authoring-discipline.md)
- Updated: [Feature-Branch Git Workflow for AI-Assisted Development](conventions/feature-branch-git-workflow.md)
- Updated: [Don't Peek at a Fork's output_file](lessons-learned/dont-peek-at-fork-output.md)
- Updated: [Confirm Before Escalating to a Destructive Op; Serialize Shared Writes; Background Long Jobs](lessons-learned/destructive-op-confirmation-and-background-jobs.md)

## [2026-07-03] merge | [Sanitize Content Before Writing to an External Tracker](conventions/sanitize-before-external-tracker.md) → [No Confidential Information in Code or Git History](conventions/no-confidential-leak.md)
- The former was a strict superset of the latter's rule (self-flagged in its own See Also); folded its content in and deleted the standalone article to cut duplicate conventions.
- Updated: [Never Read Secret Values Into Agent Context](conventions/never-expose-secrets-to-agent-context.md) (redirected its cross-link)
- Updated: `wiki/index.md` (removed the now-merged row)

## [2026-07-03] lint | 4 issues found, 1 auto-fixed

## [2026-07-03] ingest | [Never Read Secret Values Into Agent Context](conventions/never-expose-secrets-to-agent-context.md)
- Updated: [No Confidential Information in Code or Git History](conventions/no-confidential-leak.md)

## [2026-07-03] ingest | [Sanitize Content Before Writing to an External Tracker](conventions/sanitize-before-external-tracker.md)
- Updated: [No Confidential Information in Code or Git History](conventions/no-confidential-leak.md)

## [2026-07-03] ingest | [Quarantine a Destructive Script the Moment Its Blind Spot Is Found](lessons-learned/quarantine-destructive-scripts-immediately.md)
- Updated: [Pre-Flight Checks Before Building](lessons-learned/preflight-checks-before-building.md)
- Updated: [Real Timestamps Beat File-Modification Timestamps for Falsifiable Claims](lessons-learned/real-timestamps-for-falsifiable-claims.md)
- Updated: [Self-Deleting Instruction Injection](lessons-learned/self-deleting-instruction-injection.md)
- Updated: [Confirm Before Escalating to a Destructive Op; Serialize Shared Writes; Background Long Jobs](lessons-learned/destructive-op-confirmation-and-background-jobs.md)
- Updated: [Don't Peek at a Fork's output_file](lessons-learned/dont-peek-at-fork-output.md)

## [2026-06-30] ingest | [Don't Peek at a Fork's output_file](lessons-learned/dont-peek-at-fork-output.md)

## [2026-06-30] ingest | [macOS BSD sed Does Not Support \b Word Boundaries](lessons-learned/macos-sed-word-boundary.md)

## [2026-06-30] ingest | [Speckit Setup Scripts Resolve FEATURE_DIR by Git Branch](lessons-learned/speckit-script-branch-resolution.md)

## [2026-06-30] ingest | [Parallel Agent Waves Need a Build Gate](lessons-learned/parallel-agent-build-gate.md)

## [2026-06-29] ingest | [Verify CLI Install Commands from Official Docs](lessons-learned/verify-install-commands-from-docs.md)

## [2026-06-29] ingest | [Passive Signals vs Hard Gates](lessons-learned/passive-signals-vs-hard-gates.md)

## [2026-06-29] ingest | [Hook Authoring Discipline](lessons-learned/hook-authoring-discipline.md)

## [2026-06-29] ingest | [Feature-Branch Git Workflow for AI-Assisted Development](conventions/feature-branch-git-workflow.md)

## [2026-06-29] ingest | [Claude chat history as a repetition source](raw/lessons-learned/2026-06-29-claude-chat-history-as-repetition-source.md)
- Updated: [Scripting Recurring CLI Prompts](lessons-learned/scripting-recurring-cli-prompts.md)

## [2026-06-29] ingest | [Scripting Recurring CLI Prompts](lessons-learned/scripting-recurring-cli-prompts.md)

## [2026-06-28] lint | 23 issues found, 23 auto-fixed — added `type` field to all article frontmatter (OKF conformance)

## [2026-06-28] ingest | [Open Knowledge Format (OKF)](knowledge-formats/open-knowledge-format.md)

## [2026-06-28] ingest | [When to Consult the Wiki](conventions/when-to-consult-wiki.md)
- Compressed to trigger table + intro only; procedural detail moved to wiki-consult-procedure.md
- Created: [Wiki Consult Procedure](conventions/wiki-consult-procedure.md)

## [2026-06-28] ingest | [Installing dlib on Apple Silicon macOS](lessons-learned/dlib-apple-silicon-install.md)

## [2026-06-28] ingest | [When to Consult the Wiki](conventions/when-to-consult-wiki.md)

## [2026-06-28] ingest | [Skill Configuration and Responsibility Boundaries](lessons-learned/skill-config-and-responsibility.md)
- Updated: [Session Tool Efficiency](lessons-learned/session-tool-efficiency.md)

## [2026-06-28] ingest | [Session Tool Efficiency](lessons-learned/session-tool-efficiency.md)
## [2026-06-28] update | [Public Repo Setup Discipline](lessons-learned/public-repo-setup-discipline.md) — added uppercase disclaimer pattern

## [2026-06-28] ingest | [Pre-Flight Checks Before Building](lessons-learned/preflight-checks-before-building.md)
## [2026-06-28] ingest | [LLM Script Discipline in Sessions](lessons-learned/llm-script-discipline.md)

## [2026-06-28] ingest | [MCP Permissions and Allow List Hygiene](lessons-learned/mcp-permissions-and-allow-list-hygiene.md)
## [2026-06-28] ingest | [Name the Capability Gap Before Evaluating New Infrastructure](lessons-learned/capability-gap-before-infrastructure-eval.md)

## [2026-06-27] ingest | [Public Repo Setup Discipline](lessons-learned/public-repo-setup-discipline.md)

## [2026-06-27] ingest | [Wiki Ingest and Cleanup Discipline](lessons-learned/wiki-ingest-and-cleanup-discipline.md)
## [2026-06-27] ingest | [Grep Docs for Stale References After Any Removal Commit](conventions/grep-docs-after-removal.md)
## [2026-06-27] ingest | [Targeted Grep Over Reading Full Sibling Files](conventions/targeted-grep-over-full-reads.md)
## [2026-06-27] ingest | [Ask for Domain Rules Before Deriving Proxies](conventions/ask-for-domain-rules-before-proxies.md)
## [2026-06-27] ingest | [Smoke-Test the Parts You Can](conventions/smoke-test-parts-you-can.md)
## [2026-06-27] ingest | [Subagent Trust Boundary](conventions/subagent-trust-boundary.md)
## [2026-06-27] ingest | [Write Home-Directory Paths as ~/... in Text Output](conventions/home-dir-path-notation.md)
## [2026-06-27] ingest | [Defensive Habits Can Outlive Their Cost-Justification](conventions/defensive-habits-outlive-cost.md)
## [2026-06-27] ingest | [Numbered Lists for Referenceable Items](conventions/numbered-lists-for-referenceable-items.md)
## [2026-06-27] ingest | [Sign Off as Claude When Filing Externally](conventions/sign-off-as-claude.md)
## [2026-06-27] ingest | [No Confidential Information in Code or Git History](conventions/no-confidential-leak.md)

## [2026-06-27] ingest | [Named Size in a Spec Means Example, Not Constraint](lessons-learned/named-size-means-example-not-constraint.md)

## [2026-06-27] init | Wiki initialized
- Created raw/ and wiki/ directories
- Created wiki/index.md and wiki/log.md
- Created CLAUDE.md (wiki root) and ~/.claude/CLAUDE.md (global rules)

## [2026-06-29] ingest | Allowlist Audit and Session Hygiene

## [2026-07-04] ingest | [Wiki Automation Gaps Found by Comparing Against a Reference Implementation](lessons-learned/wiki-automation-gaps-vs-reference-implementation.md)
- Updated: [Wiki Ingest and Cleanup Discipline](lessons-learned/wiki-ingest-and-cleanup-discipline.md)

## [2026-07-05] ingest | [Check a Helper's Contract Before Printing Its Output to Inspect Shape; Isolate Shared Namespaces by Default](lessons-learned/debug-print-secret-leak.md)
- Updated: [Never Read Secret Values Into Agent Context](conventions/never-expose-secrets-to-agent-context.md)
- Updated: [Confirm Before Escalating to a Destructive Op; Serialize Shared Writes; Background Long Jobs](lessons-learned/destructive-op-confirmation-and-background-jobs.md)
- Updated: [Layer-Boundary Config Bugs and Staged Service Cutover](lessons-learned/layer-boundary-configs-and-staged-cutover.md)

## [2026-07-06] ingest | [A Shared-File Collision Between Concurrent Agents Is a Protocol Gap, Not a Latency Gap](lessons-learned/concurrent-session-shared-file-collision.md)
- Updated: [Layer-Boundary Config Bugs and Staged Service Cutover](lessons-learned/layer-boundary-configs-and-staged-cutover.md)
- Updated: [A Guard's Enforcement Scope Doesn't Automatically Match an Override's Conversational Scope](lessons-learned/guard-scope-vs-verbal-override.md)
- Updated: [Confirm Before Escalating to a Destructive Op; Serialize Shared Writes; Background Long Jobs](lessons-learned/destructive-op-confirmation-and-background-jobs.md)
- Updated: [Uncommitted State Is Not the Same as "In Use" — Worktree Cleanup Needs a Liveness Check](lessons-learned/worktree-liveness-check-before-destructive-cleanup.md)

## [2026-07-07] lint | 2 issues found, 2 auto-fixed
- Added: Memory Backlinks check to karpathy-llm-wiki SKILL.md Heuristic Checks
- Fixed: ~/.claude/memory/feedback_prompt_cache_invalidates_subagent_experiments.md missing Wiki: link
- Fixed: ~/.claude/memory/feedback_daemon_thread_needs_join.md missing Wiki: link

## [2026-07-08] ingest | [Git-Based Isolation Can't Isolate What Git Doesn't Track; a Directory-Change Hook Can Silently Revert a Workaround Edit](lessons-learned/worktree-isolation-untracked-files-and-shell-hook-race.md)
- Updated: [Uncommitted State Is Not the Same as "In Use" — Worktree Cleanup Needs a Liveness Check](lessons-learned/worktree-liveness-check-before-destructive-cleanup.md)
- Updated: [A Guard's Enforcement Scope Doesn't Automatically Match an Override's Conversational Scope](lessons-learned/guard-scope-vs-verbal-override.md)
- Updated: [Fire-and-Forget Background Threads in Short-Lived Scripts Need a Bounded Join](lessons-learned/fire-and-forget-thread-needs-bounded-join.md)
- Updated: [A Shared-File Collision Between Concurrent Agents Is a Protocol Gap, Not a Latency Gap](lessons-learned/concurrent-session-shared-file-collision.md)

## [2026-07-17] ingest | [Verify a System's Deeper Invariant Before Building On It; Validate a Debugger's Signal Against a Known-Good Baseline](lessons-learned/verify-invariants-and-validate-debugging-signals.md)

## [2026-07-17] ingest | [Flag Each Surprising Field Separately; Read the Real Interface Before Extending It](lessons-learned/flag-fields-and-read-real-interfaces.md)
- Updated: [A Shared-File Collision Between Concurrent Agents Is a Protocol Gap, Not a Latency Gap](lessons-learned/concurrent-session-shared-file-collision.md)

## [2026-07-17] ingest | [Verify a Credential's Environment and a Script's Own Safety Claims Independently](lessons-learned/verify-environment-and-safety-claims.md)

## [2026-07-14] ingest | [When a Worktree-Isolation Guard Blocks Write/Edit, Reach for a Bash Heredoc First](lessons-learned/bgisolation-write-edit-workaround.md)

## [2026-07-17] ingest | [Calibrating When and How to Ask — Structured Choices Fit Stable Ambiguity, Not Unstable Intent](lessons-learned/calibrating-when-to-ask.md)

## [2026-07-12] ingest | [A Test That Passes Against an Unimplemented Stub Is a Smell; Codify a Repeated Workflow the Moment It Repeats](lessons-learned/stub-test-smell-and-workflow-codification.md)

## [2026-07-12] ingest | [Resolve Targets Directly, Don't Infer From a Manifest; Test Through a System's Own API, Not a Generic External One](lessons-learned/resolve-targets-test-through-own-api.md)
- Updated: [Fire-and-Forget Background Threads in Short-Lived Scripts Need a Bounded Join](lessons-learned/fire-and-forget-thread-needs-bounded-join.md)

## [2026-07-17] ingest | [Stale In-Context File State Is Indistinguishable From a Hallucination — Re-Read Before Asserting or Editing](lessons-learned/stale-mutable-state-reread-discipline.md)
- Updated: [A Shared-File Collision Between Concurrent Agents Is a Protocol Gap, Not a Latency Gap](lessons-learned/concurrent-session-shared-file-collision.md)

## [2026-07-10] ingest | [Probe a Live Runtime Instead of Theorizing; Key a Cache by Entity, Not by a Shared Evicting Scope](lessons-learned/empirical-probe-runtime-and-cache-isolation-design.md)

## [2026-07-10] ingest | [A Documented Default Path Is a Claim, Not a Fact — A Schema/Ingestion Audit Checklist](lessons-learned/schema-and-ingestion-audit-checklist.md)

## [2026-07-10] ingest | [A New Parameter Is a Data-Flow Change, Not a Signature Change; Filter Every Structure the Record Leaks Into](lessons-learned/threading-parameters-and-filter-design.md)

## [2026-07-09] ingest | [Verify a Subagent Handoff Actually Chains; Query the Structured Log for Live Metrics, Don't Estimate](lessons-learned/verify-subagent-handoffs-and-query-structured-logs.md)

## [2026-07-08] ingest | [Verify a Settings Knob Covers the Real Mechanism; Disclose a Vendored Patch's Fragility Up Front; State a Telemetry Window](lessons-learned/config-fix-diligence-and-classifier-retry.md)
- Updated: [Passive Signals vs Hard Gates](lessons-learned/passive-signals-vs-hard-gates.md)

## [2026-07-17] backlog-note | 9 raw lessons-learned files skipped as already-covered by existing articles (same session content, different filename): 2026-07-06-cloud-storage-api-consumer (→ api-capability-probing-and-plausible-wrong-values.md), 2026-07-06-cross-session-repo-cleanup (→ git-history-scrubbing-and-mount-verification.md), 2026-07-05-worktree-cleanup-collision (→ worktree-liveness-check-before-destructive-cleanup.md), 2026-07-04-agent-hooks-and-guardrails (→ fork-resumption-follow-up-unreliable.md, scope-before-autonomous-automation.md, hook-authoring-discipline.md, feature-branch-git-workflow.md, chained-command-denial-blocks-whole-chain.md), 2026-07-04-docker-nginx-auth-cutover (→ layer-boundary-configs-and-staged-cutover.md), 2026-07-03-corpus-cleanup-and-reindex (→ real-timestamps-for-falsifiable-claims.md, self-deleting-instruction-injection.md, destructive-op-confirmation-and-background-jobs.md, quarantine-destructive-scripts-immediately.md), 2026-06-28-mcp-conversion-eval (→ capability-gap-before-infrastructure-eval.md), 2026-06-28-file-state-tracking-and-readme-authoring (→ session-tool-efficiency.md, public-repo-setup-discipline.md), 2026-06-27-universal-wiki-setup (→ wiki-ingest-and-cleanup-discipline.md). conventions/2026-07-03-varlock-claude-skill-secure-env-vars.md also skipped — already the cited Raw source of conventions/never-expose-secrets-to-agent-context.md.
