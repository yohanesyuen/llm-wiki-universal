---
source: session-reflection
collected: 2026-06-30
published: Unknown
---

# macOS BSD sed Does Not Support \b Word Boundaries

**Date**: 2026-06-30
**Tags**: tooling, macos, shell

---

## Lesson

`sed -i '' 's/\bPATTERN\b/REPLACE/g'` exits 0 on macOS but makes zero changes. BSD sed (shipped with macOS) silently ignores `\b` word boundaries. GNU sed (Linux default) supports `\b` — the same command works there, so the bug only surfaces on macOS.

## Failure Mode

A batch rename of task IDs (T001→T101) was run with `sed -i '' 's/\bT0\([0-9][0-9]\)\b/T1\1/g'`. Exit code was 0, no error output. The file was unchanged. The error was only discovered by grep-verifying the output file — a step that had not been done because exit 0 felt conclusive. A full context window was spent diagnosing downstream effects (56 of 64 GitHub issues silently skipped) before tracing the root cause back to the no-op sed.

## Fix

Use Perl or Python for portable word-boundary substitutions on macOS:

```bash
# Perl (portable, one-liner)
perl -pi -e 's/\bT0(\d{2})\b/T1$1/g' file.md

# Python (explicit, auditable)
python3 -c "
import re
with open('file.md') as f: c = f.read()
c = re.sub(r'\bT0(\d{2})\b', r'T1\1', c)
with open('file.md', 'w') as f: f.write(c)
"
```

BSD sed does support `[[:<:]]` and `[[:>:]]` as word-boundary anchors, but Perl/Python are more readable and portable.

## Verification Rule

After any sed substitution on macOS, always verify at least one replacement occurred:

```bash
grep -c 'NEW_PATTERN' file.md  # must be > 0
```

Never trust exit 0 alone for sed on macOS.
