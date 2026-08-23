import os
import sys
import subprocess
import time
import requests
import logging

from desktop.config import desktop_settings, DeploymentProfile

logging.basicConfig(level=logging.INFO, format="%(asctime)s [PILOT DESKTOP] %(message)s")
logger = logging.getLogger("desktop_runner")


def start_backend_service():
    """Starts the embedded backend service on localhost without exposing DB credentials."""
    logger.info(f"Starting Aram Pilot Backend Service (Profile: {desktop_settings.PROFILE.value})...")

    env = os.environ.copy()
    env["DATABASE_URL"] = desktop_settings.HIDDEN_DB_URL
    env["SECRET_KEY"] = desktop_settings.SECRET_KEY
    env["PYTHONPATH"] = "."

    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "backend.app.main:app",
        "--host",
        desktop_settings.BACKEND_HOST,
        "--port",
        str(desktop_settings.BACKEND_PORT),
    ]

    process = subprocess.Popen(cmd, env=env)
    return process


def check_backend_health():
    """Checks if the backend service health endpoint is active."""
    url = f"http://{desktop_settings.BACKEND_HOST}:{desktop_settings.BACKEND_PORT}/api/v1/health"
    for _ in range(10):
        try:
            res = requests.get(url, timeout=2)
            if res.status_code == 200:
                logger.info("Backend service health check PASSED.")
                return True
        except Exception:
            pass
        time.sleep(1)
    logger.error("Backend service health check FAILED.")
    return False


def main():
    logger.info(f"Initializing {desktop_settings.APP_NAME} (v{desktop_settings.VERSION})")
    backend_proc = start_backend_service()

    if not check_backend_health():
        logger.error("Failed to initialize desktop application backend.")
        backend_proc.terminate()
        sys.exit(1)

    logger.info(f"Aram Accountant Pilot is running successfully. Desktop UI available at: http://{desktop_settings.BACKEND_HOST}:{desktop_settings.BACKEND_PORT}/")
    try:
        backend_proc.wait()
    except KeyboardInterrupt:
        logger.info("Stopping Pilot Desktop Application...")
        backend_proc.terminate()


if __name__ == "__main__":
    main()
