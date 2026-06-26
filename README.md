# llm-wiki-universal

A personal knowledge base maintained by LLMs using the [karpathy-llm-wiki](https://github.com/karpathy/llm-wiki) pattern.

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
