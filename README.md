# atlassian-cli-skill

一个基于 `atlassian-cli` 的 Agent Skill，用来在不启动 MCP server 的前提下，通过本地命令直接读写 Jira 和 Confluence。

这个仓库本身不是 CLI 实现；它依赖 `atlassian-cli`。  
但这个 skill 已经把“检查 CLI 是否存在、缺失时自动安装”的逻辑封装进脚本里了。  
Skill 负责把常见工作流封装好，例如：

- 读取 Jira issue / Confluence 页面
- 搜索 Jira / Confluence
- 创建或更新 Jira issue
- 从本地 Markdown 创建或更新 Confluence 页面

## 仓库结构

```text
.
├── README.md
├── .atlassian-cli.env.example
└── atlassian-cli-skill/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── scripts/
        ├── ensure_atlassian_cli.sh
        ├── run_atlassian_cli.sh
        └── confluence_markdown_page.py
```

真正的 Skill 内容在 `atlassian-cli-skill/` 目录下。  
如果要安装到本地 skills 目录，复制这个子目录即可。

## 前置条件

### 1. 安装 Skill

如果你在 Codex 里使用 `skill-installer`，可以直接从 GitHub 安装这个 skill：

```bash
python /path/to/skill-installer/scripts/install-skill-from-github.py \
  --repo jiongQAQ/atlassian-cli-skill \
  --path atlassian-cli-skill
```

或者手动复制：

```bash
cp -R ./atlassian-cli-skill ~/.claude/skills/
```

安装后重启你的 Agent，使 skill 被重新发现。

### 2. 自动安装 `atlassian-cli`

第一次运行 skill 时，优先通过下面这个脚本进入：

```bash
./atlassian-cli-skill/scripts/run_atlassian_cli.sh --help
```

如果本机还没有 `atlassian-cli`，脚本会自动调用：

```bash
uv tool install --force git+https://github.com/jiongQAQ/cli-atlassian
```

所以通常不需要手动先装 CLI。  
前提是本机已经安装了 `uv`。

如果你更愿意手动安装，也可以直接执行：

```bash
uv tool install git+https://github.com/jiongQAQ/cli-atlassian
```

### 3. 准备环境变量

推荐把认证信息放进 `~/.atlassian-cli.env`，不要直接写进命令行。

可以复制模板：

```bash
cp ./.atlassian-cli.env.example ~/.atlassian-cli.env
chmod 600 ~/.atlassian-cli.env
```

然后按你的实际环境填写。

如果希望每次开终端自动生效，把下面这段加到 `~/.zshrc`：

```bash
if [ -f "$HOME/.atlassian-cli.env" ]; then
  source "$HOME/.atlassian-cli.env"
fi
```

## 如何使用

### 1. 在 Agent 中显式调用 Skill

直接在提示词中引用：

```text
使用 $atlassian-cli-skill 去操作 Confluence 页面
使用 $atlassian-cli-skill 把本地 Markdown 更新到指定 Confluence 页面
使用 $atlassian-cli-skill 搜索 Jira 中最近更新的 issue
```

### 2. 直接运行 Skill 自带脚本

先让 skill 自动检查并安装 CLI：

```bash
./atlassian-cli-skill/scripts/run_atlassian_cli.sh --help
```

读取 Confluence 页面：

```bash
./atlassian-cli-skill/scripts/run_atlassian_cli.sh confluence page get 123456 --json
```

搜索 Jira issue：

```bash
./atlassian-cli-skill/scripts/run_atlassian_cli.sh jira issue search \
  --jql 'project = DEMO ORDER BY updated DESC' \
  --json
```

从 Markdown 更新 Confluence 页面：

```bash
python3 ./atlassian-cli-skill/scripts/confluence_markdown_page.py \
  update 123456 ./design.md --json
```

从 Markdown 创建 Confluence 页面：

```bash
python3 ./atlassian-cli-skill/scripts/confluence_markdown_page.py \
  create ./design.md --space-key DOC --parent-id 10000 --json
```

## Markdown 同步脚本行为

`confluence_markdown_page.py` 做了几件事：

- 读取本地 Markdown 文件
- 如果没有传 `--title`，就取第一个 H1 作为页面标题
- 把第一个 H1 从正文里去掉，避免页面标题和正文标题重复
- 调用 `atlassian-cli confluence page create/update`
- 支持 `--dry-run`，先只打印最终命令，不真正写入

示例：

```bash
python3 ./atlassian-cli-skill/scripts/confluence_markdown_page.py \
  update 123456 ./design.md --dry-run
```

## 适用场景

适合下面这些情况：

- 想通过“安装 skill”的方式直接获得 Jira / Confluence 操作能力
- 希望 skill 首次运行时自动补装 `atlassian-cli`
- 已经有 `atlassian-cli`，想给 Claude / Codex 再加一层可复用工作流
- 不想启动 `mcp-atlassian` server
- 想直接通过本地命令访问 Jira / Confluence
- 想把“本地 Markdown -> Confluence 页面”固定成一个稳定流程

## 安全说明

- 不要把真实 token、邮箱、内网地址提交到仓库
- 认证信息只放在 `~/.atlassian-cli.env`
- 公开仓库里的示例配置必须使用占位值

## 关联项目

- CLI 实现：<https://github.com/jiongQAQ/cli-atlassian>
- 本仓库：<https://github.com/jiongQAQ/atlassian-cli-skill>
