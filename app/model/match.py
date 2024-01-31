from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import Session, relationship

from app.db.session import Base

from app.rest_api.schema.match.match import MatchRegisterSchema

from app.helper.exception import RegisterException


class Match(Base):
    __tablename__ = "match"

    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    match_type = Column(String(24), nullable=False, comment="매치유형")
    location = Column(String(128), nullable=False, comment="매치장소")
    match_time = Column(DateTime, nullable=False, comment="매치일정")
    skill = Column(String(24), nullable=False, comment="레벨")
    team_size = Column(Integer, nullable=False, comment="매치인원")
    gender = Column(String(12), nullable=False, comment="성별")
    match_fee = Column(Integer, nullable=True, comment="매치비용")
    notice = Column(String(255), nullable=True, comment="공지사항")
    status = Column(String(24), nullable=False, comment="매치상태")
    guests = Column(Integer, nullable=False, comment="용병id")
    club_seq = Column(Integer, nullable=False, comment="클럽id")

    poll = relationship("Poll", back_populates="match")

    @staticmethod
    def create(match_data: MatchRegisterSchema, db: Session) -> None:
        match_type = match_data.match_type
        location = match_data.location
        match_time = match_data.match_time
        skill = match_data.skill
        team_size = match_data.team_size
        gender = match_data.gender
        match_fee = match_data.match_fee
        notice = match_data.notice
        status = match_data.status
        guests = match_data.guests
        club_seq = match_data.club_seq
        # 필수 필드 검사
        if not match_type:
            raise RegisterException("match_type")
        if not location:
            raise RegisterException("location")
        if not match_time:
            raise RegisterException("match_time")
        if not skill:
            raise RegisterException("skill")
        if team_size is None:
            raise RegisterException("team_size")
        if not gender:
            raise RegisterException("gender")
        if match_fee is None:
            raise RegisterException("match_fee")
        if not status:
            raise RegisterException("status")
        if guests is None:
            raise RegisterException("guests")
        if club_seq is None:
            raise RegisterException("club_seq")

        # Match 객체 생성 및 데이터베이스에 추가
        match = Match(
            match_type=match_type,
            location=location,
            match_time=match_time,
            skill=skill,
            team_size=team_size,
            gender=gender,
            match_fee=match_fee,
            notice=notice,
            status=status,
            guests=guests,
            club_seq=club_seq,
        )
        db.add(match)
        db.commit()
