from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Aram API"
    environment: str = "development"
    database_url: str = "sqlite:///./aram.db"
    model_config = SettingsConfigDict(env_prefix="ARAM_", env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()

