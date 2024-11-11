from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship


from app.core.utils import get_position_type
from app.db.session import Base, session

db = session()


class Guest(Base):
    __tablename__ = "guest"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    date = Column(DateTime, nullable=False, comment="게시일")
    user_seq = Column(Integer, nullable=False, comment="작성자 유저 시퀀스")
    club_seq = Column(Integer, nullable=False, comment="클럽 시퀀스")
    match_seq = Column(
        Integer,
        ForeignKey("match.seq", ondelete="CASCADE"),
        nullable=False,
        comment="매치 시퀸스",
    )
    level = Column(Integer, nullable=False, comment="레벨")
    gender = Column(String(12), nullable=False, comment="성별")
    position = Column(get_position_type(), comment="포지션")
    match_fee = Column(Integer, comment="매치비용")
    guest_number = Column(Integer, nullable=False, comment="모집인원")
    notice = Column(String(255), nullable=False, comment="공지사항")
    closed = Column(Boolean, default=False, comment="공고 마감 여부")

    join_guest = relationship(
        "JoinGuest",
        back_populates="guest",
        cascade="all, delete-orphan",
    )
    home_matches = relationship(
        "Match",
        foreign_keys="[Match.home_club_guest_seq]",
        back_populates="home_club_guest",
    )
    away_matches = relationship(
        "Match",
        foreign_keys="[Match.away_club_guest_seq]",
        back_populates="away_club_guest",
    )
    match = relationship(
        "Match", foreign_keys=[match_seq], back_populates="guest", passive_deletes=True
    )

    @property
    def guest_accpeted_number(self):
        return (
            db.query(JoinGuest)
            .filter(JoinGuest.accepted == True, JoinGuest.guest_seq == self.seq)
            .count()
        )


class JoinGuest(Base):
    __tablename__ = "join_guest"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    guest_seq = Column(Integer, ForeignKey("guest.seq", ondelete="CASCADE"))
    user_seq = Column(Integer, ForeignKey("users.seq", ondelete="CASCADE"))
    accepted = Column(Boolean, comment="수락 여부")

    guest = relationship("Guest", back_populates="join_guest")
    user = relationship("User", back_populates="join_guest")
