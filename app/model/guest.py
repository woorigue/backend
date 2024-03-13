from sqlalchemy import ARRAY, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base

from dataclasses import dataclass

from app.helper.exception import RegisterException


class Guest(Base):
    __tablename__ = "guest"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    date = Column(DateTime, nullable=False, comment="게시일")
    user_seq = Column(Integer, nullable=False, comment="작성자 유저 시퀀스")
    club_seq = Column(Integer, nullable=False, comment="클럽 시퀀스")
    match_seq = Column(Integer, nullable=False, comment="매치 시퀀스")
    position = Column(ARRAY(Integer), comment="포지션")
    skill = Column(String(24), nullable=False, comment="레벨")
    guest_number = Column(Integer, nullable=False, comment="모집인원")
    match_fee = Column(Integer, comment="매치비용")
    status = Column(String(24), nullable=False, comment="용병상태")
    notice = Column(String(255), nullable=False, comment="공지사항")

    join_guest = relationship(
        "JoinGuest",
        back_populates="guest",
        cascade="all, delete-orphan",
    )


class JoinGuest(Base):
    __tablename__ = "join_guest"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    guest_seq = Column(Integer, ForeignKey("guest.seq", ondelete="CASCADE"))
    user_seq = Column(Integer, ForeignKey("users.seq", ondelete="CASCADE"))
    accepted = Column(Boolean, comment="수락 여부")

    guest = relationship("Guest", back_populates="join_guest")
    user = relationship("User", back_populates="join_guest")
