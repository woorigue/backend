from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class Firebase(Base):
    __tablename__ = "firebase"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    user_seq = Column(Integer, ForeignKey("users.seq", ondelete="CASCADE"))
    refresh_token = Column(String(128), comment="리프레시 토큰")

    user = relationship("User", back_populates="firebase")
