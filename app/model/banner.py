from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.session import Base

from datetime import datetime


class Banner(Base):
    __tablename__ = "banner"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    url = Column(String(255), nullable=False, comment="주소")
    create_date = Column(DateTime, nullable=False, comment="생성일자")
