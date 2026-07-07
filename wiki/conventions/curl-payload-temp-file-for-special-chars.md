---
type: convention
tags: [curl, shell-quoting, http]
Title: Use `curl --data @file` for Payloads with Shell-Special Characters
Sources: session-reflection, 2026-07-07
Raw: "[../../raw/lessons-learned/2026-07-07-cache-invalidated-experiment.md](../../raw/lessons-learned/2026-07-07-cache-invalidated-experiment.md)"
Updated: 2026-07-07
---

# Use `curl --data @file` for Payloads with Shell-Special Characters

Default to writing a `curl` JSON payload to a temp file and sending it with `--data @file` instead of inlining it with `-d '...'` whenever the payload text is unpredictable (user-authored message content, apostrophes, quotes, or other shell-special characters).

## Why

Inline `-d '...'` breaks the instant the payload contains an unescaped single quote, double quote, or other shell metacharacter — the shell terminates the quoted string early and the rest is interpreted as commands or garbage arguments. Hand-escaping is fragile and easy to get wrong on the first try, especially for content you didn't author yourself (e.g. relaying a message someone else wrote).

Writing the payload to a temp file sidesteps the shell entirely — the JSON body is never parsed by the shell's quoting rules, so apostrophes, quotes, and any other special characters pass through unchanged.

## Pattern

```
✗ curl -d '{"text": "it'"'"'s broken"}' https://example.test/api
✓ printf '%s' '{"text": "it'\''s fine"}' > /tmp/payload.json
  curl --data @/tmp/payload.json https://example.test/api
```

Prefer this by default for any `curl` payload carrying free-text content, rather than reaching for it only after a quoting failure.

## See Also

- [Never Read Secret Values Into Agent Context](never-expose-secrets-to-agent-context.md) — another curl-payload discipline, for a different failure mode (secret exposure rather than quoting)
