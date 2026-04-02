# atlassian-cli-skill

`atlassian-cli-skill` is a Claude Code plugin for Confluence operations.

The plugin installs a Confluence-focused skill that uses the local `atlassian-cli` command as its execution backend. On first use, it can bootstrap `atlassian-cli` automatically.

## Features

- read a Confluence page
- search Confluence pages
- create a Confluence page from Markdown
- update an existing Confluence page from Markdown

## Installation

This repository is published as a Claude Code plugin marketplace.

### 1. Add the marketplace

```text
/plugin marketplace add jiongQAQ/atlassian-cli-skill
```

### 2. Install the plugin

```text
/plugin install atlassian-cli-skill@jiongqaq-tools
```

You can also use the CLI form:

```bash
claude plugin marketplace add jiongQAQ/atlassian-cli-skill
claude plugin install atlassian-cli-skill@jiongqaq-tools
```

## Configuration

Copy the example environment file:

```bash
curl -fsSL https://raw.githubusercontent.com/jiongQAQ/atlassian-cli-skill/main/plugins/atlassian-cli-skill/skills/confluence/assets/.atlassian-cli.env.example -o ~/.atlassian-cli.env
chmod 600 ~/.atlassian-cli.env
```

If you already cloned this repository, you can also copy the file directly:

```bash
cp ./plugins/atlassian-cli-skill/skills/confluence/assets/.atlassian-cli.env.example ~/.atlassian-cli.env
chmod 600 ~/.atlassian-cli.env
```

Fill in the required values:

- `CONFLUENCE_URL`
- `CONFLUENCE_SSL_VERIFY`

For Atlassian Cloud:

- `CONFLUENCE_USERNAME`
- `CONFLUENCE_API_TOKEN`

Token creation guide:
- <https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/>

For Server / Data Center:

- `CONFLUENCE_PERSONAL_TOKEN`

Optional alias:

- `CONFLUENCE_TOKEN`

Optional shell auto-load:

```bash
if [ -f "$HOME/.atlassian-cli.env" ]; then
  source "$HOME/.atlassian-cli.env"
fi
```

## Usage

After installation, ask Claude Code to use the plugin skill:

```text
使用 /atlassian-cli-skill:confluence 读取 pageId=544882063 的 Confluence 页面
使用 /atlassian-cli-skill:confluence 搜索标题里包含“接口设计”的 Confluence 页面
使用 /atlassian-cli-skill:confluence 把本地 design.md 更新到 Confluence 页面 544882063
```

The plugin is limited to Confluence operations.

## Repository Layout

```text
.
├── .claude-plugin/marketplace.json
├── plugins/
│   └── atlassian-cli-skill/
│       ├── .claude-plugin/plugin.json
│       └── skills/confluence/
└── atlassian-cli-skill/
```

- `.claude-plugin/marketplace.json` defines the marketplace catalog.
- `plugins/atlassian-cli-skill/` contains the installable Claude Code plugin.
- `atlassian-cli-skill/` is the legacy standalone skill layout retained for compatibility.

## Validation

Validate the marketplace or plugin locally:

```bash
claude plugin validate .
claude plugin validate ./plugins/atlassian-cli-skill
```

## Related Project

- CLI backend: <https://github.com/jiongQAQ/cli-atlassian>
