---
source: session-reflection
collected: 2026-07-09
published: Unknown
---

# Session Reflection: Parallel Subagent Ingest + Observability Recall

**Date**: 2026-07-09
**Session Goal**: Build a reusable bs4 HTML-to-text extractor in one subagent while a second subagent ingested a pasted URL into an LLM wiki; then answer an ad-hoc question about live context usage and restart a background service.

---

## What Went Well

- **Decoupled the two subagent tasks correctly.** The build task (bs4 extractor) had no dependency on the ingest task, so both were launched as independent background agents. The ingest agent was explicitly told the snippet *might* be available and given a fallback ("don't block waiting on the other agent"). This avoided a false serial dependency — a common trap when two tasks *sound* related but aren't.
- **Held the second task until its required input arrived.** The user asked to ingest "the next url I paste." Rather than guessing or proceeding, the flow launched the build agent immediately and parked the ingest agent until the URL landed. Clean separation of "can start now" vs. "needs input."
- **Went to the structured log store first, not the transcript.** When asked about context usage, the answer came from querying the observability sink (statusLine events carry the full token/context/cost payload) instead of eyeballing the conversation. One query returned an authoritative, timestamped number.
- **Verified the service restart instead of assuming.** After kickstarting the background service, a follow-up check confirmed a fresh PID and running state — closing the loop rather than reporting success blind.

## What Went Wrong

- **No end-to-end confirmation that the two subagents actually chained.** The ingest agent used its skill's internal fetch path and never confirmed whether it used the freshly-built extractor. The two deliverables completed in parallel but were never proven to interoperate. This was surfaced honestly rather than papered over, but it means "wire up an ingestor, then use it" was only half-satisfied — the *build* and the *use* happened, the *wiring* between them wasn't demonstrated.
- **First observability queries were imprecise.** The initial `logsql` queries used a broad free-text OR filter that mostly returned the user's own prompt echoed back, not the metric. It took a couple of iterations (tally event types → inspect one statusLine record → sort-by-time-desc for the latest) to land on the right field. A quick "what fields does a statusLine event carry" inspection up front would have saved two round-trips.

## Lessons Learned

1. **"Do X in a subagent, then use X in another" needs an explicit interop check.** When one agent produces an artifact and another is supposed to consume it, either (a) sequence them and pass the concrete artifact path as required input to the consumer, or (b) accept they're parallel and state plainly that interop wasn't verified. Don't let "they both finished" masquerade as "they worked together."
2. **For live metrics, query the structured sink, not the conversation.** statusLine/hook events forwarded to a log store carry exact context-window %, token splits (cache-creation / cache-read / fresh), cost, and rate-limit usage. Sort by time descending and take the newest record — that's the current state. This beats estimating from transcript length.
3. **Subagent token spend is not in the parent's context metric.** The main-loop statusLine reflects only the orchestrator session. Subagents run on separate transcripts; their token cost (reported in their own completion messages) has to be added manually for a true total.
4. **Restarting a keepalive background service = kickstart -k + verify new PID.** For a launch-managed keepalive job, an in-place restart is one command, and confirming a changed PID + running state is the proof it took.

## Action Items

- [ ] When chaining a producer subagent into a consumer subagent, pass the concrete output path as a required input to the consumer and have it confirm it used that path — or explicitly flag non-verification.
- [ ] When querying the log store for a metric, first inspect one representative record's fields, then write the precise filter — don't start with a broad OR text search.
- [ ] When reporting "context usage," note whether the figure includes subagent spend or is orchestrator-only.

## Tips & Tricks for Claude Code

- **Tip**: Launch independent background agents in parallel and give the downstream one a non-blocking fallback, so a slow/failed sibling never stalls it.
- **Tip**: The latest statusLine log record is a one-query snapshot of context %, token breakdown, cost, and rate-limit consumption — more reliable than estimating.
- **Tip**: `kickstart -k` on a keepalive service does an in-place restart; a follow-up state/PID check confirms it without babysitting.

## Generalization Opportunities

- **Slash Command / Skill**: A small "context-usage" helper that queries the log sink for the newest statusLine record of the current session and prints context %, token split, cost, and rate-limit usage in one line — recurring enough to be worth a one-shot command rather than re-deriving the query each time.

---

*Generated by `/reflect`*
