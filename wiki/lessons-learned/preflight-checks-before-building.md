---
Title: Pre-Flight Checks Before Building
Sources: Session reflection, 2026-06-28
Raw: "[../../raw/lessons-learned/2026-06-28-esm-compatibility-llm-script-discipline.md](../../raw/lessons-learned/2026-06-28-esm-compatibility-llm-script-discipline.md)"
Updated: 2026-06-28
---

# Pre-Flight Checks Before Building

## Check Package ESM/CJS Compatibility Before Choosing an Output Format

If a dependency only exposes an `"import"` condition in its `package.json` exports map (no `"require"`), bundling to CommonJS will fail at runtime with `ERR_REQUIRE_ASYNC_MODULE` or similar. This is a 30-second check that prevents a full config thrash.

```bash
npm info <pkg> exports
```

If the result contains only `"import"` and no `"require"`, the output format must be ESM (`"type": "module"` + `--format esm` in tsup/esbuild). Any CJS output will fail.

**The failure mode is a runtime crash, not a build error** — the build succeeds, the import fails. Don't wait for the crash to discover the constraint.

## Grep the Model Config Before Loading with a Native Binding

Native MLX/GGML/ONNX bindings have strict expectations about weight tensor names and layer shapes. If the model uses a non-standard architecture (linear attention, state-space, MoE hybrids), the native thread will crash on load with a generic error like "model thread exited."

Before attempting `load()` with any native binding, check:

```bash
grep -E "model_type|architectures|linear_attn|mamba|rwkv|state_space" config.json
```

Key signals that a model is incompatible with standard transformer bindings:
- `linear_attn.*` weight names instead of `q_proj/k_proj/v_proj`
- `model_type` values like `mamba`, `rwkv`, `falcon_mamba`, or custom hybrid names
- `architectures` entries ending in `ForConditionalGeneration` combined with non-standard attention names

The crash is hard to diagnose from the error message alone. A config diff takes ten seconds.

## Verify Architecture Before Investing in a Stack

When picking a library/binding to drive a specific model, verify the model's actual architecture first rather than inferring from name or README. Model names like `Qwen3.5` suggest a well-known architecture, but a suffix like `OptiQ` or a non-standard quantization scheme can indicate a fork with a different weight layout entirely.

Order of checks:
1. Read `config.json` → `architectures`, `model_type`
2. Grep weight names for non-standard patterns
3. Only then choose the loading library

Building out a full stack (bundler config, TUI, type definitions) before verifying model compatibility risks discarding all of it on a single incompatibility.

## Complete Tool Setup Before Invoking It

If a tool has a missing feature (e.g., file injection for a headless LLM runner), implement and verify that feature first, then hand off the tool to the user. Running the tool in an incomplete state to discover what's missing wastes a round-trip and produces confusing output.

Pattern:
1. Implement the feature
2. Read through the code to confirm correctness
3. Hand the invocation to the user
