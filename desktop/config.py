import os
from enum import Enum
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class DeploymentProfile(str, Enum):
    DEVELOPMENT = "development"
    PILOT = "pilot"
    PRODUCTION = "production"


class DesktopSettings(BaseSettings):
    PROFILE: DeploymentProfile = DeploymentProfile.PILOT
    APP_NAME: str = "Aram Accountant Pilot Desktop"
    VERSION: str = "0.1.0-pilot"

    # Internal backend API host for desktop wrapper communication
    BACKEND_HOST: str = "127.0.0.1"
    BACKEND_PORT: int = 8000

    # Hidden DB configuration - NEVER exposed to the desktop UI client
    # In pilot mode, uses an isolated local SQLite database embedded with the backend service
    HIDDEN_DB_URL: str = "sqlite:///./aram_pilot_hidden.db"
    SECRET_KEY: str = "PILOT_HIDDEN_SECRET_KEY_NEVER_EXPOSE_TO_UI"

    model_config = ConfigDict(case_sensitive=True)


desktop_settings = DesktopSettings()
