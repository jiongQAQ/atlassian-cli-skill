# atlassian-cli-skill

`atlassian-cli-skill` 是一个面向 Claude Code 的 Confluence 插件。

它安装后会提供一个只处理 Confluence 的 skill，底层通过本地 `atlassian-cli` 执行真实操作。首次使用时，如果机器上还没有安装 `atlassian-cli`，插件会自动尝试补装。

## 功能

- 读取 Confluence 页面
- 搜索 Confluence 页面
- 从 Markdown 创建 Confluence 页面
- 用 Markdown 更新已有 Confluence 页面

## 安装

这个仓库按 Claude Code plugin marketplace 的方式分发。

### 1. 添加 marketplace

```text
/plugin marketplace add jiongQAQ/atlassian-cli-skill
```

### 2. 安装插件

```text
/plugin install atlassian-cli-skill@jiongqaq-tools
```

也可以使用命令行：

```bash
claude plugin marketplace add jiongQAQ/atlassian-cli-skill
claude plugin install atlassian-cli-skill@jiongqaq-tools
```

## 配置

先复制示例环境文件：

```bash
curl -fsSL https://raw.githubusercontent.com/jiongQAQ/atlassian-cli-skill/main/plugins/atlassian-cli-skill/skills/confluence/assets/.atlassian-cli.env.example -o ~/.atlassian-cli.env
chmod 600 ~/.atlassian-cli.env
```

如果你已经克隆了仓库，也可以直接从本地复制：

```bash
cp ./plugins/atlassian-cli-skill/skills/confluence/assets/.atlassian-cli.env.example ~/.atlassian-cli.env
chmod 600 ~/.atlassian-cli.env
```

然后按实际环境填写变量。

### 必填项

- `CONFLUENCE_URL`
  Confluence 根地址。一般可以直接从浏览器地址栏获取。
- `CONFLUENCE_SSL_VERIFY`
  默认填 `"true"`。如果你的环境使用自签名证书或证书链不完整，再改成 `"false"`。

### Atlassian Cloud

- `CONFLUENCE_USERNAME`
  你的 Atlassian 账号邮箱。
- `CONFLUENCE_API_TOKEN`
  你的 Atlassian Cloud API Token。

API Token 获取说明：
- <https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/>

### Server / Data Center

- `CONFLUENCE_PERSONAL_TOKEN`
  Confluence 的 Personal Access Token。

如果界面里没有 `Personal access tokens` 入口，需要让管理员确认实例是否启用了 PAT。

### 可选兼容别名

- `CONFLUENCE_TOKEN`
  可作为 `CONFLUENCE_API_TOKEN` 的别名。

### 可选 shell 自动加载

如果希望每次打开终端自动加载环境变量，可以把这段加入 `~/.zshrc` 或 `~/.bashrc`：

```bash
if [ -f "$HOME/.atlassian-cli.env" ]; then
  source "$HOME/.atlassian-cli.env"
fi
```

## 使用方式

安装完成后，可以直接在 Claude Code 里显式调用这个插件提供的 skill：

```text
使用 /atlassian-cli-skill:confluence 读取 pageId=544882063 的 Confluence 页面
使用 /atlassian-cli-skill:confluence 搜索标题里包含“接口设计”的 Confluence 页面
使用 /atlassian-cli-skill:confluence 把本地 design.md 更新到 Confluence 页面 544882063
```

这个插件只支持 Confluence，不包含 Jira 能力。

## 仓库结构

```text
.
├── .claude-plugin/marketplace.json
├── plugins/
│   └── atlassian-cli-skill/
│       ├── .claude-plugin/plugin.json
│       └── skills/confluence/
└── atlassian-cli-skill/
```

- `.claude-plugin/marketplace.json`：marketplace 目录文件
- `plugins/atlassian-cli-skill/`：真正可安装的 Claude Code plugin
- `atlassian-cli-skill/`：保留的旧版 standalone skill 目录，用于兼容之前的安装方式

## 校验

本地可以用下面两条命令检查 marketplace 和 plugin 结构是否正确：

```bash
claude plugin validate .
claude plugin validate ./plugins/atlassian-cli-skill
```

## 相关项目

- CLI 后端：<https://github.com/jiongQAQ/cli-atlassian>
