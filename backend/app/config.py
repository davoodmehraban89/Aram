import os
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Financial Reporting Platform API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Database settings default to SQLite for local dev
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./financial_platform.db")

    model_config = ConfigDict(case_sensitive=True)

settings = Settings()
