---
type: lesson
tags: [tooling, macos, shell, sed, regex]
Title: macOS BSD sed Does Not Support \b Word Boundaries
Sources: Session reflection, 2026-06-30
Raw: "[../../raw/lessons-learned/2026-06-30-macos-sed-word-boundary.md](../../raw/lessons-learned/2026-06-30-macos-sed-word-boundary.md)"
Updated: 2026-06-30
---

# macOS BSD sed Does Not Support \b Word Boundaries

`sed -i '' 's/\bPATTERN\b/REPLACE/g'` exits 0 on macOS but makes zero changes. BSD sed (shipped with macOS) silently ignores `\b` word boundaries. The same command works on Linux (GNU sed), so the bug only surfaces on macOS.

## Failure mode

A batch substitution runs, exits 0, emits no errors, and leaves the file unchanged. The silent no-op is only caught by post-verification.

## Fix

Use Perl or Python for portable word-boundary substitutions on macOS:

```bash
# Perl (portable, one-liner)
perl -pi -e 's/\bOLD\b/NEW/g' file.md

# Python (explicit, auditable)
python3 -c "
import re
with open('file.md') as f: c = f.read()
c = re.sub(r'\bOLD\b', r'NEW', c)
with open('file.md', 'w') as f: f.write(c)
"
```

BSD sed does support `[[:<:]]` and `[[:>:]]` as word-boundary anchors, but Perl/Python are more readable and portable across environments.

## Verification rule

After any sed substitution on macOS, always verify at least one replacement occurred:

```bash
grep -c 'NEW_PATTERN' file.md  # must be > 0
```

Never trust exit 0 alone for sed on macOS.

## See Also

- [Pre-Flight Checks Before Building](preflight-checks-before-building.md) — same theme of tool-behaviour assumptions that only surface at runtime
