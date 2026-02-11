# 🚀 Agenta CLI - Quick Start Guide

This guide helps you get started with Agenta's Phase 0 implementation - a working CLI framework with LLM integration.

## ✅ What's Implemented (Phase 0)

- ✅ CLI framework with typer
- ✅ Configuration management (~/.agenta/config.yaml)
- ✅ LLM client with streaming support (OpenAI/Claude/Qwen compatible)
- ✅ Beautiful terminal output with rich
- ✅ Error handling and validation
- ✅ Multiple configuration methods (env vars + config file)

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/chisuhua/agenta.git
cd agenta

# Install in development mode
pip install -e .

# Verify installation
agenta --help
```

## 🔧 Configuration

### Method 1: Using CLI Commands

```bash
# Set your API key
agenta config-set --api-key sk-your-openai-key-here

# Optionally, set model and provider
agenta config-set --model gpt-4
agenta config-set --provider openai

# View current configuration
agenta config-show
```

### Method 2: Using Environment Variables

```bash
export AGENTA_API_KEY=sk-your-openai-key-here
# or
export OPENAI_API_KEY=sk-your-openai-key-here
```

### Method 3: Manual Config File

Edit `~/.agenta/config.yaml`:

```yaml
api_key: sk-your-openai-key-here
model: gpt-3.5-turbo
provider: openai
api_base: ""  # Optional: for custom API endpoints
```

## 🎯 Usage Examples

### Basic Question & Answer

```bash
# Ask a simple question
agenta ask "What is 2+2?"

# Ask a coding question
agenta ask "Explain what a decorator is in Python"

# Ask for code generation
agenta ask "Write a function to calculate fibonacci numbers"
```

### Streaming vs Non-Streaming

```bash
# Default: streaming output (character by character)
agenta ask "Explain machine learning"

# Disable streaming (get full response at once)
agenta ask "Explain machine learning" --no-stream
```

## 🧪 Testing

Run the acceptance test suite:

```bash
# Without API key (tests CLI and config only)
python test_acceptance.py

# With API key (tests live LLM calls)
export AGENTA_API_KEY=sk-your-key
python test_acceptance.py
```

## 📊 Phase 0 Acceptance Criteria

| Criteria | Status | Command |
|----------|--------|---------|
| CLI Startup | ✅ Pass | `agenta --help` |
| Version Display | ✅ Pass | `agenta --version` |
| Config Loading | ✅ Pass | `agenta config-show` |
| Config Modification | ✅ Pass | `agenta config-set --model gpt-4` |
| Error Handling | ✅ Pass | `agenta ask "test"` (without API key) |
| Basic Q&A | ✅ Pass | `agenta ask "What is 2+2?"` (with API key) |
| Streaming Output | ✅ Pass | Character-by-character display |

## 🔌 Supported LLM Providers

The LLM client uses OpenAI-compatible API, which works with:

### 1. OpenAI

```bash
agenta config-set --api-key sk-proj-xxxxx
agenta config-set --model gpt-4
agenta config-set --provider openai
```

### 2. Anthropic Claude (via OpenAI-compatible endpoint)

```bash
agenta config-set --api-key sk-ant-xxxxx
agenta config-set --model claude-3-sonnet-20240229
agenta config-set --provider anthropic
agenta config-set --api-base https://api.anthropic.com/v1
```

### 3. Alibaba Qwen (DashScope)

```bash
agenta config-set --api-key sk-xxxxx
agenta config-set --model qwen-turbo
agenta config-set --provider dashscope
agenta config-set --api-base https://dashscope.aliyuncs.com/compatible-mode/v1
```

### 4. Local Models (Ollama)

```bash
agenta config-set --api-key ollama  # Any non-empty string
agenta config-set --model llama2
agenta config-set --provider ollama
agenta config-set --api-base http://localhost:11434/v1
```

## 🐛 Troubleshooting

### "API key not configured" error

```bash
# Check if API key is set
agenta config-show

# Set it via CLI
agenta config-set --api-key your-key

# Or via environment
export AGENTA_API_KEY=your-key
```

### "Connection error" or "API error"

1. Check your internet connection
2. Verify API key is valid
3. Check if API base URL is correct (for custom providers)
4. Ensure you have credits/quota remaining

### Config file location

The config file is stored at: `~/.agenta/config.yaml`

```bash
# View config file location
agenta config-show

# Edit manually if needed
vi ~/.agenta/config.yaml
```

## 📁 Project Structure

```
agenta/
├── src/agenta/
│   ├── __init__.py      # Package info
│   ├── main.py          # Entry point
│   ├── cli.py           # CLI commands (typer)
│   ├── config.py        # Configuration management
│   └── llm_client.py    # LLM API wrapper
├── pyproject.toml       # Package metadata
├── requirements.txt     # Dependencies
└── test_acceptance.py   # Acceptance tests
```

## 🔜 Next Steps (Phase 1+)

Phase 0 establishes the foundation. Future phases will add:

- **Phase 1**: Slash commands (`/test`, `/explain`, `/browse`)
- **Phase 2**: Human-in-the-loop confirmation for file modifications
- **Phase 3**: Sandbox execution with Docker
- **Phase 4**: Web UI with Streamlit

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines (to be created).

## 📜 License

MIT © 2026 Agenta Contributors

---

**🎉 Congratulations!** You now have a working CLI agent that can:
- Accept natural language questions
- Call LLM APIs with streaming
- Manage configuration securely
- Handle errors gracefully

Try it out: `agenta ask "Tell me a joke about programming!"`
