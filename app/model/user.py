from passlib.context import CryptContext
from sqlalchemy import ARRAY, Boolean, Column, Integer, String, select
from sqlalchemy.orm import Session, relationship

from app.db.session import Base

from .email import Email
from .profile import Profile
from .club import JoinClub
from .clubPosting import JoinClubPosting
from .guest import JoinGuest
from .memberPosting import JoinMemberPosting
from .firebase import Firebase
from app.helper.exception import (
    EmailConflictException,
    PasswordInvalidException,
    UserNotFoundException,
)
from app.model.chat import UserChatRoomAssociation


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    email = Column(String(128), unique=True, comment="이메일")
    password = Column(String(256), comment="비밀번호")
    is_active = Column(Boolean, default=True, comment="활성화 여부")
    clubs = Column(ARRAY(Integer), nullable=True, comment="클럽")

    profile = relationship(Profile, back_populates="user", cascade="all, delete-orphan")
    join_club = relationship(
        JoinClub, back_populates="user", cascade="all, delete-orphan"
    )
    join_club_posting = relationship(
        JoinClubPosting, back_populates="user", cascade="all, delete-orphan"
    )
    join_guest = relationship(
        JoinGuest, back_populates="user", cascade="all, delete-orphan"
    )
    join_member_posting = relationship(
        JoinMemberPosting, back_populates="user", cascade="all, delete-orphan"
    )
    chatting_rooms = relationship(
        "ChattingRoom", secondary=UserChatRoomAssociation, back_populates="users"
    )
    poll = relationship("Poll", back_populates="user")
    join_poll = relationship("JoinPoll", back_populates="user")
    firebase = relationship(
        Firebase, back_populates="user", cascade="all, delete-orphan"
    )

    @staticmethod
    def create(db: Session, email: str, password: str) -> None:
        user = db.scalar(select(User).where(User.email == email))  # ORM

        if user:
            raise EmailConflictException

        if len(password) < 6:
            raise PasswordInvalidException

        user = User(email=email, password=pwd_context.hash(password))
        db.add(user)
        db.commit()
        return user

    @staticmethod
    def resset_password(db: Session, email: str, password: str):
        user = db.scalar(select(User).where(User.email == email))

        if not user:
            raise UserNotFoundException

        db.query(User).filter(User.email == email).update(
            {"password": pwd_context.hash(password)}
        )
        db.commit()
        db.flush()
