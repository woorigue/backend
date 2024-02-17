from sqlalchemy import Column, Integer, String, DateTime

from app.db.session import Base


class Banner(Base):
    __tablename__ = "banner"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    url = Column(String(255), nullable=False, comment="주소")
    create_date = Column(DateTime, nullable=False, comment="생성일자")
