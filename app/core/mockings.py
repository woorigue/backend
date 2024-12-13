from factory.alchemy import SQLAlchemyModelFactory

from app.app import app as fastapi_app
from app.core.token import get_current_user
from app.model.user import User, pwd_context


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User

    email = "tpdnrqkh@naver.com"


class UserMocking:
    def __init__(self):
        self.user = None

    def create_user(self, password: str = "test"):
        self.user = UserFactory.create(password=pwd_context.hash(password))

    def force_authenticate(self):
        async def override_get_current_user():
            return self.user

        fastapi_app.dependency_overrides[get_current_user] = override_get_current_user
