from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    pg_dsn: str
    