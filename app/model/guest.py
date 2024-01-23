from sqlalchemy import ARRAY, Column, String, Integer, DateTime
from sqlalchemy.orm import Session

from app.db.session import Base

from dataclasses import dataclass

from app.helper.exception import RegisterException


class Guest(Base):
    __tablename__ = "guest"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    club = Column(Integer, nullable=False, comment="클럽id")
    match = Column(Integer, nullable=False, comment="매치id")
    position = Column(ARRAY(Integer), comment="포지션")
    skill = Column(String(24), nullable=False, comment="레벨")
    guest_number = Column(Integer, nullable=False, comment="모집인원")
    match_fee = Column(Integer, comment="매치비용")
    status = Column(String(24), nullable=False, comment="용병상태")
    notice = Column(String(255), nullable=False, comment="공지사항")
