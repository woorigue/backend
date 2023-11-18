from sqlalchemy import Boolean, Column, Integer, String, select
from sqlalchemy.orm import Session, relationship

from app.db.session import Base


class Sns(Base):
    __tablename__ = "sns"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    refresh_token = Column(String(128), comment="지역 이름")
    sub = Column(String(64), comment="구분 값")

    # user = relationship("User", back_populates="sns")
    # join_sns = relationship("JoinSns", back_populates="sns")
