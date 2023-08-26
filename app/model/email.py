from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.db.session import Base


class Email(Base):
    __tablename__ = "email"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    email = Column(String(128), comment="이메일")
    is_verified = Column(Boolean, default=False, comment="인증 여부")
    expired_at = Column(DateTime, server_default=func.now(), comment="만료 시간")

    @staticmethod
    def create(db: Session, email: str) -> None:
        email = Email(email=email, expired_at=datetime.now() + timedelta(minutes=3))
        db.add(email)
        db.commit()
        return None
