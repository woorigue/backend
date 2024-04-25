from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Club(Base):
    __tablename__ = "clubs"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    name = Column(String(24), comment="클럽명")
    register_date = Column(Date, comment="창단일")
    edit_date = Column(Date, comment="수정일")
    location = Column(String(24), comment="활동 장소")
    age_group = Column(String(24), comment="연령대")
    membership_fee = Column(Integer, comment="회비")
    skill = Column(String(24), comment="실력")
    emblem_img = Column(String(256), comment="클럽 엠블럼 URL")
    img = Column(String(256), comment="클럽 이미지 URL")
    uniform_color = Column(String(24), comment="유니폼 색")
    deleted = Column(Boolean, default=False, comment="삭제 여부")

    poll = relationship("Poll", back_populates="club")
    join_club = relationship(
        "JoinClub",
        back_populates="club",
        cascade="all, delete-orphan",
    )


class JoinClub(Base):
    __tablename__ = "join_club"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    clubs_seq = Column(Integer, ForeignKey("clubs.seq", ondelete="CASCADE"))
    user_seq = Column(Integer, ForeignKey("users.seq", ondelete="CASCADE"))
    role = Column(String(10), comment="역할")
    accepted = Column(Boolean, comment="수락 여부")

    club = relationship("Club", back_populates="join_club")
    user = relationship("User", back_populates="join_club")
