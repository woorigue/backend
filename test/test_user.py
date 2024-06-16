from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.mockings import UserMocking


def test_user_login(test_db_session: Session, test_app: TestClient):
    user_mocking = UserMocking()
    test_db_session.add(user_mocking.user)
    test_db_session.commit()

    data = {"email": user_mocking.user.email, "password": "test"}
    response = test_app.post("/user/email/login", json=data)

    assert response.status_code, 200
