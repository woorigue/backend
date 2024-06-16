from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.utils import get_position_type
from app.db.session import Base


class Profile(Base):
    __tablename__ = "profile"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    nickname = Column(String(24), comment="닉네임")
    gender = Column(String(12), comment="성별")
    location = Column(String(24), comment="활동 장소")
    birth_date = Column(DateTime, comment="생년월일")
    foot = Column(String(12), comment="주발")
    level = Column(Integer, comment="레벨")
    positions = Column(get_position_type(), nullable=True, comment="포지션")
    img = Column(String(256), nullable=True, comment="프로필 이미지 URL")
    user_seq = Column(Integer, ForeignKey("users.seq", ondelete="CASCADE"))

    user = relationship("User", back_populates="profile")
    join_position = relationship(
        "JoinPosition", back_populates="profile", cascade="all, delete-orphan"
    )
