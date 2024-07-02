from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class MemberPosting(Base):
    __tablename__ = "memberPosting"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    date = Column(DateTime, nullable=False, comment="게시일")
    user_seq = Column(Integer, ForeignKey("profile.user_seq"), comment="유저 시퀸스")
    title = Column(String(128), comment="제목")
    notice = Column(String(255), comment="소개글")
    status = Column(String(24), comment="상태")

    user_profile = relationship("Profile", backref="member_postings")
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
