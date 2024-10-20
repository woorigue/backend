from typing import List, Optional, Literal

from pydantic import BaseModel, Field, model_validator

# from pytz import timezone
from enum import Enum, StrEnum
from datetime import datetime


class NotificationType(StrEnum):
    MESSAGE = "MESSAGE"  # 메시지(chat)
    MATCH_REQUEST = "MATCH_REQUEST"  # 매치 요청
    MATCH_ACCEPT = "MATCH_ACCEPT"  # 매치 수락
    MATCH_DENIED = "MATCH_DENIED"  # 매치 거부
    CLUB_REQUEST = "CLUB_REQUEST"  # 클럽 요청
    CLUB_ACCEPT = "CLUB_ACCEPT"  # 클럽 수락
    CLUB_DENIED = "CLUB_DENIED"  # 클럽 거부
    GUEST_REQUEST = "GUEST_REQUEST"  # 용병 요청
    GUEST_ACCEPT = "GUEST_ACCEPT"  # 용병 수락
    GUEST_DENIED = "GUEST_DENIED"  # 용병 거부


class CreateNotificationSchema(BaseModel):
    """Notification 생성 스키마"""

    type: NotificationType = Field(title="알림 타입")
    data: dict = Field(default_factory=dict, title="데이터")
    from_user_seq: int = Field(title="보내는 사용자 seq")
    to_user_seq: int = Field(title="받는 사용자 seq")
    title: str = Field(title="제목")
    message: str = Field(title="내용")


class GetNotificationSchema(BaseModel):
    seq: int = Field(title="시퀀스")
    type: NotificationType = Field(title="알림 타입")
    data: dict = Field(default_factory=dict, title="데이터")
    from_user_seq: int = Field(title="보내는 사용자 seq")
    to_user_seq: int = Field(title="받는 사용자 seq")
    title: str = Field(title="제목")
    message: str = Field(title="내용")
    is_read: bool = Field(title="읽음 여부")
    created_at: datetime = Field(title="생성일자")

    # @model_validator(mode="before")
    # def convert_created_at_to_kst(cls, values):
    #     kst = timezone("Asia/Seoul")
    #
    #     if values.created_at:
    #         values.created_at = values.created_at.astimezone(kst)
    #
    #     return values


class UpdateIsReadNotificationSchema(BaseModel):
    seq: int = Field(title="시퀀스")


class NotificationAppPushSchema(BaseModel):
    type: NotificationType = Field(title="알림 타입")
    title: str = Field(title="제목")
    message: str = Field(title="내용")
    to_user_seq: int = Field(title="받는 사용자 seq")
