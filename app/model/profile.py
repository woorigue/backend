from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Profile(Base):
    __tablename__ = "profile"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    nickname = Column(String(24), comment="닉네임")
    positions = Column(ARRAY(Integer), nullable=True, comment="포지션")
    img = Column(String(256), nullable=True, comment="프로필 이미지 URL")
    user_seq = Column(Integer, ForeignKey("users.seq"))

    user = relationship("User", back_populates="profile")
    join_profile = relationship("JoinPosition", back_populates="profile")
