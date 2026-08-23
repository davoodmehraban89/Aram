import os
import pytest
from desktop.config import DesktopSettings, DeploymentProfile


def test_desktop_settings_default_profile():
    settings = DesktopSettings()
    assert settings.PROFILE == DeploymentProfile.PILOT
    assert settings.BACKEND_HOST == "127.0.0.1"
    assert settings.BACKEND_PORT == 8000


def test_desktop_settings_environment_override(monkeypatch):
    monkeypatch.setenv("PROFILE", "production")
    monkeypatch.setenv("BACKEND_PORT", "9000")

    settings = DesktopSettings()
    assert settings.PROFILE == DeploymentProfile.PRODUCTION
    assert settings.BACKEND_PORT == 9000


def test_hidden_db_credentials_protection():
    settings = DesktopSettings()
    # Ensure hidden DB URL is configured for internal service and not exposed to UI
    assert settings.HIDDEN_DB_URL is not None
    assert "sqlite:///" in settings.HIDDEN_DB_URL
    assert settings.SECRET_KEY is not None


def test_pilot_mode_validation():
    settings = DesktopSettings(PROFILE=DeploymentProfile.PILOT)
    assert settings.PROFILE.value == "pilot"
    assert "Pilot" in settings.APP_NAME


def test_development_profile_validation():
    settings = DesktopSettings(PROFILE=DeploymentProfile.DEVELOPMENT)
    assert settings.PROFILE.value == "development"


def test_production_profile_validation():
    settings = DesktopSettings(PROFILE=DeploymentProfile.PRODUCTION)
    assert settings.PROFILE.value == "production"
