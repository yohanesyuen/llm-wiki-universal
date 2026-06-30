---
source: https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/refs/heads/main/okf/SPEC.md
collected: 2026-06-28
published: Unknown
---

# Open Knowledge Format (OKF) Specification

## Overview

OKF is a specification for representing knowledge through "a directory of markdown files with YAML frontmatter." It prioritizes accessibility—no schema registry, no central authority, minimal tooling required.

## Core Principles

The format emphasizes four qualities:

1. **Readable** by humans without specialized tools
2. **Parseable** by agents without custom SDKs
3. **Diffable** in version control systems
4. **Portable** across tools and organizations

## Key Structural Elements

**Knowledge Bundle** — A hierarchical collection of markdown documents serving as the distribution unit.

**Concept** — A single markdown file representing one unit of knowledge, which may describe tangible assets (tables, APIs) or abstract ideas (metrics, processes).

**Frontmatter** — Required YAML metadata block at the file's beginning, containing at minimum a `type` field identifying the concept's category.

**Body** — Markdown content following frontmatter, using structural elements like headings, tables, and code blocks.

## Required and Recommended Fields

Every concept must include a `type` value. Recommended fields include `title`, `description`, `resource` (asset URI), `tags`, and `timestamp`. Producers may add custom fields; consumers must gracefully handle unknown keys.

## Cross-linking and Navigation

Concepts link to others using markdown syntax, with two forms supported: bundle-relative paths (beginning with `/`) and standard relative paths. Links express relationships without specifying their type—context comes from surrounding prose.

## Optional Features

**Index files** (`index.md`) provide directory listings supporting progressive disclosure. **Log files** (`log.md`) track changes chronologically. **Citations** document external sources backing claims within concept bodies.

## Conformance Requirements

Bundles conforming to OKF v0.1 must have parseable YAML frontmatter with non-empty `type` fields in all non-reserved markdown files. However, consumers should treat most constraints as guidance rather than strict requirements, tolerating missing fields, unknown types, and broken links.

## Distribution and Versioning

Bundles may be shared as git repositories (recommended for history and attribution), tarballs, or subdirectories. The specification uses semantic versioning, with minor bumps for backward-compatible additions and major bumps for breaking changes.
