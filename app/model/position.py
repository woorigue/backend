from fastapi import HTTPException, status
from sqlalchemy import Column, Integer, String

from app.db.session import Base


class Position(Base):
    __tablename__ = "position"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    name = Column(String(12), unique=True, comment="이름")
