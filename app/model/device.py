from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import Session, relationship

from app.db.session import Base
from enum import StrEnum
from sqlalchemy.orm import Mapped, mapped_column


class DeviceTypeEnum(StrEnum):
    """디바이스 타입 enum"""

    AOS = "AOS"
    iOS = "iOS"


class Device(Base):
    __tablename__ = "device"

    seq: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="시퀀스"
    )
    user_seq: Mapped[int] = mapped_column(ForeignKey("users.seq"), comment="유저 시퀸스")
    token: Mapped[str] = mapped_column(String(256), comment="기기 토큰")
    type: Mapped[DeviceTypeEnum] = mapped_column(Enum(DeviceTypeEnum), comment="타입")

    user = relationship("User", back_populates="device")
