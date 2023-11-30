from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


class Club(Base):
    __tablename__ = "clubs"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    name = Column(String(24), comment="클럽명")
    register_date = Column(Date, comment="창단일")
    location = Column(String(24), comment="활동 장소")
    age_group = Column(String(24), comment="연령대")
    membership_fee = Column(Integer, comment="회비")
    skill = Column(String(24), comment="실력")
    img = Column(String(256), comment="클럽 이미지 URL")
    color = Column(String(24), comment="유니폼 색")
    deleted = Column(Boolean, default=True, comment="삭제 여부")

    join_club = relationship("JoinClub", back_populates="club")


class JoinClub(Base):
    __tablename__ = "join_club"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    clubs_seq = Column(Integer, ForeignKey("clubs.seq"))
    user_seq = Column(Integer, ForeignKey("users.seq"))
    role = Column(String(10), comment="역할")

    club = relationship("Club", back_populates="join_club")
    user = relationship("User", back_populates="join_club")
