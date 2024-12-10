import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.app import app as fastapi_app
from app.core.config import settings
from app.core.mockings import UserFactory, UserManager
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


@pytest.fixture(scope="session")
def test_app() -> TestClient:
    return TestClient(app=fastapi_app)


@pytest.fixture(scope="function", autouse=True)
def set_factory_session(test_db_session):
    factory_list = [UserFactory]
    for item in factory_list:
        item._meta.sqlalchemy_session = test_db_session


@pytest.fixture(scope="session", autouse=True)
def configure_user_factory(test_db_session):
    UserFactory._meta.sqlalchemy_session = test_db_session


@pytest.fixture(scope="session")
def setup_users(test_db_session, test_app):
    users = {}

    def generate_token(email, password):
        login_response = test_app.post(
            "/user/email/login", json={"email": email, "password": password}
        )
        assert login_response.status_code == 200
        return login_response.json()["access_token"]

    user1 = UserManager.create_user(test_db_session, "user1@example.com", "test")
    user2 = UserManager.create_user(test_db_session, "user2@example.com", "test")

    users["user1"] = {
        "user": user1,
        "token": generate_token("user1@example.com", "test"),
    }
    users["user2"] = {
        "user": user2,
        "token": generate_token("user2@example.com", "test"),
    }

    return users
