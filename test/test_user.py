from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.mockings import UserMocking


def test_user_login(test_db_session: Session, test_app: TestClient) -> None:
    user_mocking = UserMocking()
    user_mocking.create_user("test")
    user = user_mocking.user
    print(user.__dict__)

    data = {"email": user.email, "password": "test"}
    response = test_app.post("/user/email/login", json=data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_update_user_profile(
    test_db_session: Session, test_app: TestClient, auth_user_mocking: UserMocking
) -> None:
    response = test_app.get("/user/me")
    print(response.json())
