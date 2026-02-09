非常好！我们将以 **OpenCode**（一个开源的、类 Claude Code 的智能体系统）为参考蓝本，为你量身定制一套**务实、可执行、分阶段演进**的开发路径。该路径聚焦于 **CLI 优先、人类反馈闭环、轻量安全、后期可扩展 Web（Streamlit）** 的目标，并明确每个阶段的架构、功能、验收标准。

---

## 🧭 总体演进策略（4 阶段）

| 阶段 | 目标 | 核心原则 | 周期 |
|------|------|--------|------|
| **Phase 0: 基石搭建** | 可运行的 CLI 框架 + 最小 LLM 调用 | “Hello Agent” 必须跑通 | 3–5 天 |
| **Phase 1: MVP 智能体** | 实现 1 个真实替代人工的 Skill（如自动写测试） | 解决一个高频痛点 | 1–2 周 |
| **Phase 2: 安全与反馈** | 加入沙箱执行 + 人类确认机制 | 安全第一，可控可靠 | 1 周 |
| **Phase 3: 扩展与 Web 化** | 支持多 Skill + Streamlit UI | 从工具到平台 | 1 周+ |

> ✅ **参考 OpenCode 的关键设计**：
> - 使用 `slash commands`（如 `/test`）触发 Skill
> - 通过 `MCP`（Model Context Protocol）连接外部工具
> - 本地存储上下文（`CLAUDE.md`）
> - 终端优先交互

---

## 📦 Phase 0：基石搭建（“能说话”）

### 🔧 架构概览
```
[User] → (CLI: typer) → [Agent Core] → (LLM API) → [Response]
```

### ✅ 实现功能
1. **CLI 入口**：支持命令 `your-agent ask "Explain this code"`
2. **LLM 封装**：调用 OpenAI/Claude/Qwen（兼容 OpenAI 协议）
3. **流式输出**：在终端逐字打印响应（模拟 Claude Code 的打字效果）
4. **配置管理**：读取 `~/.your-agent/config.yaml`（含 API_KEY）

### 🧪 测试与验收标准
| 测试项 | 验收标准 |
|-------|--------|
| CLI 启动 | `your-agent --help` 显示帮助 |
| 基础问答 | `your-agent ask "What is 2+2?"` 返回正确答案 |
| 流式输出 | 响应逐字出现，非一次性打印 |
| 配置加载 | 修改 config.yaml 后，API 调用使用新 key |
| 错误处理 | 无 API_KEY 时提示清晰错误，不崩溃 |

> 📁 产出物：`main.py`, `config.py`, `llm_client.py`, `cli.py`

---

## 🚀 Phase 1：MVP 智能体（“能干活”）

### 🔧 架构概览
```
[User] → /test file.py → [Skill Router] → [TestWriter Skill] → (LLM) → [Code Output]
```

### ✅ 实现功能
1. **Slash Command 系统**：支持 `/test <file>`、`/explain <file>`
2. **文件读取**：自动读取指定代码文件内容
3. **上下文注入**：将代码 + 指令拼接为 LLM prompt
4. **结果输出**：在终端显示生成的测试代码（带语法高亮）

> 💡 **选择 `/test` 作为首个 Skill 的理由**：
> - 高频重复工作
> - 输入输出明确
> - 低风险（不直接修改原文件）

### 🧪 测试与验收标准
| 测试项 | 验收标准 |
|-------|--------|
| Slash 命令识别 | `your-agent /test main.py` 正确触发 TestWriter |
| 文件读取 | 能读取相对/绝对路径的 Python/JS 文件 |
| Prompt 构造 | LLM 收到包含完整代码 + “Write unit tests” 的指令 |
| 输出质量 | 生成的测试代码语法基本正确（可用 mypy/pylint 初步验证） |
| 错误边界 | 文件不存在时友好提示 |

> 📁 产出物：`skills/test_writer.py`, `skill_router.py`, `prompt_templates/test.j2`

---

## 🛡️ Phase 2：安全与人类反馈（“可信任”）

### 🔧 架构概览
```
[User] → /fix bug.py → [Skill] → (LLM) → [Diff Preview] → [Human Confirm?] → [Apply?]
                              ↓
                      [Sandbox Executor (Docker)]
```

### ✅ 实现功能
1. **Diff 预览**：生成修改建议时，输出 `unified diff` 格式
2. **人类确认**：使用 `rich.prompt.Confirm` 询问是否应用
3. **沙箱执行**（可选但推荐）：
   - 若 Skill 涉及代码执行（如 `/run-test`），在 Docker 中运行
   - 禁用网络、只读挂载、超时限制
4. **本地上下文记忆**：将项目信息写入 `./.your-agent/CLAUDE.md`

### 🧪 测试与验收标准
| 测试项 | 验收标准 |
|-------|--------|
| Diff 预览 | 修改建议以 `--- old\n+++ new\n@@@...` 格式显示 |
| 人类中断 | 用户输入 `n` 后，不修改任何文件 |
| 沙箱隔离 | 在容器中运行的代码无法访问外网或父目录 |
| 上下文持久化 | 第二次运行时能引用之前对话中的项目信息 |
| 安全兜底 | 任何异常不导致原文件损坏 |

> 📁 产出物：`human_feedback.py`, `sandbox_executor.py`, `memory/local_memory.py`

---

## 🌐 Phase 3：扩展与 Web 化（“可分享”）

### 🔧 架构概览
```
CLI Layer ←→ Shared Core ←→ Streamlit Web
               ↑
        [Skill Registry]
        ├── /test
        ├── /browse (Playwright)
        └── /doc (RAG)
```

### ✅ 实现功能
1. **Skill 注册机制**：自动发现 `skills/` 目录下的所有 Skill
2. **Playwright 集成**：实现 `/browse --url=https://api.example.com/docs` 抓取网页内容供 LLM 使用
3. **Streamlit Web UI**：
   - 输入框 + 提交按钮
   - 流式显示响应
   - 支持所有 CLI 命令（如输入 `/test main.py`）
4. **多模型支持**：通过配置切换 Claude/OpenAI/Qwen

### 🧪 测试与验收标准
| 测试项 | 验收标准 |
|-------|--------|
| 新 Skill 自动加载 | 添加 `skills/lint.py` 后，`/lint` 命令立即可用 |
| Playwright 抓取 | 能登录（如有 Cookie）、提取正文、防反爬 |
| Web-CLI 一致性 | 在 Web 输入 `/test x.py` 与 CLI 结果一致 |
| 模型切换 | 修改 config 后，请求发送到新模型 |
| 并发安全 | 多用户使用 Web 版时，上下文不混淆 |

> 📁 产出物：`skills/browse.py`, `streamlit_app.py`, `model_router.py`

---

## 📊 整体架构图（Phase 3 完成后）

```
┌───────────────────────┐      ┌───────────────────────┐
│       CLI User        │      │      Web User         │
│  your-agent /test ... │◄────►│  Streamlit Browser    │
└───────────┬───────────┘      └───────────▲───────────┘
            │                              │
            ▼                              │
┌──────────────────────────────────────────┴───────────────┐
│                  Shared Agent Core                       │
│  • Skill Router    • Human Feedback     • Memory System  │
│  • Model Router    • Config Manager                     │
└────────────┬───────────────────────┬─────────────────────┘
             │                       │
             ▼                       ▼
┌───────────────────────┐ ┌───────────────────────────────┐
│   AI/ML Core          │ │   Execution Sandbox           │
│  • LLM Clients        │ │  • Docker Runner              │
│  • RAG (ChromaDB)     │ │  • Playwright Browser         │
│  • Prompt Templates   │ │  • File/Network Isolation     │
└───────────────────────┘ └───────────────────────────────┘
```

---

## 🛠️ 工具链推荐（全 Python 生态）

| 用途 | 工具 |
|------|------|
| CLI 框架 | `typer`（比 click 更现代） |
| 终端美化 | `rich`（表格/进度条/Markdown） |
| 异步 HTTP | `httpx`（支持 SSE 流） |
| 网页自动化 | `playwright`（官方 Python 版） |
| 向量存储 | `chromadb`（单机文件模式） |
| Web UI | `streamlit` |
| 测试 | `pytest` + `responses`（mock API） |
| 打包 | `pip install -e .` + `pyinstaller`（可选） |

---

## ✅ 成功标志（最终验收）

你的智能体达到以下任一，即证明 MVP 成功：
- **你不再手动写单元测试**（全部交给 `/test`）
- **同事主动安装你的工具** 解决某个重复任务
- **Web 版每天被使用 >5 次**

---

## ⚠️ 关键提醒（来自 OpenCode 的教训）

1. **不要过早抽象**：先让 `/test` 跑起来，再考虑通用 Skill 框架
2. **安全必须前置**：任何文件写入前必须有确认机制
3. **本地优先**：避免依赖云端服务，确保离线可用
4. **日志即文档**：用 `CLAUDE.md` 记录每次交互，便于调试和复盘

---

按照这个路径，你可以在 **4–6 周内** 交付一个真正替代人工工作的智能体 CLI 工具，并具备平滑扩展到 Web 的能力。**记住：第一个 Skill 的价值，远大于完美的架构**。现在就开始 Phase 0 吧！🚀
