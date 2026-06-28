# llm-wiki-universal

A personal knowledge base of lessons learned from using LLMs heavily in daily work — maintained by LLMs using the [karpathy-llm-wiki](https://github.com/karpathy/llm-wiki) pattern.

The goal is simple: capture hard-won insights from real sessions, distill them into reusable knowledge, and share them openly in case they help anyone else who relies on LLMs as a core part of their workflow.

> DISCLAIMER: ALL CONTENT IN THIS WIKI IS GENERATED FROM REAL WORK SESSIONS AND SANITIZED TO REMOVE ANY PERSONALLY IDENTIFIABLE OR CONFIDENTIAL INFORMATION BEFORE PUBLICATION. LESSONS ARE GENERIC BY DESIGN — THEY REFLECT PATTERNS, NOT SPECIFICS. USE AT YOUR OWN DISCRETION.

## Structure

```
raw/        # Immutable source material (never edited after ingestion)
wiki/       # Compiled knowledge articles (LLM-maintained)
  index.md  # Global article index
  log.md    # Append-only operation log
```

## How it works

- **Ingest**: source material goes into `raw/`, compiled into `wiki/` articles
- **Query**: ask questions → answered from wiki articles
- **Reflect**: session lessons written to `raw/lessons-learned/` then ingested

The LLM writes and maintains the wiki. The human reads and asks questions.

## Contents

- `wiki/conventions/` — operating rules and process conventions
- `wiki/lessons-learned/` — session retrospectives compiled into reusable insights
