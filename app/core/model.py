from sqlalchemy import Column, DateTime
from datetime import datetime


class BaseModel:
    created_at = Column(DateTime, default=datetime.utcnow(), comment="생성 시간")
    updated_at = Column(
        DateTime,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow(),
        comment="업데이트 시간",
    )
