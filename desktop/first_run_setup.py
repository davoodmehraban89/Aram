import os
import sys
import logging
from sqlalchemy.orm import Session

from backend.app.database import engine, Base, SessionLocal
from backend.app.models.entities import User, UserRole
from backend.app.api.auth import hash_password

logging.basicConfig(level=logging.INFO, format="%(asctime)s [FIRST RUN] %(message)s")
logger = logging.getLogger("first_run_setup")


def initialize_first_run_setup(db_session: Session = None):
    """
    Executes first-run initialization for clean Windows environment assumptions:
    1. Creates database schema tables.
    2. Validates database connection.
    3. Seeds initial Administrator account if no users exist.
    """
    logger.info("Initializing first-run environment setup...")

    Base.metadata.create_all(bind=engine)
    logger.info("Database schema initialized successfully.")

    db: Session = db_session if db_session else SessionLocal()
    try:
        user_count = db.query(User).count()
        if user_count == 0:
            logger.info("No users found in database. Creating initial administrator account...")
            admin_user = User(
                username="admin_user",
                hashed_password=hash_password("admin_pass"),
                role=UserRole.ADMIN,
                is_active=True,
            )
            db.add(admin_user)
            db.commit()
            logger.info("Initial administrator account ('admin_user') created successfully.")
        else:
            logger.info(f"Database contains {user_count} existing user(s). Skipping user seeding.")
    finally:
        if not db_session:
            db.close()


if __name__ == "__main__":
    initialize_first_run_setup()
