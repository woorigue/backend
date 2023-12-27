from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


class ClubPosting(Base):
    __tablename__ = "clubPosting"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    club_seq = Column(Integer, comment="클럽 시퀸스")
    title = Column(String(128), comment="제목")
    intro = Column(String(255), comment="클럽 소개글")
    recruitment_number = Column(Integer, comment="모집 회원 수")
    location = Column(String(24), comment="활동 장소")
    age_group = Column(String(24), comment="연령대")
    membership_fee = Column(Integer, comment="회비")
    skill = Column(String(24), comment="실력")
    gender = Column(String(12), comment="성별")
    status = Column(String(24), comment="상태")
    user_seq = Column(Integer, comment="유저 시퀸스")

    join_club_posting = relationship(
        "JoinClubPosting",
        back_populates="club_posting",
        cascade="all, delete-orphan",
    )


class JoinClubPosting(Base):
    __tablename__ = "join_clubPosting"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    club_posting_seq = Column(
        Integer, ForeignKey("clubPosting.seq", ondelete="CASCADE")
    )
    club_seq = Column(Integer, ForeignKey("clubs.seq", ondelete="CASCADE"))
    user_seq = Column(Integer, ForeignKey("users.seq", ondelete="CASCADE"))
    accepted = Column(Boolean, comment="수락 여부")

    club_posting = relationship("ClubPosting", back_populates="join_club_posting")
