import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.seed import seed_data
from api.dependencies.database import SessionLocal, Base, engine

@pytest.fixture(autouse=True, scope="function")
def reset_and_seed_db():
    """
    Drops & recreates all tables, then seeds them before each test.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

    yield


@pytest.fixture(scope="function")
def client():
    """
    Provides a TestClient connected to the freshly‐seeded DB.
    """
    return TestClient(app)