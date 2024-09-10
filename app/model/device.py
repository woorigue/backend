from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, relationship

from app.db.session import Base


class Device(Base):
    __tablename__ = "device"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    user_seq = Column(Integer, ForeignKey("users.seq"), comment="유저 시퀸스")
    token = Column(String(256), comment="기기 토큰")

    user = relationship("User", back_populates="device")
