---
source: https://github.com/wrsmith108/varlock-claude-skill
collected: 2026-07-03
published: Unknown
---

# Varlock Skill for Claude Code

> Secure-by-default environment variable management. Ensures secrets are **never exposed** in Claude sessions.

## Why This Skill?

When working with Claude Code, secrets can accidentally leak into:
- Terminal output
- Claude's input/output context
- Log files or traces
- Git commits or diffs

This skill wraps [Varlock](https://varlock.dev) to enforce secure patterns and prevent accidental exposure.

## Core Principle

**Secrets must NEVER appear in Claude's context.**

| Never Do | Safe Alternative |
|----------|------------------|
| `cat .env` | `cat .env.schema` |
| `echo $SECRET` | `varlock load` |
| `printenv \| grep API` | `varlock load \| grep API` |

## CRITICAL: Security Rules for Claude

### Rule 1: Never Echo Secrets

```bash
# NEVER DO THIS - exposes secret to Claude's context
echo $CLERK_SECRET_KEY
cat .env | grep SECRET
printenv | grep API

# DO THIS - validates without exposing
varlock load --quiet && echo "Secrets validated"
```

### Rule 2: Never Read .env Directly

```bash
# NEVER DO THIS - exposes all secrets
cat .env
less .env
Read tool on .env file

# DO THIS - read schema (safe) not values
cat .env.schema
varlock load  # Shows masked values
```

### Rule 3: Use Varlock for Validation

```bash
# NEVER DO THIS - exposes secret in error
test -n "$API_KEY" && echo "Key: $API_KEY"

# DO THIS - Varlock validates and masks
varlock load
# Output shows: API_KEY sensitive -> masked
```

### Rule 4: Never Include Secrets in Commands

```bash
# NEVER DO THIS - secret in command history
curl -H "Authorization: Bearer sk_live_xxx" https://api.example.com

# DO THIS - use environment variable
curl -H "Authorization: Bearer $API_KEY" https://api.example.com
# Or better: varlock run -- curl ...
```

## Schema File: .env.schema

The schema defines types, validation, and sensitivity for each variable, and is safe to read because it contains no values.

```bash
# Global defaults
# @defaultSensitive=true @defaultRequired=infer

# Public config
# @type=enum(development,staging,production) @sensitive=false
NODE_ENV=development

# Sensitive secrets
# @type=string(startsWith=sk_) @required @sensitive
STRIPE_SECRET_KEY=

# @type=url @required @sensitive
DATABASE_URL=
```

### Security Annotations

| Annotation | Effect | Use For |
|------------|--------|---------|
| `@sensitive` | Redacted in all output | API keys, passwords, tokens |
| `@sensitive=false` | Shown in logs | Public keys, non-secret config |
| `@defaultSensitive=true` | All vars sensitive by default | High-security projects |

## Handling Secret-Related Tasks

### When User Asks to "Check if API key is set"

```bash
# Safe approach
varlock load 2>&1 | grep "API_KEY"

# Never do
echo $API_KEY
```

### When User Asks to "Update a secret"

```
Claude should respond:
"I cannot directly modify secrets for security reasons. Please:
1. Update the value in your .env file manually
2. Or update in your secrets manager (1Password, AWS, etc.)
3. Then run `varlock load` to validate

I can help you update the .env.schema if you need to add new variables."
```

### When User Asks to "Show me the .env file"

```
Claude should respond:
"I won't read .env files directly as they contain secrets. Instead:
- Run `varlock load` to see masked values
- Run `cat .env.schema` to see the schema (safe)
- I can help you modify .env.schema if needed"
```

## Security Checklist for New Projects

- Install Varlock CLI
- Create `.env.schema` with all variables defined
- Mark all secrets with `@sensitive` annotation
- Add `@defaultSensitive=true` to schema header
- Add `.env` to `.gitignore`
- Commit `.env.schema` to version control
- Add `npm run env:validate` to CI/CD
- Document secret rotation procedure
- Never use `cat .env` or `echo $SECRET` in Claude sessions

## Quick Reference Card

| Task | Safe Command |
|------|-------------|
| Validate all env vars | `varlock load` |
| Quiet validation | `varlock load --quiet` |
| Run with env | `varlock run -- <cmd>` |
| View schema | `cat .env.schema` |
| Check specific var | `varlock load \| grep VAR_NAME` |

| Never Do | Why |
|----------|-----|
| `cat .env` | Exposes all secrets |
| `echo $SECRET` | Exposes to Claude context |
| `printenv \| grep` | Exposes matching secrets |
| Read .env with tools | Secrets in Claude's context |
| Hardcode in commands | In shell history |
