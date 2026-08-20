import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from aram_backend.database import Base, build_engine
from aram_backend.main import app


@pytest.fixture
def session(tmp_path) -> Session:
    engine = build_engine(f"sqlite:///{tmp_path / 'test.db'}")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    with factory() as db:
        yield db
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

