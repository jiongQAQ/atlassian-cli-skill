---
name: atlassian-cli-skill
description: Use the local `atlassian-cli` command to read, search, create, update, and comment on Jira and Confluence without starting an MCP server. Trigger this skill when the task is to operate Jira issues, Jira projects, Confluence pages, or to sync a local Markdown file into Confluence through the terminal, especially when credentials are already provided by `~/.atlassian-cli.env`.
---

# Atlassian CLI Skill

## Overview

Use the installed `atlassian-cli` as the execution backend.
Prefer the bundled wrapper script so the skill can bootstrap `atlassian-cli` when missing and reuse `~/.atlassian-cli.env` without repeating environment variables in every command.

## Preconditions

- Prefer running `scripts/run_atlassian_cli.sh --help` before the first live operation in a fresh shell.
- If `atlassian-cli` is missing, let `scripts/ensure_atlassian_cli.sh` install it through `uv`.
- Keep `uv` available on `PATH` for first-time bootstrap.
- Expect credentials to come from `~/.atlassian-cli.env` unless the current shell already exports the same variables.
- Use `--json` whenever the result needs to be parsed or summarized.

## Core Workflow

1. Start with `scripts/run_atlassian_cli.sh ...` for direct Jira or Confluence operations.
2. Use raw `atlassian-cli ...` only when the shell is already configured and there is no benefit from the wrapper.
3. Let `scripts/run_atlassian_cli.sh` handle CLI bootstrap and environment loading before the actual command runs.
4. Prefer `scripts/confluence_markdown_page.py` when updating or creating a Confluence page from a local Markdown file because it derives the page title from the first H1 and strips the duplicate H1 from the body.
5. Read back the target issue or page after a write operation when correctness matters.

## Jira Operations

Use the wrapper script for the standard commands:

```bash
scripts/run_atlassian_cli.sh jira project list --json
scripts/run_atlassian_cli.sh jira issue get PROJ-123 --json
scripts/run_atlassian_cli.sh jira issue search --jql 'project = PROJ ORDER BY updated DESC' --json
scripts/run_atlassian_cli.sh jira issue create \
  --project-key PROJ \
  --summary 'Ship CLI skill' \
  --issue-type Task \
  --description 'Created from atlassian-cli-skill.' \
  --json
scripts/run_atlassian_cli.sh jira issue update PROJ-123 --summary 'New title' --json
scripts/run_atlassian_cli.sh jira issue comment add PROJ-123 --body 'Done.' --json
```

Use `jira issue search` first when the exact issue key is unknown.
Use `jira issue update --status ...` only when a simple status transition is enough; otherwise call the dedicated transition command.

## Confluence Operations

Use the wrapper script for direct page operations:

```bash
scripts/run_atlassian_cli.sh confluence page get 544882063 --json
scripts/run_atlassian_cli.sh confluence page search --query 'text ~ "\"CLI\""' --json
scripts/run_atlassian_cli.sh confluence page create \
  --space-key DOC \
  --title 'CLI Usage' \
  --body-file ./body.md \
  --json
scripts/run_atlassian_cli.sh confluence page update 544882063 \
  --title 'CLI Usage' \
  --body-file ./body.md \
  --json
```

Use `confluence page get` after writes when the page title, version, or content must be confirmed.

## Markdown Sync

Use `scripts/confluence_markdown_page.py` for Markdown-to-Confluence workflows.
The script:

- reads a local Markdown file,
- extracts the first H1 as the page title when `--title` is omitted,
- removes that H1 from the page body to avoid duplicate titles,
- calls `atlassian-cli confluence page create` or `update`,
- supports `--dry-run` so the final CLI command can be inspected without changing Confluence.

Examples:

```bash
python3 scripts/confluence_markdown_page.py update 544882063 ./design.md --json
python3 scripts/confluence_markdown_page.py create ./design.md --space-key DOC --parent-id 123456 --json
python3 scripts/confluence_markdown_page.py update 544882063 ./design.md --dry-run
```

## Verification

- Run a `--help` command first if the environment is uncertain.
- Use `--json` on read or search commands when the result will be parsed.
- After create or update operations, read the target issue or page back and verify the critical fields.
- Keep secrets in `~/.atlassian-cli.env`; do not embed tokens or internal URLs into the skill files.

## Resources

- `scripts/ensure_atlassian_cli.sh`: Install `atlassian-cli` automatically through `uv` when the command is missing.
- `scripts/run_atlassian_cli.sh`: Load `~/.atlassian-cli.env` if present, then execute `atlassian-cli`.
- `scripts/confluence_markdown_page.py`: Create or update a Confluence page from Markdown with title extraction and H1 stripping.
