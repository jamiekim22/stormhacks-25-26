import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings and configuration."""
    
    # Snowflake Database Settings
    SNOWFLAKE_ACCOUNT: str = os.getenv("SNOWFLAKE_ACCOUNT", "")
    SNOWFLAKE_USER: str = os.getenv("SNOWFLAKE_USER", "")
    SNOWFLAKE_PASSWORD: str = os.getenv("SNOWFLAKE_PASSWORD", "")
    SNOWFLAKE_WAREHOUSE: str = os.getenv("SNOWFLAKE_WAREHOUSE", "")
    SNOWFLAKE_DATABASE: str = os.getenv("SNOWFLAKE_DATABASE", "")
    SNOWFLAKE_SCHEMA: str = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
    
    # API Settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_RELOAD: bool = os.getenv("API_RELOAD", "false").lower() == "true"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    
    # Speech Pipeline Settings
    SPEECH_PIPELINE_PATH: str = os.getenv("SPEECH_PIPELINE_PATH", "../Speech to Speech")
    MAX_CALL_DURATION: int = int(os.getenv("MAX_CALL_DURATION", "300"))
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "en-US")
    
    # Logging Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Call Service Settings
    MAX_CONCURRENT_CALLS: int = int(os.getenv("MAX_CONCURRENT_CALLS", "5"))
    CALL_HISTORY_RETENTION_HOURS: int = int(os.getenv("CALL_HISTORY_RETENTION_HOURS", "24"))
    CLEANUP_INTERVAL_MINUTES: int = int(os.getenv("CLEANUP_INTERVAL_MINUTES", "60"))
    
    # Development Settings
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    ENABLE_DOCS: bool = os.getenv("ENABLE_DOCS", "true").lower() == "true"
    
    @classmethod
    def validate(cls) -> List[str]:
        """Validate required settings and return list of missing values."""
        required_settings = [
            ("SNOWFLAKE_ACCOUNT", cls.SNOWFLAKE_ACCOUNT),
            ("SNOWFLAKE_USER", cls.SNOWFLAKE_USER),
            ("SNOWFLAKE_PASSWORD", cls.SNOWFLAKE_PASSWORD),
            ("SNOWFLAKE_DATABASE", cls.SNOWFLAKE_DATABASE),
        ]
        
        missing = []
        for setting_name, value in required_settings:
            if not value:
                missing.append(setting_name)
        
        return missing

# Global settings instance
settings = Settings()