# atlassian-cli-skill

`atlassian-cli-skill` is a reusable skill package for AI agents that need to operate Confluence from the terminal.

This repository distributes one installable skill directory, `atlassian-cli-skill/`. The skill uses the local `atlassian-cli` command as its execution backend and can bootstrap that CLI automatically on first use.

## What It Does

After installation, the skill can help an AI agent:

- read a Confluence page
- search Confluence pages
- create a Confluence page from Markdown
- update an existing Confluence page from Markdown

This repository does not package an MCP server. The skill is intended for environments that support local skills, such as Claude Code or Codex-compatible setups.

## Repository Layout

```text
.
├── README.md
└── atlassian-cli-skill/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── assets/.atlassian-cli.env.example
    └── scripts/
        ├── ensure_atlassian_cli.sh
        ├── run_atlassian_cli.sh
        └── confluence_markdown_page.py
```

The actual skill content lives in `atlassian-cli-skill/`.

## Requirements

- a skill-capable agent environment, such as Claude Code or Codex
- `uv` available on `PATH`
- a working Confluence account and API credential

## Installation

### Install with `skill-installer`

Install to `~/.claude/skills`:

```bash
python3 ~/.claude/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo jiongQAQ/atlassian-cli-skill \
  --path atlassian-cli-skill \
  --dest ~/.claude/skills
```

Install to `~/.codex/skills`:

```bash
python3 ~/.claude/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo jiongQAQ/atlassian-cli-skill \
  --path atlassian-cli-skill \
  --dest ~/.codex/skills
```

### Install manually

Copy:

```bash
cp -R ./atlassian-cli-skill ~/.claude/skills/
cp -R ./atlassian-cli-skill ~/.codex/skills/
```

Or symlink:

```bash
ln -s "$(pwd)/atlassian-cli-skill" ~/.claude/skills/atlassian-cli-skill
ln -s "$(pwd)/atlassian-cli-skill" ~/.codex/skills/atlassian-cli-skill
```

Restart the agent after installation so the skill can be discovered again.

## Configuration

Copy the example environment file:

```bash
cp ./atlassian-cli-skill/assets/.atlassian-cli.env.example ~/.atlassian-cli.env
chmod 600 ~/.atlassian-cli.env
```

Then fill in the required values.

### Required variables

- `CONFLUENCE_URL`
  The base URL of your Confluence instance. This is usually visible in the browser address bar.
- `CONFLUENCE_SSL_VERIFY`
  Set to `"true"` by default. Set to `"false"` only if your environment uses self-signed or otherwise untrusted certificates.

### Cloud authentication

- `CONFLUENCE_USERNAME`
  Your Atlassian account email.
- `CONFLUENCE_API_TOKEN`
  Your Atlassian Cloud API token.

Token creation guide:
- <https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/>

### Server / Data Center authentication

- `CONFLUENCE_PERSONAL_TOKEN`
  A Confluence personal access token from your profile or personal settings.

If your instance does not show a personal access token entry, ask the administrator whether PAT is enabled.

### Optional compatibility alias

- `CONFLUENCE_TOKEN`
  Supported as an alias for `CONFLUENCE_API_TOKEN`.

### Optional shell auto-load

To load the file automatically in new shells:

```bash
if [ -f "$HOME/.atlassian-cli.env" ]; then
  source "$HOME/.atlassian-cli.env"
fi
```

## Usage

Use the skill explicitly in the agent prompt:

```text
使用 $atlassian-cli-skill 读取 pageId=544882063 的 Confluence 页面
使用 $atlassian-cli-skill 搜索标题里包含“接口设计”的 Confluence 页面
使用 $atlassian-cli-skill 把本地 design.md 更新到 Confluence 页面 544882063
```

On first use, the skill:

1. checks whether `atlassian-cli` is installed
2. installs it through `uv` if needed
3. loads `~/.atlassian-cli.env`
4. executes the Confluence operation through the local CLI

## Scope

This skill is intentionally limited to Confluence.

- the skill expects credentials to be managed outside the repository
- the public repository only contains placeholder configuration values

## Related Project

- CLI backend: <https://github.com/jiongQAQ/cli-atlassian>
