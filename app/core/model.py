from sqlalchemy import Column, DateTime
from datetime import datetime
from app.db.session import Base


class TimestampedModel(Base):
    __abstract__ = True  # 추상화

    created_at = Column(DateTime, default=datetime.utcnow, comment="생성 시간")
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="업데이트 시간",
    )
