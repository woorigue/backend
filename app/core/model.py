from sqlalchemy import Column, DateTime, Integer
from datetime import datetime


class BaseModel:
    seq = Column(Integer, primary_key=True, autoincrement=True, comment="시퀀스")
    created_at = Column(DateTime, default=datetime.utcnow(), comment="생성 시간")
    updated_at = Column(
        DateTime,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
        comment="업데이트 시간",
    )
