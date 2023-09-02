from sqlalchemy import Column, Integer, String

from app.db.session import Base


class Province(Base):
    __tablename__ = "provinces"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    name = Column(String(10), comment="지역 이름")
