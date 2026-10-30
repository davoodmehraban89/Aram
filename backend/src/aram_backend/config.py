from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Aram API"
    environment: str = "development"
    database_url: str = "sqlite:///./aram.db"
    # UNCONFIGURED BY DEFAULT. Supply a trusted issuer/audience and *public*
    # RSA verification key from a deployed enterprise identity provider.
    # Never put a signing private key into application settings or source.
    auth_issuer: str = ""
    auth_audience: str = ""
    auth_public_key_pem: str = ""
    model_config = SettingsConfigDict(env_prefix="ARAM_", env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()

