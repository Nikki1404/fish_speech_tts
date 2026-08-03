from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    fish_http_url: str = "http://fish-speech:8080"
    ws_api_key: str = ""
    max_text_length: int = Field(default=8000, ge=1, le=100_000)
    upstream_connect_timeout: float = Field(default=30.0, gt=0)
    upstream_read_timeout: float = Field(default=900.0, gt=0)
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
