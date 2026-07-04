---
type: convention
tags: [security, secrets, env-vars]
Title: Never Read Secret Values Into Agent Context
Sources: wrsmith108/varlock-claude-skill (GitHub), 2026
Raw: "[../../raw/conventions/2026-07-03-varlock-claude-skill-secure-env-vars.md](../../raw/conventions/2026-07-03-varlock-claude-skill-secure-env-vars.md)"
Updated: 2026-07-03
---

# Never Read Secret Values Into Agent Context

Any command whose output could contain a secret must be avoided, replaced with a masking equivalent, or declined — because once a secret enters the agent's context, it can resurface in terminal output, logs, traces, commit diffs, or error messages.

## The Rule

Treat "does this expose a raw secret value to me" as a hard gate on shell commands, not just source code:

- `cat .env`, `less .env`, or a generic file-read tool on an env file — always exposes every value at once.
- `echo $SECRET_VAR`, `printenv | grep X` — exposes to the agent's context even if the terminal is not seen by a human.
- `test -n "$API_KEY" && echo "Key: $API_KEY"` — presence checks that leak the value are just as bad as printing it directly.
- Secrets interpolated literally into a command (e.g., a hardcoded bearer token in a `curl` call) — persists in shell history even if never echoed back.

## Safe Alternatives

Prefer tools that validate and mask rather than print:

- Read a schema/definition file (e.g., `.env.schema`) instead of the values file — schemas describe types and requirements without containing secret values, so they're always safe to read.
- Use a validator that shows masked output on success (e.g., `varlock load`, which prints `API_KEY 🔐sensitive └ ▒▒▒▒▒` instead of the value).
- Inject secrets into a subprocess at runtime rather than resolving them into the agent's own context first (e.g., `varlock run -- npm start` instead of exporting and echoing).
- Reference the variable by name in commands (`$API_KEY`) rather than reading and re-typing its value.

## When a User Asks to Inspect or Change a Secret

Decline the direct action and redirect to a safe equivalent:

- "Check if API key is set" → run a masked validator filtered to that key, not `echo`.
- "Update a secret" → decline to write the value yourself; ask the user to update it in the source (`.env` file, secrets manager) manually, then re-validate.
- "Show me the .env file" → offer the schema or a masked validation run instead of reading the file.

This mirrors the general policy against reading raw data files directly ([No Confidential Information in Code or Git History](no-confidential-leak.md)), but is stricter: even *internal* context exposure (not just external write targets) is disallowed for secrets.

## See Also

- [No Confidential Information in Code or Git History](no-confidential-leak.md) — same spirit applied to names/orgs and raw data values instead of secret values
- [Layer-Boundary Config Bugs and Staged Service Cutover](../lessons-learned/layer-boundary-configs-and-staged-cutover.md) — adjacent rule: never fabricate a placeholder secret for a live account when an interactive reset tool fails, even transiently
