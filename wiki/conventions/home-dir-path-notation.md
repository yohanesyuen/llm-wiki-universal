---
Title: Write Home-Directory Paths as ~/... in Text Output
Sources: session-reflection, 2026-06-25
Raw: [../../raw/conventions/home-dir-path-notation.md](../../raw/conventions/home-dir-path-notation.md)
Updated: 2026-06-27
---

# Write Home-Directory Paths as ~/... in Text Output

In chat output and written files, write home-directory paths as `~/...` rather than the full absolute path. Tool call arguments (Read/Write/Bash) still need real resolved paths — this rule applies to text that gets displayed or written, not tool inputs.

For team-scoped or cross-machine content, `~/...` is still wrong because it only resolves on one user's machine. Use a placeholder (e.g. `~our_path/`) or refer to the location by GitHub repo name.
