from backend.app.database import engine, Base
from backend.app.models import *  # ensure all models are registered

def init_db():
    """Initializes database schema by creating all tables."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database tables initialized successfully.")
