from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from app.model.email import Email
from app.model.user import User
from app.rest_api.schema.email import (
    EmailAuthCodeSchema,
    EmailPasswordResetSchema,
    EmailVerifySchema,
)
from app.helper.exception import (
    EmailConflictException,
    EmailExpiredException,
    EmailAuthNumberInvalidException,
)

from app.helper.exception import UserNotFoundException
from app.utils.email_form import verify_email_form, sign_up_form


class EmailController:
    def send_verify_code_for_reset_password(
        self, db: Session, user_data: EmailPasswordResetSchema
    ) -> None:
        user = db.scalar(select(User).where(User.email == user_data.email))

        if not user:
            raise UserNotFoundException

        email = Email.create(db, email=user_data.email)
        client = boto3.client("ses", region_name="ap-northeast-2")

        to_email = user_data.email
        auth_number = email.auth_number
        data = verify_email_form(auth_number)
        sender = "woorigue@gmail.com"
        try:
            response = client.send_email(
                Destination={
                    "ToAddresses": [
                        to_email,
                    ],
                },
                Message={
                    "Body": {
                        "Html": {
                            "Charset": "UTF-8",
                            "Data": data,
                        },
                    },
                    "Subject": {
                        "Charset": "UTF-8",
                        "Data": "[우리들만의리그] 패스워드 초기화",
                    },
                },
                Source=sender,
            )
        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            print("Email sent! Message ID:"),
            print(response["MessageId"])

    def send_verify_code(self, db: Session, user_data: EmailVerifySchema) -> None:
        user = db.scalar(select(User).where(User.email == user_data.email))

        if user:
            raise EmailConflictException

        # TODO: Create function of ses

        email = Email.create(db, email=user_data.email)
        client = boto3.client("ses", region_name="ap-northeast-2")

        to_email = user_data.email
        auth_number = email.auth_number
        sender = "woorigue@gmail.com"
        data = sign_up_form(auth_number)
        try:
            response = client.send_email(
                Destination={
                    "ToAddresses": [
                        to_email,
                    ],
                },
                Message={
                    "Body": {
                        "Html": {
                            "Charset": "UTF-8",
                            "Data": data,
                        },
                    },
                    "Subject": {
                        "Charset": "UTF-8",
                        "Data": "[우리들만의리그] 이메일 인증",
                    },
                },
                Source=sender,
            )
        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            print("Email sent! Message ID:"),
            print(response["MessageId"])

    def verify_auth_code(self, db: Session, user_data: EmailAuthCodeSchema) -> None:
        email_list = db.scalars(
            select(Email)
            .where(
                Email.email == user_data.email,
                Email.is_verified == False,
            )
            .order_by(desc("seq"))
        ).all()

        email = email_list[0]

        if email:
            if email.auth_number != user_data.auth_number:
                raise EmailAuthNumberInvalidException

        if not email or datetime.now() > email.expired_at:
            raise EmailExpiredException

        db.query(Email).filter(Email.seq == email.seq).update({"is_verified": True})
        db.commit()
        db.flush()


email_controller = EmailController()
