from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Project root and app directory paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APP_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(str(APP_DIR / ".env"), str(BASE_DIR / ".env")),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    ENVIRONMENT: str = "development"
    CORS_ORIGINS: Union[str, List[str]] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    GROQ_API_KEY: str = ""
    GROK_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    GROQ_TUTOR_MODEL: str = "qwen/qwen3.8-27b"
    GROQ_QUIZ_MODEL: str = "qwen/qwen3.8-27b"
    GEMINI_MODEL: str = "gemini-1.5-flash"
    RATE_LIMIT_PER_MINUTE: int = 20
    MAX_QUESTION_CHARS: int = 500
    DATABASE_URL: str = "sqlite:///./prismed.db"

    @property
    def active_groq_key(self) -> str:
        return self.GROQ_API_KEY or self.GROK_API_KEY

    @property
    def cors_origins_list(self) -> List[str]:
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        if isinstance(self.CORS_ORIGINS, str):
            # Parse comma-separated origins
            return [orig.strip() for orig in self.CORS_ORIGINS.split(",") if orig.strip()]
        return ["http://localhost:5173"]

settings = Settings()
