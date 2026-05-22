"""
Configuration de l'application
Variables d'environnement et settings globaux
"""

from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "Google Ads Dashboard"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # API
    API_PREFIX: str = "/api"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:4200",
        "http://localhost:3000",
        "http://127.0.0.1:4200",
    ]

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
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Create directories if they don't exist
settings.CREDENTIALS_DIR.mkdir(exist_ok=True)
settings.CACHE_DIR.mkdir(exist_ok=True)
settings.DATA_DIR.mkdir(exist_ok=True)
