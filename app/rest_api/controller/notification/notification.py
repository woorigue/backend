from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from typing import final, Optional

from firebase_admin import messaging
from sqlalchemy.orm import Session

from app.model.device import Device
from app.model.match import Match
from app.model.notification import Notification
from app.model.user import User
from app.rest_api.schema.notification.notification import (
    CreateNotificationSchema,
    NotificationType,
)


class NotificationMeta(ABCMeta):
    def __new__(cls, name, bases, namespace, **kwargs) -> type:
        if name != "AbstractNotification":
            if "TITLE" not in namespace:
                raise TypeError(f"{name} must define TITLE")
            if "MESSAGE" not in namespace:
                raise TypeError(f"{name} must define MESSAGE")
        return super().__new__(cls, name, bases, namespace, **kwargs)


class AbstractNotification(ABC, metaclass=NotificationMeta):
    def send(self, publisher_user: User, db: Session) -> None:
        notification_schema = self.create_schema(publisher_user.seq)
        self.save_to_db(db, notification_schema)

        device_info = self.get_device_info(db, notification_schema.to_user_seq)
        if device_info:
            self.send_push(notification_schema, device_info)

    @abstractmethod
    def create_schema(self, publisher_user_seq: int) -> CreateNotificationSchema:
        pass

    @staticmethod
    @final
    def save_to_db(db: Session, data: CreateNotificationSchema) -> None:
        notification = Notification(**data.model_dump())
        db.add(notification)
        db.commit()

    @staticmethod
    @final
    def get_device_info(db: Session, user_seq: int) -> Optional[Device]:
        device_info = db.query(Device).filter(Device.user_seq == user_seq).first()
        return device_info

    @staticmethod
    @final
    def send_push(data: CreateNotificationSchema, device: Device) -> None:
        message = messaging.Message(
            notification=messaging.Notification(title=data.title, body=data.message),
            token=device.token,
        )
        messaging.send(message)


class MatchNotificationService(AbstractNotification):
    TITLE = "매치 신청 알림"
    MESSAGE = "매치 신청이 도착했습니다."

    def __init__(self, match: Match) -> None:
        self.match = match

    def create_schema(self, publisher_user_seq: int) -> CreateNotificationSchema:
        data = {
            "away_club_seq": self.match.away_club_seq,
            "away_club_name": self.match.away_club.name,
            "match_seq": self.match.seq,
            "match_date": self.match.match_date.strftime("%Y-%m-%d"),
        }
        notification_schema = CreateNotificationSchema(
            type=NotificationType.MATCH_REQUEST.value,
            title=self.TITLE,
            message=self.MESSAGE,
            from_user_seq=publisher_user_seq,
            to_user_seq=self.match.user_seq,
            data=data,
        )
        return notification_schema
