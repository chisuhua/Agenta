"""LLM client with streaming support"""

import sys
from typing import Iterator, Optional
from openai import OpenAI


class LLMClient:
    """
    Unified LLM client supporting OpenAI, Claude, and Qwen.
    Uses OpenAI-compatible API for all providers.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", 
                 api_base: Optional[str] = None, provider: str = "openai"):
        """
        Initialize LLM client
        
        Args:
            api_key: API key for the provider
            model: Model name to use
            api_base: Optional custom API base URL
            provider: Provider name (openai, anthropic, dashscope)
        """
        if not api_key:
            raise ValueError("API key is required. Please set it in ~/.agenta/config.yaml or AGENTA_API_KEY environment variable")
        
        self.api_key = api_key
        self.model = model
        self.provider = provider
        
        # Initialize OpenAI client (works with compatible APIs)
        client_kwargs = {"api_key": api_key}
        if api_base:
            client_kwargs["base_url"] = api_base
        
        self.client = OpenAI(**client_kwargs)
    
    def ask(self, prompt: str, stream: bool = True) -> Iterator[str]:
        """
        Send a question to the LLM and get response
        
        Args:
            prompt: The question or prompt to send
            stream: Whether to stream the response
            
        Yields:
            Chunks of text as they arrive (if stream=True)
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                stream=stream
            )
            
            if stream:
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            else:
                yield response.choices[0].message.content
                
        except Exception as e:
            error_msg = f"Error calling LLM: {str(e)}"
            print(f"\n❌ {error_msg}", file=sys.stderr)
            raise
    
    def ask_non_streaming(self, prompt: str) -> str:
        """
        Send a question and get complete response at once
        
        Args:
            prompt: The question or prompt to send
            
        Returns:
            Complete response text
        """
        chunks = list(self.ask(prompt, stream=False))
        return chunks[0] if chunks else ""
