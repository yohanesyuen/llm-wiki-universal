# Wiki Log

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
