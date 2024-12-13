import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.app import app as fastapi_app
from app.core.config import settings
from app.core.mockings import UserFactory, UserMocking
from app.db.session import Base

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def test_db_session() -> None:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="session")
def test_app() -> TestClient:
    return TestClient(app=fastapi_app)


@pytest.fixture(scope="function", autouse=True)
def set_factory_session(test_db_session) -> None:
    factory_list = [UserFactory]
    for item in factory_list:
        item._meta.sqlalchemy_session = test_db_session


@pytest.fixture(scope="function")
def user_mocking() -> UserMocking:
    user_mocking = UserMocking()
    user_mocking.create_user("test")
    return user_mocking


@pytest.fixture(scope="function")
def auth_user_mocking(user_mocking) -> UserMocking:
    user_mocking.force_authenticate()
    return user_mocking
