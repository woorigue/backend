from sqlalchemy.orm import Session

from app.model.email import Email
from app.rest_api.schema.email import EmailVerifySchema


class EmailController:
    def send_verify_code(self, db: Session, user_data: EmailVerifySchema) -> None:
        Email.create(db, email=user_data.email)


email_controller = EmailController()
