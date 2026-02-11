# 🏗️ Agenta 最终架构设计文档
## CLI + Streamlit 智能体系统（类 Claude Code / OpenCode）

**版本**: 1.0  
**日期**: 2026-02-09  
**状态**: Final Design

---

## 📋 目录

1. [系统概述](#系统概述)
2. [设计原则](#设计原则)
3. [整体架构](#整体架构)
4. [核心组件](#核心组件)
5. [数据流](#数据流)
6. [技术栈](#技术栈)
7. [安全模型](#安全模型)
8. [扩展机制](#扩展机制)
9. [部署架构](#部署架构)
10. [性能考量](#性能考量)

---

## 📖 系统概述

### 愿景
Agenta 是一个**本地优先**、**人类可控**的 AI 智能体系统，通过 CLI 和 Web UI 两种交互方式，帮助开发者自动化编码任务，如编写测试、解释代码、浏览文档等。

### 核心特性
- **双接口支持**: CLI（命令行）+ Streamlit（Web UI）
- **Slash Command**: 类 Claude Code 的 `/test`, `/explain`, `/browse` 等指令
- **人类反馈闭环**: 所有文件修改前需用户确认
- **本地运行**: 数据不离开用户机器（除非显式调用外部 LLM）
- **可扩展 Skill 系统**: 插件式架构，用户可自定义 Skill
- **安全沙箱**: Docker 隔离执行生成的代码
- **多模型支持**: OpenAI、Claude、Qwen、Ollama 等

### 与参考系统的对比

本节对比 Agenta 与四个主流AI编程工具的核心架构差异，以明确 Agenta 的设计定位。

| 特性 | **Aider** | **OpenHands** | **Claude Code** | **Agenta** |
|------|-----------|--------------|----------------|------------|
| **定位** | AI结对编程工具 | 自主代理系统 | VS Code AI助手 | **CLI优先智能体** |
| **交互方式** | 终端REPL | 事件驱动命令 | IDE集成 | **CLI + Web UI** |
| **工作流** | 用户驱动单步 | 有限循环(MAX_ITERATIONS) | 单线程主循环 | **会话生命周期** |
| **编辑范式** | 结构化补丁(diff) | 命令执行(Action) | 自由文本编辑 | **混合模式** |
| **Git集成** | ✅ 深度原生 | ⚠️ 基础支持 | ⚠️ 依赖IDE | ✅ **原生集成** |
| **人类确认** | ⚠️ 可选 | ✅ 强制 | ⚠️ 部分 | ✅ **强制+预览** |
| **本地运行** | ✅ 完全本地 | ✅ 支持 | ❌ 云端 | ✅ **本地优先** |
| **Web界面** | ❌ 无 | ✅ 有 | ❌ 无 | ✅ **Streamlit** |
| **Skill插件** | ❌ 不支持 | ⚠️ 固定工具集 | ❌ 不支持 | ✅ **动态加载** |
| **沙箱执行** | ❌ 直接执行 | ✅ Docker | ⚠️ 依赖IDE | ✅ **Docker隔离** |

#### 核心差异分析

**1. Aider（18.7k stars）— AI结对编程工具**
- **优势**: 极致的Git集成、结构化补丁编辑、快速响应
- **劣势**: 无沙箱、无插件系统、不支持复杂工作流
- **适用场景**: 单文件快速编辑、代码审查

**2. OpenHands（前OpenDevin）— 自主代理系统**
- **优势**: 完整的事件驱动架构、支持浏览器自动化
- **劣势**: 循环次数硬限制、工具集固定、配置复杂
- **适用场景**: 复杂任务自动化、多步骤工作流

**3. Claude Code — IDE集成助手**
- **优势**: 深度IDE集成、上下文理解强、用户体验好
- **劣势**: 云端依赖、无本地支持、不可扩展
- **适用场景**: VS Code用户、云端协作

**4. Agenta — 本设计**
- **设计理念**: 结合Aider的轻量+OpenHands的自主性
- **核心优势**: 
  - CLI优先但提供Web选项
  - 强制人类确认+Docker沙箱
  - 动态Skill加载系统
  - 本地优先但支持云端LLM
- **适用场景**: 需要安全可控的本地AI编程助手

#### 架构选择理由

基于以上对比，Agenta采用以下设计策略：

1. **工作流机制**: 采用**会话生命周期循环**而非固定次数限制
   - 借鉴OpenCode的灵活性，避免OpenHands的MAX_ITERATIONS限制
   
2. **编辑范式**: 采用**混合模式**
   - 简单编辑使用Aider式的结构化补丁
   - 复杂任务使用OpenHands式的命令执行

3. **人类反馈**: **强制确认+Diff预览**
   - 所有文件修改必须展示diff并获得确认
   - 优于Aider的可选确认、Claude Code的部分确认

4. **扩展性**: **动态Skill加载**
   - 用户可自定义Skill插件
   - 优于OpenHands的固定工具集

---

## 🎯 设计原则

### 1. **CLI First, Web Optional**
- CLI 是一等公民，所有功能必须先在 CLI 实现
- Web UI 通过复用 CLI 核心逻辑实现，不重复开发

### 2. **No Surprises**
- 任何文件修改前必须展示 diff 并等待确认
- 生成的代码在沙箱中运行，不影响主系统

### 3. **Local by Default**
- 配置、上下文、记忆均存储在本地
- LLM 调用支持本地模型（Ollama）

### 4. **Extensible by Design**
- Skill 通过 Python 模块动态加载
- 用户可在 `~/.agenta/skills/` 添加自定义 Skill

### 5. **Fail Safe**
- 所有异常情况不导致数据丢失
- 提供 `--dry-run` 模式预览操作

---

## 🏛️ 整体架构

### 四层架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                         交互层 (Interface Layer)                     │
│  ┌──────────────────────┐          ┌──────────────────────┐         │
│  │   CLI Interface      │          │  Streamlit Web UI    │         │
│  │  • typer commands    │◄────────►│  • Input form        │         │
│  │  • rich output       │          │  • Stream display    │         │
│  │  • prompt_toolkit    │          │  • File browser      │         │
│  └──────────┬───────────┘          └──────────┬───────────┘         │
└─────────────┼──────────────────────────────────┼─────────────────────┘
              │                                  │
              │       Shared Core Interface      │
              ▼                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    智能体核心层 (Agent Core Layer)                    │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                     Orchestrator 调度器                        │   │
│  │  • Command Parser (解析 /test, /explain 等)                   │   │
│  │  • Skill Router (路由到对应 Skill)                             │   │
│  │  • Session Manager (管理会话上下文)                            │   │
│  │  • Human Feedback Loop (确认/中断/修正)                        │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │   Skill     │  │   Memory    │  │   Config    │                 │
│  │  Registry   │  │   System    │  │  Manager    │                 │
│  │  • /test    │  │  • Context  │  │  • API Key  │                 │
│  │  • /explain │  │  • History  │  │  • Model    │                 │
│  │  • /browse  │  │  • RAG      │  │  • Settings │                 │
│  │  • Custom   │  │             │  │             │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
└───────────────────────────────────┬─────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      AI/ML 核心层 (Brain Layer)                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                      LLM Client Manager                        │   │
│  │  • OpenAI API       • Anthropic API      • DashScope (Qwen)   │   │
│  │  • Ollama (Local)   • Stream Handler     • Rate Limiter       │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │   Prompt    │  │     RAG     │  │  Embedding  │                 │
│  │  Templates  │  │   Engine    │  │   Models    │                 │
│  │  • Jinja2   │  │  • ChromaDB │  │  • Local    │                 │
│  │  • System   │  │  • Search   │  │  • Remote   │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
└───────────────────────────────────┬─────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   执行与工具层 (Execution & Tools Layer)              │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                     Sandbox Executor                           │   │
│  │  • Docker Runner      • Network Isolation                      │   │
│  │  • Resource Limits    • Timeout Control                        │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │  Playwright │  │File System  │  │   Git       │                 │
│  │  Web Auto   │  │  Operator   │  │  Integration│                 │
│  │  • Browse   │  │  • Read     │  │  • Diff     │                 │
│  │  • Extract  │  │  • Write*   │  │  • Commit   │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘

                    * Write 操作需人类确认
```

---

## 🔧 核心组件

### 1. 交互层 (Interface Layer)

#### 1.1 CLI Interface (`cli.py`)

**职责**:
- 命令行参数解析
- 用户输入处理
- 终端输出美化
- 交互式确认

**技术实现**:
```python
# 基于 typer 构建
import typer
from rich.console import Console

app = typer.Typer()

@app.command()
def test(file: str):
    """Generate unit tests for a file"""
    # 调用 Orchestrator
    orchestrator.handle_command("/test", {"file": file})

@app.command()
def explain(file: str, focus: str = None):
    """Explain code in a file"""
    orchestrator.handle_command("/explain", {"file": file, "focus": focus})
```

**特性**:
- **Slash 命令支持**: `/test`, `/explain`, `/browse`, `/lint`, `/doc`
- **流式输出**: 使用 `rich.live.Live` 实时显示 LLM 响应
- **语法高亮**: 代码块使用 Pygments 高亮
- **交互确认**: 使用 `rich.prompt.Confirm` 请求用户确认

#### 1.2 Streamlit Web UI (`streamlit_app.py`)

**职责**:
- Web 界面展示
- 输入表单处理
- 会话管理
- 文件上传/下载

**技术实现**:
```python
import streamlit as st
from agenta.core import orchestrator

st.title("🧠 Agenta - AI Coding Assistant")

# 输入框支持 slash 命令
user_input = st.text_input("输入命令（如 /test main.py）或问题")

if user_input:
    # 复用 CLI 核心逻辑！
    with st.spinner("思考中..."):
        result = orchestrator.handle_command_sync(user_input)
        st.markdown(result)
```

**特性**:
- **命令历史**: 使用 `st.session_state` 保存历史记录
- **文件浏览器**: 显示项目文件树
- **Diff 预览**: 使用 `st.code` 展示代码差异
- **一键部署**: `agenta web` 启动，自动打开浏览器

**重要**: Web UI **不重复实现**任何业务逻辑，仅作为 `Orchestrator` 的另一个前端。

---

### 2. 智能体核心层 (Agent Core Layer)

#### 2.1 Orchestrator 调度器 (`orchestrator.py`)

**职责**:
- 解析用户命令（识别 slash 命令）
- 路由到对应的 Skill
- 管理会话上下文
- 实现人类反馈循环

**核心接口**:
```python
class Orchestrator:
    def __init__(self):
        self.skill_registry = SkillRegistry()
        self.session_manager = SessionManager()
        self.config = Config.load()
    
    def handle_command(self, command: str, params: dict) -> AsyncIterator[str]:
        """处理用户命令，返回流式响应"""
        # 1. 解析命令
        skill_name = self._parse_slash_command(command)
        
        # 2. 加载 Skill
        skill = self.skill_registry.get_skill(skill_name)
        
        # 3. 准备上下文
        context = self.session_manager.get_context()
        
        # 4. 执行 Skill (流式返回)
        async for chunk in skill.execute(params, context):
            yield chunk
        
        # 5. 处理结果（如需确认）
        if skill.requires_confirmation:
            await self._request_confirmation(skill.get_changes())
```

**命令解析逻辑**:
```python
def _parse_slash_command(self, user_input: str) -> tuple[str, dict]:
    """
    解析 slash 命令
    例: "/test main.py --focus add_user" 
    -> ("test", {"file": "main.py", "focus": "add_user"})
    """
    if user_input.startswith("/"):
        parts = user_input[1:].split()
        command = parts[0]
        args = self._parse_args(parts[1:])
        return command, args
    else:
        # 非 slash 命令，默认走 ask skill
        return "ask", {"query": user_input}
```

#### 2.2 Skill Registry (`skill_registry.py`)

**职责**:
- 注册和管理所有 Skill
- 动态加载自定义 Skill
- 提供 Skill 查询接口

**实现**:
```python
class SkillRegistry:
    def __init__(self):
        self.skills = {}
        self._load_builtin_skills()
        self._load_custom_skills()
    
    def _load_builtin_skills(self):
        """加载内置 Skills"""
        from agenta.skills import test_writer, code_explainer, web_browser
        self.register(test_writer.TestWriterSkill())
        self.register(code_explainer.CodeExplainerSkill())
        self.register(web_browser.WebBrowserSkill())
    
    def _load_custom_skills(self):
        """从 ~/.agenta/skills/ 动态加载"""
        skill_dir = Path.home() / ".agenta" / "skills"
        if skill_dir.exists():
            for skill_file in skill_dir.glob("*.py"):
                self._load_skill_from_file(skill_file)
    
    def get_skill(self, name: str) -> BaseSkill:
        if name not in self.skills:
            raise SkillNotFoundError(f"Skill '{name}' not found")
        return self.skills[name]
```

#### 2.3 Session Manager (`session_manager.py`)

**职责**:
- 管理会话状态
- 保存对话历史
- 提供上下文检索

**上下文结构**:
```python
@dataclass
class SessionContext:
    session_id: str
    project_root: Path
    current_dir: Path
    history: List[Message]
    memory: Dict[str, Any]  # 项目相关记忆
    
    def add_message(self, role: str, content: str):
        self.history.append(Message(role=role, content=content))
    
    def get_recent_context(self, max_tokens: int = 4000) -> str:
        """获取最近的对话上下文（限制 token 数）"""
        # 实现上下文压缩逻辑
```

#### 2.4 Human Feedback Loop (`human_feedback.py`)

**职责**:
- 展示操作预览（如文件 diff）
- 请求用户确认
- 处理用户反馈（接受/拒绝/修改）

**实现**:
```python
class HumanFeedback:
    @staticmethod
    async def confirm_file_change(file_path: str, diff: str) -> bool:
        """请求用户确认文件修改"""
        console.print(Panel(diff, title=f"修改预览: {file_path}"))
        return Confirm.ask("是否应用此修改？", default=False)
    
    @staticmethod
    async def confirm_code_execution(code: str) -> bool:
        """请求确认代码执行"""
        console.print(Panel(
            Syntax(code, "python", theme="monokai"),
            title="即将在沙箱中执行以下代码"
        ))
        return Confirm.ask("是否继续？", default=False)
```

---

### 3. AI/ML 核心层 (Brain Layer)

#### 3.1 LLM Client Manager (`llm_client.py`)

**已实现** (Phase 0)，支持:
- OpenAI API (GPT-3.5, GPT-4)
- Claude API (通过 OpenAI 兼容端点)
- Qwen API (DashScope)
- Ollama (本地模型)

**增强功能**:
```python
class LLMClientManager:
    def __init__(self, config: Config):
        self.config = config
        self.client = self._create_client()
    
    async def complete_stream(
        self, 
        messages: List[Message],
        temperature: float = 0.7
    ) -> AsyncIterator[str]:
        """流式生成响应"""
        response = await self.client.chat.completions.create(
            model=self.config.model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            temperature=temperature,
            stream=True
        )
        
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
```

#### 3.2 Prompt Templates (`prompt_templates/`)

**职责**:
- 管理各 Skill 的提示词模板
- 使用 Jinja2 渲染上下文

**示例**: `test_writer.j2`
```jinja2
You are an expert Python developer. Generate comprehensive unit tests for the following code.

**Requirements**:
- Use pytest framework
- Cover edge cases
- Include docstrings
- Follow PEP 8 style

**Code to test**:
```python
{{ code }}
```

**Additional context**:
{{ context }}

**Generate**:
Only output the test code, no explanations.
```

#### 3.3 RAG Engine (`rag_engine.py`)

**职责**:
- 索引项目代码
- 检索相关上下文
- 增强 LLM 提示

**实现** (Phase 2+):
```python
class RAGEngine:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(AGENTA_DIR / "chroma"))
        self.collection = self.client.get_or_create_collection("project_code")
    
    def index_project(self, project_root: Path):
        """索引项目代码"""
        for py_file in project_root.rglob("*.py"):
            with open(py_file) as f:
                code = f.read()
            
            # 使用本地 embedding 模型
            self.collection.add(
                documents=[code],
                metadatas=[{"file": str(py_file)}],
                ids=[str(py_file)]
            )
    
    def search(self, query: str, n_results: int = 5) -> List[str]:
        """检索相关代码片段"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results['documents'][0]
```

---

### 4. 执行与工具层 (Execution & Tools Layer)

#### 4.1 Sandbox Executor (`sandbox_executor.py`)

**职责**:
- 在隔离环境中执行代码
- 限制资源使用
- 防止恶意操作

**实现**:
```python
class SandboxExecutor:
    @staticmethod
    async def run_python_code(
        code: str, 
        timeout: int = 30,
        network_allowed: bool = False
    ) -> ExecutionResult:
        """在 Docker 容器中运行 Python 代码"""
        
        # 1. 写入临时文件
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            f.write(code.encode())
            code_file = f.name
        
        try:
            # 2. 构建 Docker 命令
            docker_args = [
                "docker", "run", "--rm",
                f"--network={'bridge' if network_allowed else 'none'}",
                "--read-only",
                "--tmpfs=/tmp:rw,noexec,nosuid,size=50m",
                "--memory=256m",
                "--cpus=1",
                f"--volume={code_file}:/code.py:ro",
                "python:3.11-slim",
                "python", "/code.py"
            ]
            
            # 3. 执行
            result = await asyncio.create_subprocess_exec(
                *docker_args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                result.communicate(), 
                timeout=timeout
            )
            
            return ExecutionResult(
                stdout=stdout.decode(),
                stderr=stderr.decode(),
                exit_code=result.returncode
            )
        
        finally:
            os.unlink(code_file)
```

**安全特性**:
- ✅ 网络隔离（默认禁用）
- ✅ 文件系统只读
- ✅ 资源限制（内存、CPU）
- ✅ 超时保护
- ✅ 临时文件自动清理

#### 4.2 Playwright Web Browser (`web_browser.py`)

**职责**:
- 抓取网页内容
- 提取主要文本
- 处理动态加载内容

**实现** (Phase 3):
```python
class WebBrowser:
    def __init__(self):
        from playwright.async_api import async_playwright
        self.playwright = None
        self.browser = None
    
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        return self
    
    async def fetch_page(self, url: str) -> str:
        """抓取网页并返回主要内容"""
        page = await self.browser.new_page()
        
        try:
            await page.goto(url, wait_until="networkidle")
            
            # 提取主要内容（移除脚本、样式）
            content = await page.evaluate("""
                () => {
                    // 移除脚本和样式
                    document.querySelectorAll('script, style, nav, footer').forEach(e => e.remove());
                    // 返回文本
                    return document.body.innerText;
                }
            """)
            
            return content
        
        finally:
            await page.close()
```

#### 4.3 File System Operator (`file_operator.py`)

**职责**:
- 读取文件内容
- **安全地**写入文件（需确认）
- 生成 diff

**实现**:
```python
class FileOperator:
    @staticmethod
    def read_file(path: Path) -> str:
        """读取文件内容"""
        with open(path, 'r') as f:
            return f.read()
    
    @staticmethod
    def generate_diff(original: str, modified: str) -> str:
        """生成 unified diff"""
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            modified.splitlines(keepends=True),
            fromfile="original",
            tofile="modified"
        )
        return ''.join(diff)
    
    @staticmethod
    async def write_file_with_confirmation(
        path: Path, 
        content: str,
        human_feedback: HumanFeedback
    ) -> bool:
        """写入文件前需人类确认"""
        original = FileOperator.read_file(path) if path.exists() else ""
        diff = FileOperator.generate_diff(original, content)
        
        # 请求确认
        confirmed = await human_feedback.confirm_file_change(str(path), diff)
        
        if confirmed:
            with open(path, 'w') as f:
                f.write(content)
            return True
        
        return False
```

---

## 🌊 数据流

### 场景 1: 用户通过 CLI 执行 `/test main.py`

```
1. User Input
   ↓
   CLI: typer captures "/test main.py"
   ↓
2. Orchestrator
   ↓
   parse_slash_command() → ("test", {"file": "main.py"})
   ↓
3. Skill Router
   ↓
   skill_registry.get_skill("test") → TestWriterSkill
   ↓
4. TestWriterSkill.execute()
   ↓
   • 读取 main.py 内容 (FileOperator)
   • 构造 prompt (PromptTemplate)
   • 调用 LLM (LLMClient)
   ↓
5. LLM Response (Streaming)
   ↓
   async for chunk in llm_client.complete_stream():
       console.print(chunk)  # 实时显示
   ↓
6. (Optional) Write File
   ↓
   若生成的测试需要保存:
   • FileOperator.generate_diff()
   • HumanFeedback.confirm_file_change()
   • 若确认 → 写入文件
   ↓
7. Output
   ↓
   "✅ Tests written to test_main.py"
```

### 场景 2: 用户通过 Web UI 执行相同命令

```
1. User Input
   ↓
   Streamlit: st.text_input("/test main.py")
   ↓
2-7. **完全复用** CLI 的数据流
   ↓
   唯一区别: 输出通过 st.markdown() 而非 console.print()
```

### 场景 3: 执行生成的代码（沙箱模式）

```
1. LLM generates Python code
   ↓
2. HumanFeedback.confirm_code_execution()
   → 展示代码，询问确认
   ↓
3. SandboxExecutor.run_python_code()
   ↓
   • 写入临时文件
   • 启动 Docker 容器
   • 执行代码（限时、限资源、无网络）
   • 返回结果
   ↓
4. Display Result
   ↓
   console.print("stdout: ...")
   console.print("stderr: ...")
```

---

## 🛠️ 技术栈

### 核心依赖

| 用途 | 库/工具 | 版本 | 理由 |
|------|--------|------|------|
| **CLI 框架** | `typer` | >=0.9.0 | 现代、类型安全、自动生成帮助 |
| **终端美化** | `rich` | >=13.0.0 | 支持 Markdown、表格、进度条 |
| **异步 HTTP** | `httpx` | >=0.24.0 | 支持 HTTP/2、连接池 |
| **LLM 客户端** | `openai` | >=1.0.0 | 官方 SDK，流式支持 |
| **配置管理** | `PyYAML` | >=6.0 | 简单、人类可读 |
| **网页自动化** | `playwright` | >=1.40.0 | 官方 Python 版，稳定 |
| **向量存储** | `chromadb` | >=0.4.0 | 本地文件模式，无需服务 |
| **Embedding** | `sentence-transformers` | >=2.2.0 | 本地运行，无需 API |
| **Web UI** | `streamlit` | >=1.28.0 | 快速构建交互界面 |
| **代码高亮** | `pygments` | >=2.16.0 | 语法高亮 |
| **测试** | `pytest` | >=7.4.0 | 单元测试框架 |

### 可选依赖

| 用途 | 库/工具 | 说明 |
|------|--------|------|
| **本地模型** | `ollama` | 运行本地 LLM |
| **代码分析** | `jedi` | Python 代码补全和分析 |
| **Git 操作** | `GitPython` | 生成 diff、提交更改 |

---

## 🔒 安全模型

### 1. 多层安全防护

```
┌─────────────────────────────────────────┐
│  Layer 1: 权限确认                       │
│  • 所有文件写入需人类确认                 │
│  • 显示 diff 预览                        │
└───────────┬─────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│  Layer 2: 沙箱执行                       │
│  • Docker 容器隔离                       │
│  • 禁用网络（可选开启）                   │
│  • 只读文件系统                          │
└───────────┬─────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│  Layer 3: 资源限制                       │
│  • 内存限制: 256MB                       │
│  • CPU 限制: 1 核                        │
│  • 超时: 30 秒                           │
└───────────┬─────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│  Layer 4: 本地存储                       │
│  • 配置: ~/.agenta/config.yaml          │
│  • 上下文: ./.agenta/AGENTA.md          │
│  • API Key 加密存储                      │
└─────────────────────────────────────────┘
```

### 2. 安全策略

#### 文件操作
- **读取**: 无限制（用户主动发起）
- **写入**: 必须经过 `HumanFeedback.confirm_file_change()`
- **删除**: 需二次确认（`Confirm.ask("确定删除？")`）

#### 代码执行
- **默认**: 所有生成的代码在 Docker 沙箱运行
- **网络**: 默认禁用，可通过 `--allow-network` 开启
- **文件**: 只能访问 `/tmp` 临时目录

#### API Key
- **存储**: `~/.agenta/config.yaml` (权限 600)
- **环境变量**: 支持 `AGENTA_API_KEY` 覆盖
- **显示**: 在输出中自动脱敏（显示 `sk-...****`）

#### Web UI
- **认证**: (Phase 3) 支持可选的 Basic Auth
- **CORS**: 仅允许本地访问（默认 localhost:8501）
- **会话隔离**: 每个用户独立 session

---

## 🔌 扩展机制

### Skill 插件系统

#### Skill 基类

```python
# agenta/skills/base.py
from abc import ABC, abstractmethod

class BaseSkill(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Skill 名称（如 'test'）"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Skill 描述"""
        pass
    
    @property
    def requires_confirmation(self) -> bool:
        """是否需要人类确认"""
        return False
    
    @abstractmethod
    async def execute(self, params: dict, context: SessionContext) -> AsyncIterator[str]:
        """执行 Skill，流式返回结果"""
        pass
```

#### 自定义 Skill 示例

用户可在 `~/.agenta/skills/` 创建：

```python
# ~/.agenta/skills/code_reviewer.py
from agenta.skills.base import BaseSkill

class CodeReviewerSkill(BaseSkill):
    name = "review"
    description = "Review code for potential issues"
    requires_confirmation = False  # 仅输出建议，不修改文件
    
    async def execute(self, params: dict, context: SessionContext):
        file_path = params['file']
        code = FileOperator.read_file(file_path)
        
        prompt = f"""Review this code for:
        - Bugs
        - Performance issues
        - Security vulnerabilities
        
        Code:
        ```python
        {code}
        ```
        """
        
        async for chunk in context.llm_client.complete_stream([
            {"role": "user", "content": prompt}
        ]):
            yield chunk
```

**自动加载**: Agenta 启动时扫描 `~/.agenta/skills/*.py`，自动注册所有继承 `BaseSkill` 的类。

---

## 🚀 部署架构

### 本地开发模式

```bash
# 安装
pip install -e .

# 配置
agenta config-set --api-key sk-xxx --model gpt-4

# 使用
agenta /test main.py
```

### Web 模式

```bash
# 启动 Streamlit
agenta web

# 自动打开浏览器访问 http://localhost:8501
```

### Docker 部署（可选）

```dockerfile
# Dockerfile
FROM python:3.11-slim

# 安装依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制源码
COPY src /app/src
WORKDIR /app

# 安装 Agenta
RUN pip install -e .

# 暴露 Streamlit 端口
EXPOSE 8501

# 启动 Web UI
CMD ["streamlit", "run", "src/agenta/streamlit_app.py", "--server.port=8501"]
```

### 云端部署

**选项 1: Streamlit Cloud**
- Push 代码到 GitHub
- 在 Streamlit Cloud 创建 app
- 配置环境变量（AGENTA_API_KEY）

**选项 2: 自托管（VPS）**
```bash
# 使用 systemd 管理服务
sudo cat > /etc/systemd/system/agenta.service <<EOF
[Unit]
Description=Agenta Web UI
After=network.target

[Service]
User=agenta
WorkingDirectory=/opt/agenta
ExecStart=/opt/agenta/venv/bin/streamlit run src/agenta/streamlit_app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable agenta
sudo systemctl start agenta
```

---

## ⚡ 性能考量

### 1. 响应时间

| 操作 | 目标 | 优化手段 |
|------|------|---------|
| CLI 启动 | < 500ms | 延迟加载重模块（Playwright、ChromaDB） |
| LLM 首 token | < 2s | 使用流式 API，立即显示 |
| 文件读取 | < 100ms | 异步 I/O |
| Diff 生成 | < 500ms | 使用 difflib（高效） |
| 沙箱启动 | < 3s | 复用已启动的容器 |

### 2. 资源使用

- **内存**: CLI < 100MB, Web < 200MB
- **磁盘**: ChromaDB 索引 < 100MB/项目
- **网络**: 仅 LLM API 调用，无其他外部请求

### 3. 并发处理

**Web UI**:
- Streamlit 默认单进程，多用户通过 session 隔离
- 对于高并发场景，使用反向代理（Nginx）+ 多实例部署

**CLI**:
- 天然并发安全（每个用户独立进程）

### 4. 缓存策略

```python
# 缓存 LLM 响应（可选）
class CachedLLMClient:
    def __init__(self, client: LLMClient):
        self.client = client
        self.cache = {}  # 或使用 Redis
    
    async def complete_stream(self, messages: List[Message]):
        cache_key = self._generate_key(messages)
        
        if cache_key in self.cache:
            # 从缓存流式返回
            for chunk in self.cache[cache_key]:
                yield chunk
        else:
            response = []
            async for chunk in self.client.complete_stream(messages):
                response.append(chunk)
                yield chunk
            
            self.cache[cache_key] = response
```

---

## 📊 系统对比

### 与其他 AI Coding Assistant 的区别

| 特性 | **Agenta** | GitHub Copilot | Cursor | Continue.dev |
|------|-----------|---------------|--------|-------------|
| **本地运行** | ✅ 完全支持 | ❌ 云端 | ❌ 云端 | ✅ 支持 |
| **CLI 优先** | ✅ 核心设计 | ❌ VS Code 插件 | ❌ IDE 插件 | ❌ VS Code 插件 |
| **Web UI** | ✅ Streamlit | ❌ | ❌ | ❌ |
| **人类确认** | ✅ 所有修改 | 部分 | 部分 | ✅ |
| **沙箱执行** | ✅ Docker | N/A | N/A | ❌ |
| **Skill 插件** | ✅ Python 模块 | ❌ | ❌ | ✅ MCP |
| **多模型** | ✅ | ❌ (GPT only) | ✅ | ✅ |
| **开源** | ✅ MIT | ❌ | ❌ | ✅ Apache |

---

## 🗂️ 项目结构

```
agenta/
├── src/agenta/
│   ├── __init__.py
│   ├── main.py                 # 入口点
│   ├── cli.py                  # CLI 命令 (typer)
│   ├── config.py               # 配置管理
│   ├── llm_client.py           # LLM 客户端
│   │
│   ├── core/
│   │   ├── orchestrator.py     # 调度器
│   │   ├── skill_registry.py   # Skill 管理
│   │   ├── session_manager.py  # 会话管理
│   │   └── human_feedback.py   # 人类反馈
│   │
│   ├── skills/
│   │   ├── base.py             # Skill 基类
│   │   ├── test_writer.py      # /test
│   │   ├── code_explainer.py   # /explain
│   │   ├── web_browser.py      # /browse
│   │   └── doc_generator.py    # /doc
│   │
│   ├── brain/
│   │   ├── prompt_templates/   # Jinja2 模板
│   │   ├── rag_engine.py       # RAG 检索
│   │   └── embedding.py        # 本地 embedding
│   │
│   ├── execution/
│   │   ├── sandbox_executor.py # Docker 沙箱
│   │   ├── file_operator.py    # 文件操作
│   │   └── web_browser.py      # Playwright
│   │
│   └── web/
│       └── streamlit_app.py    # Web UI
│
├── tests/
│   ├── test_cli.py
│   ├── test_skills.py
│   └── test_acceptance.py
│
├── examples/
│   └── usage_examples.py
│
├── docs/
│   ├── ARCHITECTURE.md         # 本文档
│   ├── QUICKSTART.md
│   └── SKILL_DEVELOPMENT.md
│
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## 🔄 演进路径

### Phase 0: ✅ 基础框架（已完成）
- CLI 框架 (typer + rich)
- LLM 客户端 (流式输出)
- 配置管理

### Phase 1: MVP 智能体（当前阶段）
- [ ] Slash 命令系统
- [ ] TestWriterSkill (`/test`)
- [ ] CodeExplainerSkill (`/explain`)
- [ ] 文件操作封装

### Phase 2: 安全与反馈
- [ ] Diff 预览
- [ ] 人类确认机制
- [ ] Docker 沙箱执行
- [ ] 本地上下文记忆 (AGENTA.md)

### Phase 3: 扩展与 Web
- [ ] Skill 动态加载
- [ ] Playwright 网页抓取 (`/browse`)
- [ ] Streamlit Web UI
- [ ] RAG 增强（ChromaDB）

### Phase 4+: 高级特性
- [ ] VS Code 插件
- [ ] Git hook 集成
- [ ] Skill 市场
- [ ] 多人协作模式

---

## 📚 参考资源

### 设计灵感
- **OpenCode**: https://github.com/ModelScope/opencode
- **Claude Code**: https://www.anthropic.com/claude
- **Continue.dev**: https://github.com/continuedev/continue
- **OpenDevin**: https://github.com/OpenDevin/OpenDevin

### 技术文档
- **Typer**: https://typer.tiangolo.com/
- **Rich**: https://rich.readthedocs.io/
- **Streamlit**: https://docs.streamlit.io/
- **ChromaDB**: https://docs.trychroma.com/
- **Playwright**: https://playwright.dev/python/

---

## ✅ 验收标准（最终系统）

系统达到以下标准即为成功交付：

### 功能性
- [x] CLI 支持至少 3 个 Skill (`/test`, `/explain`, `/ask`)
- [ ] Web UI 能执行所有 CLI 命令
- [ ] 所有文件修改前展示 diff 并确认
- [ ] 沙箱能安全执行生成的代码
- [ ] 支持至少 3 种 LLM 提供商（OpenAI、Qwen、Ollama）

### 性能
- [ ] CLI 启动 < 500ms
- [ ] LLM 响应首 token < 2s
- [ ] 文件读取 < 100ms
- [ ] 支持同时处理 10+ 用户（Web 模式）

### 安全
- [ ] 通过代码审计（无明显安全漏洞）
- [ ] 沙箱隔离有效（无法访问外部网络/文件）
- [ ] API Key 不在日志中暴露

### 可用性
- [ ] 新用户 5 分钟内完成安装和首次使用
- [ ] 文档覆盖所有核心功能
- [ ] 错误信息清晰易懂

### 扩展性
- [ ] 用户能在 10 分钟内开发并加载自定义 Skill
- [ ] 支持通过配置文件切换模型

---

## 🎯 总结

Agenta 的最终架构是一个**四层**、**双接口**、**人类可控**的智能体系统：

1. **交互层**: CLI (typer) + Web (Streamlit) 双前端
2. **智能体层**: Orchestrator 调度 + Skill 插件 + 人类反馈
3. **AI 层**: LLM 客户端 + Prompt 模板 + RAG 检索
4. **执行层**: Docker 沙箱 + Playwright + 文件操作

**核心优势**:
- **本地优先**: 数据不离开用户机器
- **人类可控**: 所有危险操作需确认
- **易扩展**: Skill 插件式开发
- **多界面**: CLI 适合开发者，Web 适合团队

**成功指标**:
当你和你的团队**不再手写单元测试**，全部交给 `/test` 命令时，Agenta 就成功了！ 🎉

---

**版本历史**:
- v1.0 (2026-02-09): 初始发布

**维护者**: Agenta Team  
**许可**: MIT License