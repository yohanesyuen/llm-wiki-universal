# LLM Wiki

Universal knowledge base. Sources live in `raw/`; compiled articles live in `wiki/`.

- `wiki/index.md` — global article index
- `wiki/log.md` — append-only operation log
- Ingest by invoking the `karpathy-llm-wiki` skill, loaded from the main machine. There is no in-repo ingest script.
  Skill source: https://github.com/yohanesyuen/karpathy-llm-wiki

## Writing to this wiki from another repo

This wiki is meant to be written to from any session, including one rooted in a
different repo. The write protocol is the same everywhere — only how you reach
the repo differs.

**Get write access to the repo:**

- **Local CLI / your own machine:** clone it
  (`git clone https://github.com/yohanesyuen/llm-wiki-universal.git`) and work in
  that checkout. Your git credentials already grant write — nothing else needed.
- **Claude Code on the web, session rooted elsewhere:** ask Claude to
  `add_repo yohanesyuen/llm-wiki-universal`. That pulls this repo into the
  session so it can be cloned, edited, and pushed. The Claude GitHub App must
  have access to the repo (granted once in the Claude GitHub settings).

**The write protocol (do this, not hand-editing `wiki/`):**

1. Branch off `main` — never commit articles directly to `main`.
2. Drop the new source as `raw/<topic>/<YYYY-MM-DD>-<slug>.md`. `<topic>` is the
   subdirectory (e.g. `lessons-learned`, `conventions`); it becomes the article's
   topic. Sanitize first — no personal or confidential info (see
   `wiki/conventions/no-confidential-leak.md`).
3. Compile by invoking the `karpathy-llm-wiki` skill. It finds raw files not yet
   referenced by any article, writes/merges the article, and updates
   `wiki/index.md` and `wiki/log.md`. Do **not** edit files under `wiki/` by hand.
4. Commit (`raw/` source + the generated `wiki/` changes together), push, open a PR.

Note: ingest depends on the `karpathy-llm-wiki` skill, which lives on the main
machine and is **not** checked into this repo — step 3 only works there. From any
other session (a web container, or a session rooted in a different repo) you can
still add to `raw/` and push; run the ingest from the main machine, or note in the
PR that the raw source awaits ingestion.
