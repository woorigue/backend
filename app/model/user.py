from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import Boolean, CheckConstraint, Column, Integer, String, select
from sqlalchemy.orm import Session

from app.db.session import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    email = Column(String(128), unique=True, comment="이메일")
    password = Column(String(256), comment="비밀번호")
    is_active = Column(Boolean, default=True, comment="활성화 여부")

    @staticmethod
    def create(db: Session, email: str, password: str) -> None:
        user = db.scalar(select(User).where(User.email == email))

        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="email already exists."
            )

        if len(password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password need at least 6 characters",
            )

        user = User(email=email, password=pwd_context.hash(password))
        db.add(user)
        db.commit()
        return None
