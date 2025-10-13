import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration manager for aria"""
    
    # AI Settings
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL: Optional[str] = os.getenv("OPENAI_BASE_URL")
    
    # Default AI provider
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "deepseek")  # deepseek or openai
    
    # Project settings
    PLANS_DIR: str = os.getenv("PLANS_DIR", "./aria/plans")
    LOGS_DIR: str = os.getenv("LOGS_DIR", "./aria/logs")
    
    # AI Behavior
    DEFAULT_TEMPERATURE: float = 0.2
    DEFAULT_MAX_TOKENS: int = 4000
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        if cls.AI_PROVIDER == "deepseek" and not cls.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY is required when using DeepSeek provider")
        if cls.AI_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")
        return True

config = Config()