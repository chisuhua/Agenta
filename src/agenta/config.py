"""Configuration management for Agenta"""

import os
from pathlib import Path
from typing import Optional
import yaml


class Config:
    """Configuration manager for Agenta"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".agenta"
        self.config_file = self.config_dir / "config.yaml"
        self._config = None
    
    def ensure_config_dir(self):
        """Create config directory if it doesn't exist"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def load(self) -> dict:
        """Load configuration from file"""
        if self._config is not None:
            return self._config
            
        self.ensure_config_dir()
        
        if not self.config_file.exists():
            # Create default config
            default_config = {
                "api_key": "",
                "model": "gpt-3.5-turbo",
                "api_base": "",
                "provider": "openai"  # openai, anthropic, dashscope
            }
            self.save(default_config)
            return default_config
        
        with open(self.config_file, 'r') as f:
            self._config = yaml.safe_load(f) or {}
        
        return self._config
    
    def save(self, config: dict):
        """Save configuration to file"""
        self.ensure_config_dir()
        with open(self.config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        self._config = config
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        config = self.load()
        return config.get(key, default)
    
    def set(self, key: str, value):
        """Set configuration value"""
        config = self.load()
        config[key] = value
        self.save(config)
    
    @property
    def api_key(self) -> Optional[str]:
        """Get API key from config or environment"""
        # Check environment variables first
        env_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("AGENTA_API_KEY")
        if env_key:
            return env_key
        
        # Then check config file
        key = self.get("api_key")
        return key if key else None
    
    @property
    def model(self) -> str:
        """Get model name"""
        return self.get("model", "gpt-3.5-turbo")
    
    @property
    def api_base(self) -> Optional[str]:
        """Get API base URL"""
        base = self.get("api_base")
        return base if base else None
    
    @property
    def provider(self) -> str:
        """Get provider name"""
        return self.get("provider", "openai")
