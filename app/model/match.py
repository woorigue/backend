from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import Session

from app.db.session import Base

from dataclasses import dataclass

from app.helper.exception import RegisterException
from sqlalchemy.orm import Session, relationship
from app.rest_api.schema.match.match import MatchRegisterSchema

from app.helper.exception import RegisterException


class Match(Base):
    __tablename__ = "match"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    match_type = Column(String(24), nullable=False, comment="매치유형")
    location = Column(String(128), nullable=False, comment="매치장소")
    match_time = Column(DateTime, nullable=False, comment="매치일정")
    skill = Column(String(24), nullable=False, comment="레벨")
    team_size = Column(Integer, nullable=False, comment="매치인원")
    gender = Column(String(12), nullable=False, comment="성별")
    match_fee = Column(Integer, nullable=True, comment="매치비용")
    notice = Column(String(255), nullable=True, comment="공지사항")
    status = Column(String(24), nullable=False, comment="매치상태")
    guests = Column(Integer, nullable=False, comment="용병id")
    club_seq = Column(Integer, nullable=False, comment="클럽id")

    poll = relationship("Poll", back_populates="match")
