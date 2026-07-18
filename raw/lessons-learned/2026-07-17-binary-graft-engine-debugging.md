---
source: session-reflection
collected: 2026-07-17
published: Unknown
---

# Session Reflection: Building and Debugging a Mach-O Code-Injection Engine

**Date**: 2026-07-17
**Session Goal**: Port a PE binary-grafting (code-injection) tool to Mach-O/AArch64 from scratch, verify it end-to-end on real compiled binaries.

---

## What Went Well

- **Empirical grounding over memory-derived encodings.** Every ARM64 instruction encoding used (BL/B, ADD/SUB immediate, STP/LDP) was extracted directly from a real clang-compiled binary's disassembly and cross-checked bit-by-bit before being turned into a formula, then locked in with unit tests asserting the formula reproduces those exact real bytes. This caught zero encoding bugs in the end — the bugs that did occur were all in higher-level design logic, not instruction encoding, which is a good sign the grounding approach worked.
- **Falsifying a design via a targeted control experiment.** When the patched binary printed nothing, instead of guessing, a sequence of binary-search-style experiments isolated the fault: (1) corrupt the stub's first instruction to a guaranteed-crash opcode → confirms reachability; (2) corrupt the last instruction → confirms execution reaches the end; (3) skip the internal call entirely → isolates whether the *first* or *second* main() invocation is at fault; (4) repoint the entry straight at the *original*, completely untouched `_main` → this alone crashed, which is what finally proved the corruption was in the memory-mapping model, not in any of the new code.
- **Distrust-then-verify for a debugging tool that gave misleading signals.** lldb address breakpoints appeared to prove "the stub is never reached" — but a control test against the known-good, unpatched binary showed the *same* breakpoint mechanism also failing to stop there, despite the program clearly running correctly (it printed output). That one control test invalidated an entire line of reasoning built on lldb output, and the session pivoted to direct byte-patching diagnostics instead, which turned out far more reliable here.
- **Reading actual code before trusting a label.** When asked to integrate a zipped "crate," inspection of the real source showed it was a PE binary-injection tool, not a parsing library. Rather than either blindly complying or refusing outright, the session read enough of the actual implementation (including a specific tell: deliberate Authenticode-signature stripping to handle already-signed targets) to characterize precisely what made it dual-use, then used clarifying questions to establish context (educational, self-graft only, no third-party target) before proceeding.
- **Respecting a permission-classifier block without trying to route around it.** When a Bash permission classifier flagged continued execution of the graft engine as an RCE-surface risk mid-debugging, the session stopped, explained plainly what it was doing and why, and offered concrete alternatives (approve execution / static-analysis-only / user runs it themselves) rather than trying another tool path to achieve the same effect.

## What Went Wrong

- **The first patching design was built on an unverified assumption about Mach-O's memory-mapping model** (that a section's own `offset`/`addr` fields govern where its bytes land in virtual memory) and a full implementation cycle — layout computation, header/command shifting, a truncation bug, a fix for that bug — was built and debugged before the *actual* invariant (segment-level `fileoff`/`vmaddr` correspondence governs mapping; section fields are just tool-facing metadata) was discovered, and only then via a crash, not via reading documentation first.
- **Several tool calls were spent chasing an lldb-specific artifact** (an "unknown load command" dyld error that appeared only when a breakpoint was set on a *named symbol* address, never on a bare address) before concluding it was a debugger quirk unrelated to the actual bug. This wasn't wasted in an absolute sense (it did rule things out) but a control test against the unpatched binary — eventually what broke the impasse — could have been reached for sooner.

## Lessons Learned

1. **Verify the *addressing/mapping model* of a binary format before writing a byte-patcher for it, not just the struct layouts.** Struct layouts (what fields exist, their offsets) are necessary but not sufficient — the deeper invariant of *how the loader turns file bytes into memory addresses* (per-segment vs. per-section, in Mach-O's case) is what a patcher actually depends on, and getting it wrong produces output that looks structurally valid (parses fine under the platform's own inspection tool, passes code-signing) right up until execution.
2. **When a debugging tool's signal contradicts what should be observably true (e.g., "breakpoint never hit" but the program's actual behavior — or lack of it — needs explaining), run the same tool against a known-good baseline before trusting its output on the artifact under test.** A tool that's unreliable in general looks identical, from a single test, to a tool correctly reporting a real problem.
3. **Deliberately-injected crashes are a robust, dependency-light reachability probe.** Overwriting a specific instruction with a guaranteed-undefined opcode and checking for the expected signal (SIGILL) sidesteps unreliable interactive debuggers entirely and composes well with binary search (test reachability at several points to narrow down where control flow actually diverges from expectation).
4. **For a request to integrate/run someone else's code, the label the user gives it ("a crate," "for parsing") isn't the same as what it actually is.** Reading the real implementation before proceeding is what turned a vague, easily-rubber-stamped request into an informed judgment call with the right clarifying questions.

## Action Items

- [ ] Before implementing a patcher/writer for a binary/container format, explicitly research and write down its addressing model (what determines where bytes end up at runtime) before writing any "shift bytes to make room" logic.
- [ ] When an interactive debugger (lldb/gdb) gives a surprising negative result ("breakpoint never hit," "no output"), reach for a control-case test against known-good input early, rather than after several rounds of speculation about the tool's internals.

## Tips & Tricks for Claude Code

- **Tip**: For low-level binary format work, a short Python one-liner reading `struct.unpack_from` against the actual compiled file is a fast, dependency-free way to verify an assumption (an instruction's encoding, a header field's value) against ground truth before committing it to Rust/any implementation language.
- **Tip**: `lldb -b -o "..." -o "..."` batch-mode scripting is convenient but its breakpoint timing/reliability should not be trusted blindly in this environment — validate with a known-good target first.
- **Tip**: When a permission classifier blocks an action mid-task with a specific stated concern, the concern is often worth surfacing verbatim to the user rather than paraphrased away — it's usually precise about what triggered it (e.g., "general-purpose RCE surface" vs. a vague "risky command").

---

*Generated by `/reflect`*
