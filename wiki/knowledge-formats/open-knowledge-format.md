---
type: concept
tags: [knowledge-management, specification]
title: Open Knowledge Format (OKF)
updated: 2026-07-08
sources: GoogleCloudPlatform/knowledge-catalog; Unknown date
raw: "[2026-06-28-open-knowledge-format-spec.md](../../raw/knowledge-formats/2026-06-28-open-knowledge-format-spec.md)"
---

# Open Knowledge Format (OKF)

A specification for representing knowledge as a directory of markdown files with YAML frontmatter. Designed to be readable by humans without specialized tools, parseable by agents without custom SDKs, diffable in version control, and portable across tools and organizations.

## Structure

A **Knowledge Bundle** is the distribution unit — a hierarchical collection of markdown documents. Each document is a **Concept**: one unit of knowledge (a table, an API, a metric, a process). Every concept file must have a YAML **frontmatter** block as its first element, containing at minimum a `type` field. The markdown body follows, using headings, tables, and code blocks.

## Fields

Required: `type` (non-empty, identifies the concept category).

Recommended: `title`, `description`, `resource` (asset URI), `tags`, `timestamp`.

Producers may add custom fields. Consumers must gracefully handle unknown keys and missing recommended fields.

## Cross-linking

Concepts link to each other using standard markdown link syntax. Two path forms are supported:

- **Bundle-relative**: paths beginning with `/` (from the bundle root)
- **Relative**: standard relative paths from the current file

Links express relationships without naming the relationship type — context comes from surrounding prose.

## Reserved Files

- `index.md` — directory listing; supports progressive disclosure of bundle contents
- `log.md` — append-only change log; tracks what changed and when
- **Citations** — inline references in the body backing claims with external sources

These files are optional but recommended. They are exempt from the `type` conformance requirement.

## Conformance (v0.1)

A conforming bundle must have parseable YAML frontmatter with a non-empty `type` field in every non-reserved markdown file. Consumers are expected to be lenient: tolerate missing fields, unknown types, and broken links rather than failing hard.

## Distribution

Preferred: git repository (preserves history and attribution). Also valid: tarball, subdirectory within a larger repo.

Versioning follows semantic versioning — minor bumps for backward-compatible additions, major bumps for breaking changes.

## Relationship to This Wiki

This wiki's own structure mirrors OKF closely: markdown files with YAML-style frontmatter, an `index.md` global index, a `log.md` append-only operation log, and relative cross-links between articles. OKF can be read as a formalization of the pattern this wiki already uses.

## See Also

- [Wiki Ingest and Cleanup Discipline](../lessons-learned/wiki-ingest-and-cleanup-discipline.md)
- [Deterministic Compiler vs. Agent-Driven Wiki Architecture](deterministic-compiler-vs-agent-wiki.md) — a deterministic parser/compiler pipeline could target OKF-conformant bundles directly for the mechanical layer (link/orphan checks), while merge and conflict-annotation decisions stay agent-driven
