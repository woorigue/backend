from datetime import datetime, timedelta
from random import randrange

from fastapi import HTTPException, status
from sqlalchemy import Boolean, Column, DateTime, Integer, SmallInteger, String
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.db.session import Base


class Email(Base):
    __tablename__ = "email"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    email = Column(String(128), comment="이메일")
    auth_number = Column(String(6), comment="인증번호")
    is_verified = Column(Boolean, default=False, comment="인증 여부")
    expired_at = Column(DateTime, server_default=func.now(), comment="만료 시간")

    @staticmethod
    def create(db: Session, email: str) -> None:
        auth_number = randrange(10000, 99999)
        email = Email(
            email=email,
            expired_at=datetime.now() + timedelta(minutes=3),
            auth_number=auth_number,
        )
        db.add(email)
        db.commit()
        return email
