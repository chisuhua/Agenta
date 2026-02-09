"""CLI commands using typer"""

import sys
import typer
from rich.console import Console
from rich.markdown import Markdown
from typing import Optional

from .config import Config
from .llm_client import LLMClient

app = typer.Typer(
    name="agenta",
    help="🧠 Agenta — Your Local AI Agent for Developers",
    add_completion=False
)

console = Console()


@app.command()
def ask(
    question: str = typer.Argument(..., help="Question to ask the AI agent"),
    no_stream: bool = typer.Option(False, "--no-stream", help="Disable streaming output")
):
    """
    Ask the AI agent a question and get a response.
    
    Example: agenta ask "What is 2+2?"
    """
    config = Config()
    
    # Check if API key is configured
    api_key = config.api_key
    if not api_key:
        console.print("❌ [bold red]Error: API key not configured[/bold red]")
        console.print("\nPlease configure your API key using one of these methods:")
        console.print("1. Set environment variable: export AGENTA_API_KEY=your-key")
        console.print("2. Edit config file: ~/.agenta/config.yaml")
        console.print("\nExample config.yaml:")
        console.print("```yaml")
        console.print("api_key: sk-your-api-key-here")
        console.print("model: gpt-3.5-turbo")
        console.print("provider: openai")
        console.print("```")
        raise typer.Exit(code=1)
    
    try:
        # Initialize LLM client
        llm = LLMClient(
            api_key=api_key,
            model=config.model,
            api_base=config.api_base,
            provider=config.provider
        )
        
        console.print(f"[dim]💭 Thinking...[/dim]\n")
        
        if no_stream:
            # Non-streaming response
            response = llm.ask_non_streaming(question)
            console.print(response)
        else:
            # Streaming response - print character by character
            for chunk in llm.ask(question, stream=True):
                console.print(chunk, end="")
                sys.stdout.flush()
            console.print()  # New line at the end
        
    except ValueError as e:
        console.print(f"❌ [bold red]Configuration Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"❌ [bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


@app.command()
def config_set(
    api_key: Optional[str] = typer.Option(None, "--api-key", help="API key for LLM provider"),
    model: Optional[str] = typer.Option(None, "--model", help="Model name (e.g., gpt-4, claude-3)"),
    provider: Optional[str] = typer.Option(None, "--provider", help="Provider (openai, anthropic, dashscope)"),
    api_base: Optional[str] = typer.Option(None, "--api-base", help="Custom API base URL")
):
    """
    Configure Agenta settings.
    
    Example: agenta config-set --api-key sk-xxx --model gpt-4
    """
    config = Config()
    
    updated = False
    if api_key:
        config.set("api_key", api_key)
        console.print(f"✅ API key updated")
        updated = True
    
    if model:
        config.set("model", model)
        console.print(f"✅ Model set to: {model}")
        updated = True
    
    if provider:
        config.set("provider", provider)
        console.print(f"✅ Provider set to: {provider}")
        updated = True
    
    if api_base:
        config.set("api_base", api_base)
        console.print(f"✅ API base URL set to: {api_base}")
        updated = True
    
    if not updated:
        console.print("No configuration changes specified. Use --help to see available options.")
    else:
        console.print(f"\n📝 Config file: {config.config_file}")


@app.command()
def config_show():
    """
    Show current configuration.
    """
    config = Config()
    current = config.load()
    
    console.print("[bold]Current Configuration:[/bold]\n")
    
    # Mask API key for security
    api_key = current.get("api_key", "")
    if api_key:
        masked_key = api_key[:8] + "..." if len(api_key) > 8 else "***"
    else:
        masked_key = "[red]Not set[/red]"
    
    console.print(f"API Key: {masked_key}")
    console.print(f"Model: {current.get('model', 'gpt-3.5-turbo')}")
    console.print(f"Provider: {current.get('provider', 'openai')}")
    console.print(f"API Base: {current.get('api_base', 'default')}")
    console.print(f"\n📝 Config file: {config.config_file}")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="Show version")
):
    """
    🧠 Agenta — Your Local AI Agent for Developers
    
    Automate repetitive coding tasks. Run locally. Stay in control.
    """
    if version:
        from . import __version__
        console.print(f"Agenta version {__version__}")
        raise typer.Exit()
    
    if ctx.invoked_subcommand is None:
        console.print("👋 Welcome to Agenta!")
        console.print("\nUse 'agenta --help' to see available commands.")
        console.print("\nQuick start:")
        console.print("  1. Configure: agenta config-set --api-key your-key")
        console.print("  2. Ask: agenta ask 'What is 2+2?'")


if __name__ == "__main__":
    app()
