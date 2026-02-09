
# 🧠 Agenta — Your Local AI Agent for Developers

> **Automate repetitive coding tasks. Run locally. Stay in control.**

Agenta is a **command-line-first AI agent** that helps you write tests, explain code, browse docs, and automate workflows — all from your terminal.  
Unlike cloud-based assistants, Agenta runs **entirely on your machine**, respects your privacy, and lets you **review every action before it executes**.

Think of it as your pair programmer who never sleeps — but always asks for permission.

![Agenta CLI demo](https://via.placeholder.com/800x400?text=Agenta+CLI+Demo+-+Stream+LLM+Response+%2B+Human+Confirmation)

---

## ✨ Features

- **Slash Commands**: `/test`, `/explain`, `/browse`, `/doc` — just like Claude Code
- **Local & Private**: No data leaves your machine (unless you opt in)
- **Human-in-the-Loop**: Preview diffs, confirm actions, stay in control
- **Skill-Based Architecture**: Easily add new capabilities via plugins
- **Secure Execution**: Code runs in Docker sandbox (optional but recommended)
- **Web UI Ready**: One command to launch Streamlit dashboard
- **Multi-Model Support**: Works with OpenAI, Anthropic, Qwen, Ollama, and more

---

## 🚀 Quick Start

### 1. Install
```bash
pip install agenta-cli
# or from source
git clone https://github.com/chisuhua/agenta.git
cd agenta
pip install -e .
```

### 2. Configure
```bash
agenta config set --api-key sk-xxxx --model gpt-4o
# Supports: openai, anthropic, dashscope (Qwen), ollama
```

### 3. Use It!
```bash
# Generate unit tests
agenta /test src/utils.py

# Explain a function
agenta /explain src/auth.py --focus login_user

# Browse and summarize docs
agenta /browse https://fastapi.tiangolo.com/tutorial/

# Launch Web UI
agenta web
```

> 💡 **Safety First**: Agenta will **show you a diff** and ask for confirmation before modifying any file.

---

## 🔧 Core Skills (Built-in)

| Command | Description |
|--------|-------------|
| `/test <file>` | Generate pytest/unittest cases |
| `/explain <file>` | Summarize code logic in plain English |
| `/browse <url>` | Fetch & summarize web content (uses Playwright) |
| `/lint <file>` | Suggest fixes for style/performance issues |
| `/doc <symbol>` | Generate docstrings or API docs |

> Add your own skills by dropping Python modules into `~/.agenta/skills/`.

---

## 🛡️ Security Model

- **No silent writes**: All file modifications require explicit approval
- **Sandboxed execution**: Enable Docker mode to run generated code safely
- **Local context only**: Project memory stored in `.agenta/CLAUDE.md` (never uploaded)
- **Network isolation**: Playwright runs in headless Chromium with no cookies by default

---

## 🌐 Web Interface (Optional)

Run a lightweight Streamlit UI for team sharing:

```bash
agenta web
# → Open http://localhost:8501
```

The Web UI shares the same core engine as the CLI — no duplicated logic.

---

## 📚 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete system architecture and design
- **[QUICKSTART.md](QUICKSTART.md)** - Installation and getting started guide
- **[PLAN.md](PLAN.md)** - Development roadmap and phases
- **[PHASE0_SUMMARY.md](PHASE0_SUMMARY.md)** - Phase 0 implementation summary

---

## 📦 Roadmap

- [ ] Skill marketplace (`agenta skill install github-pr-reviewer`)
- [ ] Git hook integration (auto-review on `pre-commit`)
- [ ] Local RAG with ChromaDB for project-aware answers
- [ ] VS Code extension (Phase 2)

---

## 🤝 Contributing

We welcome plugins, new skills, and security improvements!

```bash
# Create a new skill
cp templates/skill_template.py ~/.agenta/skills/my_skill.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 License

MIT © 2026 Your Name  
Built with ❤️ for developers who value **automation without surrendering control**.

---

> “Agenta doesn’t replace you — it replaces the boring parts so you can focus on the brilliant ones.”

