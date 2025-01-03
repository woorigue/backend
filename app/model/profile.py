from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, select
from sqlalchemy.orm import Session, relationship

from app.core.utils import get_position_type
from app.db.session import Base


class Profile(Base):
    __tablename__ = "profile"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    nickname = Column(String(24), comment="닉네임")
    gender = Column(String(12), comment="성별", nullable=True)
    location = Column(String(24), comment="활동 장소", nullable=True)
    age = Column(DateTime, comment="생년월일", nullable=True)
    foot = Column(String(12), comment="주발", nullable=True)
    level = Column(Integer, comment="레벨", nullable=True)
    positions = Column(get_position_type(), nullable=True, comment="포지션")
    img = Column(String(256), nullable=True, comment="프로필 이미지 URL")
    user_seq = Column(Integer, ForeignKey("users.seq", ondelete="CASCADE"))

    user = relationship("User", back_populates="profile")
    join_position = relationship(
        "JoinPosition", back_populates="profile", cascade="all, delete-orphan"
    )

    @staticmethod
    def create(db: Session, nickname: str, user_seq: int) -> None:

        profile = db.scalar(select(Profile).where(Profile.user_seq == user_seq))
        profile = Profile(nickname=nickname, user_seq=user_seq)
        db.add(profile)
        db.commit()

        return profile
