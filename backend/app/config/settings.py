"""
Configuration de l'application
Variables d'environnement et settings globaux
"""

from pathlib import Path
from typing import List, Union, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, Field


def parse_cors(v: Any) -> List[str]:
    """Parse CORS origins from various formats"""
    if isinstance(v, list):
        return v
    if isinstance(v, str):
        # Handle JSON array format
        if v.startswith('['):
            import json
            return json.loads(v)
        # Handle comma-separated format
        return [origin.strip() for origin in v.split(',') if origin.strip()]
    return []


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "AdsPilot"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # API
    API_PREFIX: str = "/api"

    # CORS - Use Field with default_factory to avoid JSON parsing
    CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:4200",
            "http://localhost:4201",
            "http://localhost:4300",
            "http://localhost:5000",
            "http://localhost:3000",
            "http://127.0.0.1:4200",
        ]
    )

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Google Ads API
    GOOGLE_ADS_API_VERSION: str = "v16"

    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent.parent
    CREDENTIALS_DIR: Path = BASE_DIR / ".credentials"
    CACHE_DIR: Path = BASE_DIR / ".cache"
    DATA_DIR: Path = BASE_DIR / "data"

    # Cache
    CACHE_TTL: int = 3600  # 1 hour

    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v: Any) -> List[str]:
        return parse_cors(v)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore',
        # Don't parse env vars as JSON by default
        env_parse_none_str=None,
    )


settings = Settings()

# Create directories if they don't exist
settings.CREDENTIALS_DIR.mkdir(exist_ok=True)
settings.CACHE_DIR.mkdir(exist_ok=True)
settings.DATA_DIR.mkdir(exist_ok=True)
