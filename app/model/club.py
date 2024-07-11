from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String

from app.db.session import Base, session

db = session()


class Club(Base):
    __tablename__ = "clubs"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    name = Column(String(24), comment="클럽명")
    register_date = Column(Date, comment="창단일")
    edit_date = Column(Date, comment="수정일")
    intro = Column(String(512), comment="소개글")
    location = Column(String(24), comment="활동 장소")
    age_group = Column(String(24), comment="연령대")
    membership_fee = Column(Integer, comment="회비")
    level = Column(Integer, comment="레벨")
    gender = Column(String(12), nullable=False, comment="성별")
    emblem_img = Column(String(256), comment="클럽 엠블럼 URL")
    img = Column(String(256), comment="클럽 이미지 URL")
    uniform_color = Column(String(24), comment="유니폼 색")
    deleted = Column(Boolean, default=False, comment="삭제 여부")

    members = relationship("User", secondary="join_club", back_populates="clubs")

    poll = relationship("Poll", back_populates="club")
    home_matches = relationship(
        "Match",
        foreign_keys="[Match.home_club_seq]",
        back_populates="home_club",
        cascade="all, delete-orphan",
    )
    away_matches = relationship(
        "Match",
        foreign_keys="[Match.away_club_seq]",
        back_populates="away_club",
        cascade="all, delete-orphan",
    )

    @property
    def roles(self):
        roles = (
            db.query(JoinClub.user_seq, JoinClub.role)
            .filter(JoinClub.clubs_seq == self.seq)
            .all()
        )
        return {role: user_seq for user_seq, role in roles}

    @property
    def team_size(self):
        return db.query(JoinClub).filter(JoinClub.clubs_seq == self.seq).count()


class JoinClub(Base):
    __tablename__ = "join_club"

    seq = Column(Integer, primary_key=True, comment="시퀀스")
    clubs_seq = Column(Integer, ForeignKey("clubs.seq", ondelete="CASCADE"))
    user_seq = Column(Integer, ForeignKey("users.seq", ondelete="CASCADE"))
    role = Column(String(10), comment="역할")
    accepted = Column(Boolean, comment="수락 여부")
