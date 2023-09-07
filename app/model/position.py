from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Position(Base):
    __tablename__ = "position"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    name = Column(String(12), unique=True, comment="이름")

    join_position = relationship("JoinPosition", back_populates="position")


class JoinPosition(Base):
    __tablename__ = "join_position"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    position_seq = Column(Integer, ForeignKey("position.seq"))
    profile_seq = Column(Integer, ForeignKey("profile.seq"))

    position = relationship("Position", back_populates="join_position")
    profile = relationship("Profile", back_populates="join_profile")
