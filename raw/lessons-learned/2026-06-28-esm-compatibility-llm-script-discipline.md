---
source: session-reflection
collected: 2026-06-28
published: Unknown
---

# Session Reflection: ESM Compatibility, Architecture Mismatches, and LLM Script Discipline

**Date**: 2026-06-28
**Session Goal**: Build a Claude Code-style TUI backed by a local MLX model (Qwen), starting from TypeScript/Node.js and ending with a Python/Textual implementation.

---

## What Went Well

- Fast diagnosis of `ERR_REQUIRE_ASYNC_MODULE`: identified that `@mlx-node/lm` only exports an `import` condition (ESM-only) and that bundling to CJS was the cause; switched to `--format esm` + `"type": "module"` in one step.
- Clean module split at the end: `log.py`, `tui.py`, `tools/files.py`, slim `__main__.py` — each file had a single responsibility.
- Logging setup was added non-intrusively: `setup_logging()` called once at entry, child loggers (`qwen.tui`, `qwen.tools.files`) inherited config automatically.
- `@-ref` file injection was a clean design: explicit token (`@path`) rather than heuristic path detection.

## What Went Wrong

- **Significant time invested in a discarded stack.** TypeScript/Ink/tsup was built out before discovering that the target model architecture was incompatible with the Node.js MLX binding. The stack pivot to Python erased all of it.
- **Didn't verify ESM/CJS compatibility before choosing output format.** `@mlx-node/lm`'s `package.json` had `{ "import": "./dist/index.js" }` with no `"require"` condition — this is a clear ESM-only signal that should have been checked before writing a single line of tsup config.
- **Didn't verify model architecture before recommending it.** `Qwen3.5-9B-OptiQ-4bit` uses linear-attention hybrid layers (`linear_attn.in_proj_*`) incompatible with `@mlx-node/lm`'s expected `q_proj/k_proj/v_proj` layout. A quick grep of `config.json` would have surfaced this before any loading attempt.
- **Ran the LLM script without confirming it was appropriate.** Executing `qwen-code -p "Evaluate qwen/__main__.py"` without the `@-ref` expansion in place produced a useless round-trip (model couldn't see the file). Then a follow-up run was interrupted by the user — who stopped it because Qwen is verbose and the injected file would be too large.
- **`verbatimModuleSyntax` left in tsconfig conflicted with `"type": "commonjs"`.** This was a simple config contradiction that should have been caught before the first `tsc --noEmit`.

## Lessons Learned

1. **Check the package.json exports field before choosing a module format.** If a dependency only has `"import"` and no `"require"`, the output must be ESM. This is a 30-second check that prevents a config thrash cycle.

2. **Grep the model config before loading.** When using a native binding with strict weight-layout expectations, scan `config.json` for unexpected architecture signals (`linear_attn`, `mamba`, `rwkv`, `state_space`) before attempting `load()`. A crash in a native thread is harder to diagnose than a config diff.

3. **Don't run LLM scripts to test code during a session.** LLM inference is slow, verbose, and token-count-sensitive. Use it as an offline tool, not an in-session oracle. Verify imports and logic by reading code only; hand off execution to the user.

4. **Complete the tool setup before invoking it.** The `@-ref` expansion was added after the first failed headless run. The correct order: implement → verify the feature works conceptually → then hand off. Don't fire the tool to discover what's missing.

5. **Stack pivots are cheaper when the decision is made earlier.** The user said "rm all files and restart with python directly" only after the TypeScript path hit two successive dead ends. The right trigger to surface the pivot would have been after the first incompatibility (ESM issue) — ask "is this Node.js path firm, or would Python/mlx_lm directly be simpler given the existing main.py?"

## Action Items

- [ ] When setting up any bundler/compiler, check all dependency `package.json` exports objects first; flag ESM-only packages before writing config.
- [ ] Before loading a model with a native binding, grep the model's `config.json` for non-standard attention/layer patterns.
- [ ] Do not execute LLM inference scripts in-session without explicit user instruction. Offer the command for the user to run instead.
- [ ] When a path hits two dead ends in a row, surface the pivot option early rather than pushing deeper.

## Tips & Tricks

- **`npm info <pkg> exports`** prints the exports map in one line — fastest way to check ESM/CJS support before installing.
- **`grep "model_type\|architecture\|linear_attn" config.json`** is a reliable pre-flight for MLX native binding compatibility.
- Python `logging` child loggers (`logging.getLogger("qwen.tui")`) inherit handlers from the root namespace logger automatically — no handler wiring needed in submodules.
- `textual`'s `call_from_thread()` is the correct bridge for updating UI from a background inference thread; direct widget mutation from a non-asyncio thread will corrupt state silently.

---

*Generated by `/reflect`*
