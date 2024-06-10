from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Match(Base):
    __tablename__ = "match"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    date = Column(DateTime, nullable=False, comment="게시일")
    user_seq = Column(Integer, nullable=False, comment="유저 시퀸스")
    home_club_seq = Column(Integer, nullable=False, comment="홈 클럽 시퀸스")
    away_club_seq = Column(Integer, comment="원정 클럽 시퀸스")
    match_type = Column(String(24), nullable=False, comment="매치유형")
    location = Column(String(128), nullable=False, comment="매치장소")
    match_date = Column(DateTime, nullable=False, comment="매칭일")
    start_time = Column(DateTime, nullable=False, comment="매치 시작 시간")
    end_time = Column(DateTime, nullable=False, comment="매치 종료 시간")
    level = Column(Integer, nullable=False, comment="레벨")
    team_size = Column(Integer, nullable=False, comment="매치인원")
    gender = Column(String(12), nullable=False, comment="성별")
    match_fee = Column(Integer, nullable=True, comment="매치비용")
    notice = Column(String(255), nullable=True, comment="공지사항")
    status = Column(String(24), nullable=False, comment="매치상태")
    guest_seq = Column(Integer, nullable=False, comment="용병 게시글 시퀸스")
    home_club_poll_seq = Column(
        Integer,
        nullable=False,
        comment="홈 클럽 투표 시퀸스",
    )
    away_club_poll_seq = Column(
        Integer,
        comment="원정 클럽 투표 시퀸스",
    )

    poll = relationship("Poll", back_populates="match")
    join_match = relationship(
        "JoinMatch",
        back_populates="match",
        cascade="all, delete-orphan",
    )


class JoinMatch(Base):
    __tablename__ = "join_match"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    match_seq = Column(Integer, ForeignKey("match.seq", ondelete="CASCADE"))
    away_club_seq = Column(Integer, ForeignKey("clubs.seq", ondelete="CASCADE"))
    user_seq = Column(Integer, ForeignKey("users.seq", ondelete="CASCADE"))
    accepted = Column(Boolean, comment="수락 여부")

    match = relationship("Match", back_populates="join_match")
