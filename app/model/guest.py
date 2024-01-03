from sqlalchemy import ARRAY, Column, String, Integer, DateTime
from sqlalchemy.orm import Session

from app.db.session import Base

from datetime import datetime
from dataclasses import dataclass

from app.rest_api.schema.guest.guest import GuestRegisterSchema

from app.helper.exception import (
    RegisterException
)

class Guest(Base):
    __tablename__ = "guest"
    
    seq = Column(Integer, primary_key = True, autoincrement = True, comment = "시퀀스")
    club = Column(Integer, nullable = False, comment = "클럽id")
    match = Column(Integer, nullable = False, comment = "매치id")
    position = Column(ARRAY(Integer), comment = "포지션")
    skill = Column(String(24), nullable = False, comment="레벨")
    guest_number = Column(Integer, nullable = False, comment = "모집인원")
    match_fee = Column(Integer, comment="매치비용")
    status = Column(String(24), nullable = False, comment="용병상태")
    notice = Column(String(255), nullable = False, comment="공지사항")
    
    @staticmethod
    def create(guest_data: GuestRegisterSchema, db: Session)-> None:
        print("----create----", guest_data)
        club = guest_data.club
        match = guest_data.match
        position = guest_data.position
        skill = guest_data.skill
        guest_number = guest_data.guest_number
        match_fee = guest_data.match_fee
        status = guest_data.status
        notice = guest_data.notice
        
        if not club:
            raise RegisterException("club")
        if not match:
            raise RegisterException("match")
        if not position:
            raise RegisterException("position")
        if not skill:
            raise RegisterException("skill")
        if not guest_number:
            raise RegisterException("guest_number")            
        if not match_fee:
            raise RegisterException("match_fee")
        if not status:
            raise RegisterException("status")
        if not notice:
            raise RegisterException("notice")
       
        guest = Guest(
            club = club,
            match = match,
            position = position,
            skill = skill,
            guest_number = guest_number,
            match_fee = match_fee,
            status = status,
            notice = notice,
        )
        db.add(guest)
        db.commit()