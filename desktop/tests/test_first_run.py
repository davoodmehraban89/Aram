import os
import pytest
from backend.app.models import User, UserRole
from desktop.config import DesktopSettings, DeploymentProfile
from desktop.first_run_setup import initialize_first_run_setup


def test_first_run_setup_creates_schema_and_admin(db_session):
    # Execute first run setup with test db_session
    initialize_first_run_setup(db_session=db_session)

    # Query for created admin user
    admin = db_session.query(User).filter_by(username="admin_user").first()
    assert admin is not None
    assert admin.role == UserRole.ADMIN
    assert admin.is_active is True


def test_first_run_setup_idempotency(db_session):
    # Running first run setup twice should not raise errors or create duplicate users
    initialize_first_run_setup(db_session=db_session)
    initialize_first_run_setup(db_session=db_session)

    admins = db_session.query(User).filter_by(username="admin_user").all()
    assert len(admins) == 1


def test_spec_file_exists():
    spec_path = "desktop/aram_pilot.spec"
    assert os.path.exists(spec_path)
    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Aram_Accountant_Pilot" in content
    assert "app_runner.py" in content


def test_first_run_health_check_configuration():
    settings = DesktopSettings()
    assert settings.PROFILE == DeploymentProfile.PILOT
    assert settings.BACKEND_HOST == "127.0.0.1"
    assert settings.BACKEND_PORT == 8000
