# LLM Script Discipline in Sessions

**Topic**: lessons-learned
**Updated**: 2026-06-28

---

## Don't Run LLM Inference Scripts In-Session

LLM inference (e.g., running a local MLX/llama.cpp model) is slow, verbose, and token-count-sensitive. Using it as an in-session verification oracle creates several problems:

- **Verbosity**: local models tend to generate long responses; the output floods the conversation context.
- **File injection blowup**: injecting a source file into the prompt (e.g., to ask the model to evaluate code) can push the total prompt+output past a useful size.
- **Slow feedback loop**: a multi-second or multi-minute inference round-trip interrupts the flow of a coding session.
- **No guarantee of correctness**: the model may refuse, hallucinate, or miss issues — making it unreliable as a code correctness gate.

**Instead:** verify imports and logic by reading code. Offer the command to the user and ask them to run it and paste back errors or output.

---

## Surface Stack Pivot Options Early

When a chosen approach hits two dead ends in a row, the right move is to surface the pivot option explicitly rather than pushing deeper. Two successive dead ends (e.g., CJS/ESM incompatibility → model architecture incompatibility) are a signal that the chosen path may not be the right one.

At that point, ask: "Is this [language/stack/library] path firm, or would [simpler alternative] be better given [context]?" A 10-second pivot question avoids building further on an unstable foundation.

The cost of a late pivot is much higher than an early one — all work since the last known-good state is potentially discarded.

---

## See Also

- [Pre-Flight Checks Before Building](preflight-checks-before-building.md)
- [Name the Capability Gap Before Evaluating New Infrastructure](capability-gap-before-infrastructure-eval.md)

---

*Sources: session-reflection 2026-06-28*
*Raw: [../../raw/lessons-learned/2026-06-28-esm-compatibility-llm-script-discipline.md](../../raw/lessons-learned/2026-06-28-esm-compatibility-llm-script-discipline.md)*
