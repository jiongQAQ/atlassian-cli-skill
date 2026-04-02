# atlassian-cli-skill

一个给 AI Agent 用的 Confluence Skill。  
它内部通过 `atlassian-cli` 调用 Confluence，但正常使用时不需要人手动去敲 CLI。

这个 skill 负责把常见工作流封装好，例如：

- 读取 Confluence 页面
- 搜索 Confluence 页面
- 从本地 Markdown 创建或更新 Confluence 页面

## 仓库结构

```text
.
├── README.md
└── atlassian-cli-skill/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── assets/
    │   └── .atlassian-cli.env.example
    └── scripts/
        ├── ensure_atlassian_cli.sh
        ├── run_atlassian_cli.sh
        └── confluence_markdown_page.py
```

真正的 skill 内容在 `atlassian-cli-skill/` 目录下。

## 前置条件

### 1. 安装 Skill

有两种推荐方式。

#### 方式 A：通过 `skill-installer` 从 GitHub 安装

如果你的环境已经有系统自带的 `skill-installer`，可以直接在 Agent 里说：

```text
使用 $skill-installer 从 GitHub 安装 jiongQAQ/atlassian-cli-skill 里的 atlassian-cli-skill
```

也可以直接运行安装脚本。

安装到 Claude skills 目录：

```bash
python3 ~/.claude/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo jiongQAQ/atlassian-cli-skill \
  --path atlassian-cli-skill \
  --dest ~/.claude/skills
```

安装到 Codex skills 目录：

```bash
python3 ~/.claude/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo jiongQAQ/atlassian-cli-skill \
  --path atlassian-cli-skill \
  --dest ~/.codex/skills
```

#### 方式 B：手动复制或软链

复制到 Claude：

```bash
cp -R ./atlassian-cli-skill ~/.claude/skills/
```

复制到 Codex：

```bash
cp -R ./atlassian-cli-skill ~/.codex/skills/
```

或者直接做软链：

```bash
ln -s "$(pwd)/atlassian-cli-skill" ~/.claude/skills/atlassian-cli-skill
ln -s "$(pwd)/atlassian-cli-skill" ~/.codex/skills/atlassian-cli-skill
```

安装后重启 Claude / Codex，使 skill 被重新发现。

### 2. 准备环境变量

推荐把认证信息放进 `~/.atlassian-cli.env`，不要直接写进命令行。

可以直接从 skill 自带模板复制：

```bash
cp ./atlassian-cli-skill/assets/.atlassian-cli.env.example ~/.atlassian-cli.env
chmod 600 ~/.atlassian-cli.env
```

然后按你的实际环境填写。

#### 这些字段分别填什么

- `CONFLUENCE_URL`
  填你的 Confluence 根地址。
  Cloud 一般是 `https://your-domain.atlassian.net/wiki`
  Server / Data Center 一般是你公司自己的 Confluence 地址，例如 `https://wiki.example.com`

这个值通常直接从浏览器地址栏就能拿到。

**Cloud 认证字段**

- `CONFLUENCE_USERNAME`

通常填你的 Atlassian 账号邮箱。

- `CONFLUENCE_API_TOKEN`

填 Atlassian Cloud API Token。  
通常去 Atlassian 账号安全页创建：

- `https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/`

**Server / Data Center 认证字段**

- `CONFLUENCE_PERSONAL_TOKEN`

填你在 Confluence 实例里创建的 Personal Access Token。  
通常在产品的个人头像菜单或个人设置里找 `Personal access tokens`。

如果你在界面里找不到这个入口，常见原因有两种：

- 你的实例没有开启 PAT
- 你的管理员禁用了 PAT

这种情况就需要找管理员确认。

**SSL 校验字段**

- `CONFLUENCE_SSL_VERIFY`

默认建议填 `"true"`。  
只有在公司内网、自签名证书、或你明确知道证书校验会失败时，才临时改成 `"false"`。

**兼容别名**

- `CONFLUENCE_TOKEN` 可以作为 `CONFLUENCE_API_TOKEN` 的别名

如果你之前已经有 MCP 风格的旧环境变量，可以继续沿用这个名字。

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
```

更完整一点的自然语言示例：

```text
使用 $atlassian-cli-skill 读取 pageId=544882063 的 Confluence 页面
使用 $atlassian-cli-skill 把本地 design.md 更新到 Confluence 页面 544882063
使用 $atlassian-cli-skill 搜索标题里包含“接口设计”的 Confluence 页面
```

### 2. Skill 内部做了什么

你不需要手动运行 `atlassian-cli`。  
当 AI 使用这个 skill 时，它会：

- 检查本机是否已经安装 `atlassian-cli`
- 如果缺失，则自动通过 `uv` 安装 `cli-atlassian`
- 读取 `~/.atlassian-cli.env`
- 用本地 CLI 去执行 Confluence 的真实读写操作
- 在需要时，用内置脚本把本地 Markdown 转成 Confluence 页面更新命令

所以从使用者视角，重点只有两件事：

- 装好 skill
- 配好 `~/.atlassian-cli.env`

## 适用场景

适合下面这些情况：

- 想通过“安装 skill”的方式直接获得 Confluence 操作能力
- 希望 skill 首次运行时自动补装 `atlassian-cli`
- 不想启动 `mcp-atlassian` server
- 想让 AI 直接去读写 Confluence
- 想把“本地 Markdown -> Confluence 页面”固定成一个 AI 可复用流程

## 安全说明

- 不要把真实 token、邮箱、内网地址提交到仓库
- 认证信息只放在 `~/.atlassian-cli.env`
- 公开仓库里的示例配置必须使用占位值

## 关联项目

- CLI 实现：<https://github.com/jiongQAQ/cli-atlassian>
- 本仓库：<https://github.com/jiongQAQ/atlassian-cli-skill>
