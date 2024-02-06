from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class MemberPosting(Base):
    __tablename__ = "memberPosting"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    user_seq = Column(Integer, comment="유저 시퀸스")
    club_seq = Column(Integer, comment="클럽 시퀸스")
    title = Column(String(128), comment="제목")
    intro = Column(String(255), comment="소개글")
    age_group = Column(String(24), comment="연령대")
    gender = Column(String(12), comment="성별")
    skill = Column(String(24), comment="실력")
    location = Column(String(24), comment="활동 장소")
    status = Column(String(24), comment="상태")

    join_member_posting = relationship(
        "JoinMemberPosting",
        back_populates="member_posting",
        cascade="all, delete-orphan",
    )


class JoinMemberPosting(Base):
    __tablename__ = "join_memberPosting"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    member_posting_seq = Column(
        Integer, ForeignKey("memberPosting.seq", ondelete="CASCADE")
    )
    club_seq = Column(Integer, ForeignKey("clubs.seq", ondelete="CASCADE"))
    user_seq = Column(Integer, ForeignKey("users.seq", ondelete="CASCADE"))
    accepted = Column(Boolean, comment="수락 여부")

    member_posting = relationship("MemberPosting", back_populates="join_member_posting")
    user = relationship("User", back_populates="join_member_posting")
