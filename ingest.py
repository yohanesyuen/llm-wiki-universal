"""Ingest raw/ source files into the wiki/.

For each raw .md file not yet referenced by any wiki article, asks the model to
compile it into the appropriate wiki article (create or merge), then writes the
article, updates wiki/index.md, and appends to wiki/log.md.

Thinking is automatically disabled when the job count exceeds --thinking-threshold
(default: 5) to keep bulk ingestion fast. Pass --force-thinking to override.
"""
import argparse
import functools
import json
import logging
import re
from datetime import date
from pathlib import Path

from mlx_lm import load, generate, stream_generate

SCRIPT_DIR = Path(__file__).parent
RAW_DIR = SCRIPT_DIR / "raw"
WIKI_DIR = SCRIPT_DIR / "wiki"

MODEL_REPO = "mlx-community/Qwen3.5-9B-OptiQ-4bit"
THINKING_THRESHOLD = 5
CHARS_PER_TOKEN = 4
MAX_CONTENT_TOKENS = 10_000

LOG_DIR = SCRIPT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_PATH = LOG_DIR / f"{Path(__file__).name}.log"

logger = logging.getLogger(Path(__file__).stem)
logger.setLevel(logging.DEBUG)
_formatter = logging.Formatter("%(asctime)s %(levelname)s %(funcName)s: %(message)s")
_fh = logging.FileHandler(LOG_PATH)
_fh.setFormatter(_formatter)
_ch = logging.StreamHandler()
_ch.setFormatter(_formatter)
logger.addHandler(_fh)
logger.addHandler(_ch)

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _truncate(value, limit=200):
    text = repr(value)
    return text if len(text) <= limit else text[:limit] + "...<truncated>"


def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = ", ".join(_truncate(a) for a in args)
        kw_repr = ", ".join(f"{k}={_truncate(v)}" for k, v in kwargs.items())
        logger.debug(f"enter {func.__name__}({args_repr}{', ' if kw_repr else ''}{kw_repr})")
        try:
            result = func(*args, **kwargs)
        except Exception:
            logger.exception(f"exception in {func.__name__}")
            raise
        logger.debug(f"exit {func.__name__}")
        return result
    return wrapper


def estimate_tokens(text):
    return len(text) // CHARS_PER_TOKEN


@log_calls
def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "untitled"


# ---------------------------------------------------------------------------
# Wiki state
# ---------------------------------------------------------------------------

_RAW_LINK_RE = re.compile(r"\[.*?\]\((../../raw/[^\)]+)\)")


def _compiled_raw_paths():
    """Set of raw-file paths (relative to SCRIPT_DIR) referenced in any wiki article."""
    compiled = set()
    for article in WIKI_DIR.rglob("*.md"):
        if article.name in ("index.md", "log.md"):
            continue
        for line in article.read_text().splitlines():
            if not line.startswith("Raw:"):
                continue
            for m in _RAW_LINK_RE.finditer(line):
                # m.group(1) == "../../raw/<topic>/<file>" relative to wiki/<topic>/
                # strip the "../../" to get path relative to SCRIPT_DIR
                compiled.add(m.group(1).replace("../../", "", 1))
    return compiled


@log_calls
def find_new_raw_files(topics=None):
    """Return [(topic, raw_path), ...] for raw .md files not yet compiled."""
    compiled = _compiled_raw_paths()
    jobs = []
    for raw_path in sorted(RAW_DIR.rglob("*.md")):
        if raw_path.name == ".gitkeep":
            continue
        topic = raw_path.parent.name
        if topics and topic not in topics:
            continue
        rel = str(raw_path.relative_to(SCRIPT_DIR))
        if rel not in compiled:
            jobs.append((topic, raw_path))
    return jobs


@log_calls
def find_existing_articles(topic):
    """Return (paths, markdown_by_path) for existing articles in a topic."""
    topic_dir = WIKI_DIR / topic
    if not topic_dir.exists():
        return [], {}
    paths = sorted(
        p for p in topic_dir.glob("*.md")
        if p.name not in ("index.md", "log.md")
    )
    markdown = {p: p.read_text() for p in paths}
    return paths, markdown


def _article_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled"


def _raw_line_from_markdown(markdown):
    """Extract the Raw: field value from an article, or None."""
    for line in markdown.splitlines():
        if line.startswith("Raw:"):
            return line[4:].strip()
    return None


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """\
You are a wiki compiler for a personal knowledge base.

## Article format

Every wiki article is a markdown file with this frontmatter:

```
---
Title: <title>
Sources: <human-readable attribution, e.g. "Session reflection, 2026-06-27">
Raw: [../../raw/<topic>/<filename>](../../raw/<topic>/<filename>)
Updated: <YYYY-MM-DD>
---

# <title>

<body markdown>
```

- Multiple Raw files → semicolon-separated links on one Raw line.
- Sources: plain attribution text, not file paths.
- body_markdown in your JSON output must include the `# Title` heading and all \
  body sections but NOT the frontmatter (the script adds that).

## Your output

Return exactly one JSON object with no markdown fences or surrounding text:

{
  "title": "<article title>",
  "topic": "<topic slug — same as the raw file's parent directory>",
  "filename": "<kebab-slug.md — the article file name in wiki/<topic>/>",
  "action": "create" | "merge",
  "merge_target": "<existing filename to update, or null>",
  "sources": "<attribution string>",
  "updated": "<YYYY-MM-DD>",
  "overview": "<one sentence summary for the index>",
  "body_markdown": "<full article body starting with # Title heading>",
  "flags_for_review": ["<anything ambiguous>"]
}

Rules:
- action "create": new concept not covered by any existing article. merge_target is null.
- action "merge": new source adds detail to or confirms an existing article. \
  merge_target is the existing filename (e.g. "some-article.md"). \
  body_markdown is the COMPLETE updated body of that article (including the # heading).
- filename must be the concept slug (e.g. "transformer-attention.md"), not the raw file name.
- overview is a single clause, no period.
- today is {{today}}.

## Context

Topic: {{topic}}

### Existing articles in this topic (titles and current content)
{{existing_articles_block}}

### Raw file to ingest
Path: raw/{{topic}}/{{raw_filename}}

{{raw_content}}
"""


def _build_existing_block(paths, markdown_by_path):
    if not paths:
        return "(none)"
    parts = []
    for p in paths:
        md = markdown_by_path[p]
        parts.append(f"#### {p.name}\n\n{md.strip()}")
    return "\n\n---\n\n".join(parts)


def build_system_prompt(topic, raw_path, raw_content, existing_paths, existing_markdown):
    block = _build_existing_block(existing_paths, existing_markdown)
    return (
        _SYSTEM_PROMPT
        .replace("{{today}}", date.today().isoformat())
        .replace("{{topic}}", topic)
        .replace("{{raw_filename}}", raw_path.name)
        .replace("{{raw_content}}", raw_content)
        .replace("{{existing_articles_block}}", block)
    )


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)


@log_calls
def call_model(model, tokenizer, system_prompt, stream=False, thinking=False):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Compile the wiki article JSON for this raw file."},
    ]
    prompt = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, enable_thinking=thinking
    )
    if stream:
        chunks = []
        for response in stream_generate(model, tokenizer, prompt=prompt, max_tokens=8192):
            print(response.text, end="", flush=True)
            chunks.append(response.text)
        print()
        raw_output = "".join(chunks)
    else:
        raw_output = generate(model, tokenizer, prompt=prompt, max_tokens=8192, verbose=False)

    cleaned = _THINK_RE.sub("", raw_output)
    cleaned = re.sub(r"^```(?:json)?|```$", "", cleaned.strip(), flags=re.MULTILINE).strip()
    return json.loads(cleaned, strict=False)


# ---------------------------------------------------------------------------
# Article assembly and wiki updates
# ---------------------------------------------------------------------------

def assemble_article_markdown(article, raw_path, topic, existing_raw_line=None):
    raw_rel = f"../../raw/{topic}/{raw_path.name}"
    new_link = f"[{raw_rel}]({raw_rel})"
    raw_field = (existing_raw_line + "; " + new_link) if existing_raw_line else new_link
    frontmatter = "\n".join([
        "---",
        f"Title: {article['title']}",
        f"Sources: {article['sources']}",
        f"Raw: {raw_field}",
        f"Updated: {article['updated']}",
        "---",
    ])
    return frontmatter + "\n\n" + article["body_markdown"].strip() + "\n"


@log_calls
def update_index(topic, article_title, article_rel, overview):
    index_path = WIKI_DIR / "index.md"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    text = index_path.read_text() if index_path.exists() else "# Knowledge Base Index\n"
    today = date.today().isoformat()
    row = f"| [{article_title}]({article_rel}) | {overview} | {today} |"
    heading = f"## {topic}"

    lines = text.splitlines()
    if heading not in lines:
        lines += [
            "",
            heading,
            f"{topic.replace('-', ' ').capitalize()} topic.",
            "",
            "| Article | Summary | Updated |",
            "|---|---|---|",
            row,
        ]
    else:
        h_idx = lines.index(heading)
        end_idx = next(
            (i for i in range(h_idx + 1, len(lines)) if lines[i].startswith("## ")),
            len(lines),
        )
        section = lines[h_idx:end_idx]
        link_frag = f"]({article_rel})"
        for i, line in enumerate(section):
            if line.startswith("|") and link_frag in line:
                section[i] = row
                break
        else:
            last_row = max(
                (i for i, l in enumerate(section) if l.startswith("|")), default=None
            )
            if last_row is not None:
                section.insert(last_row + 1, row)
            else:
                section += ["", "| Article | Summary | Updated |", "|---|---|---|", row]
        lines[h_idx:end_idx] = section

    index_path.write_text("\n".join(lines).strip() + "\n")


@log_calls
def append_log(article_title, cascade_titles=()):
    log_path = WIKI_DIR / "log.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    text = log_path.read_text() if log_path.exists() else "# Wiki Log\n"
    today = date.today().isoformat()
    entry_lines = [f"## [{today}] ingest | {article_title}"]
    entry_lines += [f"- Updated: {t}" for t in cascade_titles]
    log_path.write_text(text.rstrip("\n") + "\n\n" + "\n".join(entry_lines) + "\n")


# ---------------------------------------------------------------------------
# Per-file pipeline
# ---------------------------------------------------------------------------

@log_calls
def process_raw_file(topic, raw_path, model, tokenizer, stream=False, thinking=False):
    raw_content = raw_path.read_text()
    if estimate_tokens(raw_content) > MAX_CONTENT_TOKENS:
        logger.warning(f"[{topic}] {raw_path.name}: over token budget, truncating")
        raw_content = raw_content[: MAX_CONTENT_TOKENS * CHARS_PER_TOKEN]

    existing_paths, existing_markdown = find_existing_articles(topic)

    # Only pass existing content that fits within budget (skip oversized articles)
    budget = MAX_CONTENT_TOKENS * CHARS_PER_TOKEN - len(raw_content)
    included_paths, included_markdown = [], {}
    for p in existing_paths:
        md = existing_markdown[p]
        if len(md) <= budget:
            included_paths.append(p)
            included_markdown[p] = md
            budget -= len(md)

    system_prompt = build_system_prompt(
        topic, raw_path, raw_content, included_paths, included_markdown
    )
    article = call_model(model, tokenizer, system_prompt, stream=stream, thinking=thinking)

    topic_dir = WIKI_DIR / topic
    topic_dir.mkdir(parents=True, exist_ok=True)

    existing_raw_line = None
    if article.get("action") == "merge" and article.get("merge_target"):
        target_path = topic_dir / article["merge_target"]
        if target_path.exists():
            existing_raw_line = _raw_line_from_markdown(target_path.read_text())
        else:
            logger.warning(
                f"merge_target '{article['merge_target']}' not found; creating new file instead"
            )
            target_path = topic_dir / article["filename"]
    else:
        target_path = topic_dir / article["filename"]

    markdown = assemble_article_markdown(article, raw_path, topic, existing_raw_line)
    target_path.write_text(markdown)
    print(f"[{topic}] {'merged' if existing_raw_line else 'created'} {target_path.relative_to(SCRIPT_DIR)}")

    article_rel = f"{topic}/{target_path.name}"
    update_index(topic, article["title"], article_rel, article["overview"])
    append_log(article["title"])

    return [f"[{topic}/{target_path.name}] {f}" for f in article.get("flags_for_review", [])]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

@log_calls
def main():
    parser = argparse.ArgumentParser(description="Ingest raw/ files into wiki/.")
    parser.add_argument("--topics", nargs="+", metavar="TOPIC",
                        help="process only these topic subdirectories (default: all)")
    parser.add_argument("--stream", action="store_true",
                        help="stream model output to stdout")
    parser.add_argument("--thinking", action="store_true",
                        help="enable model thinking (auto-disabled when job count > threshold)")
    parser.add_argument("--force-thinking", action="store_true",
                        help="keep thinking on regardless of job count")
    parser.add_argument("--thinking-threshold", type=int, default=THINKING_THRESHOLD,
                        metavar="N",
                        help=f"disable thinking when job count > N (default: {THINKING_THRESHOLD})")
    parser.add_argument("--dry-run", action="store_true",
                        help="list pending jobs and exit without calling the model")
    args = parser.parse_args()

    jobs = find_new_raw_files(topics=set(args.topics) if args.topics else None)

    if not jobs:
        print("No new raw files to ingest.")
        return

    print(f"Found {len(jobs)} raw file(s) to ingest:")
    for topic, raw_path in jobs:
        print(f"  [{topic}] {raw_path.name}")

    if args.dry_run:
        return

    thinking = args.thinking
    if thinking and not args.force_thinking and len(jobs) > args.thinking_threshold:
        print(
            f"\nJob count ({len(jobs)}) > threshold ({args.thinking_threshold}): "
            f"disabling thinking for this run. Use --force-thinking to override."
        )
        thinking = False

    model, tokenizer = load(MODEL_REPO)

    all_flags = []
    for topic, raw_path in jobs:
        try:
            flags = process_raw_file(
                topic, raw_path, model, tokenizer,
                stream=args.stream, thinking=thinking,
            )
            all_flags.extend(flags)
        except Exception:
            logger.exception(f"failed to process {raw_path}")
            print(f"[{topic}] ERROR on {raw_path.name} — see logs/{LOG_PATH.name}")

    if all_flags:
        print("\nFlags for review:")
        for f in all_flags:
            print(f"  - {f}")
    else:
        print("\nDone. No flags.")


if __name__ == "__main__":
    main()
