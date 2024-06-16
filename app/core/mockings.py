from factory.alchemy import SQLAlchemyModelFactory

from app.model.user import User, pwd_context


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User

    email = "tpdnrqkh@naver.com"
    password = pwd_context.hash("test")


class UserMocking:
    def __init__(self):
        self.user = UserFactory.create()
