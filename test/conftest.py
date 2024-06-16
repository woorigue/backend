import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.app import app as fastapi_app
from app.core.config import settings
from app.core.mockings import UserFactory
from app.db.session import Base

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="session")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def test_db_session(setup_database):
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def test_app() -> TestClient:
    return TestClient(app=fastapi_app)


@pytest.fixture(scope="function", autouse=True)
def set_factory_session(test_db_session):
    factory_list = [UserFactory]
    for item in factory_list:
        item._meta.sqlalchemy_session = test_db_session
