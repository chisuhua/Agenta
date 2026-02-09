#!/usr/bin/env python3
"""
Example usage of Agenta CLI programmatically.

This demonstrates how to use Agenta's components as a library.
"""

from agenta.config import Config
from agenta.llm_client import LLMClient
import os


def example_basic_usage():
    """Example: Basic usage with config"""
    print("=" * 70)
    print("Example 1: Basic Usage")
    print("=" * 70)
    
    # Load configuration
    config = Config()
    
    # Check if API key is available
    if not config.api_key:
        print("⚠️  No API key configured.")
        print("Set it with: agenta config-set --api-key your-key")
        return
    
    # Initialize LLM client
    llm = LLMClient(
        api_key=config.api_key,
        model=config.model,
        api_base=config.api_base,
        provider=config.provider
    )
    
    # Ask a question with streaming
    print("\n💭 Asking: 'What is 2+2?'\n")
    for chunk in llm.ask("What is 2+2?", stream=True):
        print(chunk, end="", flush=True)
    print("\n")


def example_custom_model():
    """Example: Using custom model settings"""
    print("\n" + "=" * 70)
    print("Example 2: Custom Model Settings")
    print("=" * 70)
    
    # Get API key from environment or config
    api_key = os.environ.get("AGENTA_API_KEY")
    if not api_key:
        config = Config()
        api_key = config.api_key
    
    if not api_key:
        print("⚠️  No API key available")
        return
    
    # Use specific model
    llm = LLMClient(
        api_key=api_key,
        model="gpt-4",  # Use GPT-4
        provider="openai"
    )
    
    print("\n💭 Using GPT-4: 'Explain quantum computing in one sentence'\n")
    response = llm.ask_non_streaming("Explain quantum computing in one sentence")
    print(response)


def example_error_handling():
    """Example: Error handling"""
    print("\n" + "=" * 70)
    print("Example 3: Error Handling")
    print("=" * 70)
    
    try:
        # Try to create client without API key
        llm = LLMClient(api_key="", model="gpt-3.5-turbo")
    except ValueError as e:
        print(f"✅ Caught expected error: {e}")


def example_config_management():
    """Example: Configuration management"""
    print("\n" + "=" * 70)
    print("Example 4: Configuration Management")
    print("=" * 70)
    
    config = Config()
    
    # Show current settings
    print(f"Current model: {config.model}")
    print(f"Current provider: {config.provider}")
    
    # Update settings
    print("\nUpdating model to gpt-4...")
    config.set("model", "gpt-4")
    
    print(f"New model: {config.model}")
    
    # Reset to default
    print("\nResetting to gpt-3.5-turbo...")
    config.set("model", "gpt-3.5-turbo")
    print(f"Model: {config.model}")


def main():
    """Run all examples"""
    print("\n" + "🧠" * 35)
    print("AGENTA - Usage Examples")
    print("🧠" * 35 + "\n")
    
    # Run examples
    example_basic_usage()
    example_custom_model()
    example_error_handling()
    example_config_management()
    
    print("\n" + "=" * 70)
    print("✅ Examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
