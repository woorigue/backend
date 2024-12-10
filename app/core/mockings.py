from factory.alchemy import SQLAlchemyModelFactory
from factory import Sequence

from app.model.user import User, pwd_context


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = None

    email = Sequence(lambda n: f"user{n}@example.com")
    password = pwd_context.hash("default_password")


class UserManager:
    _users = {}

    @classmethod
    def create_user(cls, test_db_session, email, password="default_password"):
        if email in cls._users:
            return cls._users[email]

        hashed_password = pwd_context.hash(password)
        user = UserFactory.create(email=email, password=hashed_password)

        test_db_session.add(user)
        test_db_session.commit()
        cls._users[email] = user
        return user
