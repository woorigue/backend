from sqlalchemy import Boolean, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base


class Poll(Base):
    __tablename__ = "poll"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    expired_at = Column(DateTime, comment="투표 종료 시간")
    vote_closed = Column(Boolean, default=False, comment="투표 종료 여부")
    created_at = Column(DateTime, default=datetime.utcnow, comment="생성 시간")
    updated_at = Column(DateTime, default=datetime.utcnow, comment="수정 시간")

    # FK
    match_seq = Column(Integer, ForeignKey("match.seq"))
    user_seq = Column(Integer, ForeignKey("users.seq"))

    # relation
    user = relationship("User", back_populates="poll")
    match = relationship("Match", back_populates="poll")
    join_poll = relationship("JoinPoll", back_populates="poll")


class JoinPoll(Base):
    __tablename__ = "join_poll"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    attend = Column(Boolean, comment="참석 여부")
    created_at = Column(DateTime, default=datetime.utcnow, comment="생성 시간")

    # FK
    user_seq = Column(Integer, ForeignKey("users.seq"))
    poll_seq = Column(Integer, ForeignKey("poll.seq"))

    # relation
    poll = relationship("Poll", back_populates="join_poll")
    user = relationship("User", back_populates="join_poll")
