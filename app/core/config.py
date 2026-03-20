from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
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
    GOOGLE_VISION_CREDENTIALS: str = ""
    MISTRAL_API_KEY: str = ""

    APP_ENV:    str  = "development"
    APP_NAME:   str  = "LivroAI"
    API_PREFIX: str  = "/api/v1"
    DEBUG:      bool = False
    PORT:       int  = 8000

    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    YOLO_CONFIDENCE_THRESHOLD: float = 0.6

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def allowed_origins_list(self) -> list[str]:
        value = (self.ALLOWED_ORIGINS or "").strip()
        if not value:
            return []

        if value.startswith("["):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return [str(item).strip() for item in parsed if str(item).strip()]
            except json.JSONDecodeError:
                pass

        return [item.strip() for item in value.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()