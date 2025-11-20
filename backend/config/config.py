from functools import lru_cache
from typing import List
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
        sets up the basic settings, defaulting to dev since I don't have time to set this up for prod.
        defaults are the same as the provided env, but a staging or prod env would override them.
    """

    ENV: str = "dev"
    DEBUG: bool = True
    API_PREFIX: str = "/api"
    
    # localhost
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # db
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/d33tcode"

    # auth
    JWT_SECRET: SecretStr = SecretStr("dev-secret")
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRES_MIN: int = 60

    config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        case_sensitive=False,
        extra="ignore",
    )


# basically creates a singleton of the settings for this instance of the app
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
