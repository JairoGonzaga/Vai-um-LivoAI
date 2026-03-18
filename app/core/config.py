from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pydantic import field_validator
import json


class Settings(BaseSettings):
    DATABASE_URL: str

    SUPABASE_URL:         str
    SUPABASE_ANON_KEY:    str
    SUPABASE_SERVICE_KEY: str
    STORAGE_BUCKET:       str = "Pratileiras"
    STORAGE_BUCKET_FOTOS: str = "Pratileiras"

    HF_SPACE_URL: str
    HF_TOKEN:     str

    GOOGLE_BOOKS_API_KEY: str
    GOOGLE_VISION_API_KEY: str = ""
    MISTRAL_API_KEY: str = ""

    APP_ENV:    str  = "development"
    APP_NAME:   str  = "LivroAI"
    API_PREFIX: str  = "/api/v1"
    DEBUG:      bool = True
    PORT:       int  = 8000

    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value):
        if isinstance(value, str):
            cleaned = value.strip()
            if not cleaned:
                return []
            if cleaned.startswith("["):
                return json.loads(cleaned)
            return [item.strip() for item in cleaned.split(",") if item.strip()]
        return value

    YOLO_CONFIDENCE_THRESHOLD: float = 0.6

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()