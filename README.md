# BookerPaperTool

BookerPaperTool 是一个基于 OpenAI 兼容 API 的命令行工具集，专注于论文与素材的智能处理，可生成可溯源教科书、技术方案代码、自动化科研流水线等。

本项目由 [BookerGptTool](https://github.com/DracoUnion/BookerGptTool) 拆分而来，聚焦论文/素材 → 教科书、论文 → 代码、科研自动化三类工作流。

## 安装

推荐使用 Python 3.8 或更高版本：

```bash
pip install git+https://github.com/DracoUnion/BookerPaperTool.git
```

也可以在源码目录中安装：

```bash
pip install .
```

安装后提供两个等价的命令：`paper-tool` 和 `BookerPaperTool`。

## 配置 API

工具通过 OpenAI 兼容接口访问大模型。至少需要设置 API Key：

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_CHAT_MODEL="gpt-4o-mini"
```

Windows PowerShell：

```powershell
$env:OPENAI_API_KEY = "sk-..."
$env:OPENAI_BASE_URL = "https://api.openai.com/v1"
$env:OPENAI_CHAT_MODEL = "gpt-4o-mini"
```

`OPENAI_BASE_URL` 可替换为其他 OpenAI 兼容服务的地址。

不要把 API Key 提交到 Git 仓库或写入公开脚本中。

## 基本用法

```bash
paper-tool -h
paper-tool --version
paper-tool <子命令> -h
```

通用参数应放在子命令之前，例如：

```bash
paper-tool --model gpt-4o-mini --retry 3 textbook paper.pdf
```

## 子命令

| 子命令 | 说明 |
| --- | --- |
| `textbook` | 多篇论文到可溯源教科书（原 paper2textbook） |
| `textbook-any` | 多篇素材到可溯源教科书（原 any2textbook） |
| `code` | 从论文生成代码方案（原 paper2code） |
| `auto-research` | 合规科研自动化流水线（文献→假设→实验→写作→投稿包） |

## 开发

添加子命令遵循 `AGENTS.md` 中的约定：提示词、Pydantic 模型、智能体、编排器分层存放。

## 许可证

SATA