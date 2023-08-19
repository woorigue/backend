from sqlalchemy.orm import Session

from app.model.user import User
from app.rest_api.schema.user import EmailRegisterSchema


class UserController:
    def email_register_user(self, db: Session, user_data: EmailRegisterSchema) -> None:
        User.create(db, email=user_data.email, password=user_data.password)


user_controller = UserController()
