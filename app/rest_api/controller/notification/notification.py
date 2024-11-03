from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from typing import final, Optional

from firebase_admin import messaging
from sqlalchemy.orm import Session

from app.model.device import Device, DeviceTypeEnum
from app.model.club import Club, JoinClub
from app.model.match import Match
from app.model.guest import Guest
from app.model.notification import Notification
from app.model.user import User
from app.rest_api.schema.notification.notification import (
    CreateNotificationSchema,
    NotificationType,
)
from app.rest_api.schema.notification.notification import (
    NotificationAppPushSchema,
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
    def send(self, db: Session, publisher_user: User) -> None:
        notification_schema = self.create_schema(publisher_user.seq)
        self.save_to_db(db, notification_schema)

        device_info = self.get_device_info(db, notification_schema.to_user_seq)
        for device in device_info:
            try:
                if device.token:
                    self.send_push(db, notification_schema, device)
            except Exception as e:
                print(e)
                continue

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
    def get_device_info(db: Session, user_seq: int) -> list:
        device_info = db.query(Device).filter(Device.user_seq == user_seq).all()
        return device_info

    @staticmethod
    @final
    def send_push(
        db: Session,
        data: CreateNotificationSchema,
        device: Device,
    ) -> None:
        message_kwargs = {
            "notification": messaging.Notification(title=data.title, body=data.message),
            "token": device.token,
        }

        notification_count = (
            db.query(Notification)
            .filter(
                Notification.to_user_seq == data.to_user_seq,
                Notification.is_read != True,
            )
            .count()
        )

        if device.type == DeviceTypeEnum.iOS.value:
            message_kwargs["apns"] = messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        badge=notification_count,
                    )
                )
            )
        elif device.type == DeviceTypeEnum.AOS.value:
            message_kwargs["android"] = messaging.AndroidConfig(
                notification=messaging.AndroidNotification(
                    notification_count=notification_count
                )
            )

        message = messaging.Message(**message_kwargs)
        messaging.send(message)


class MatchNotificationService(AbstractNotification):
    TITLE = "매치 신청 알림"
    MESSAGE = "매치 신청이 도착했습니다."

    def __init__(self, db: Session, match: Match, away_club_seq: int) -> None:
        self.db = db
        self.match = match
        self.away_club_seq = away_club_seq

    def create_schema(self, publisher_user_seq: int) -> CreateNotificationSchema:
        away_club = self.db.query(Club).filter(Club.seq == self.away_club_seq).first()
        data = {
            "away_club_seq": away_club.seq,
            "away_club_name": away_club.name,
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


class ClubNotificationService(AbstractNotification):
    TITLE = "클럽 신청 알림"
    MESSAGE = "클럽 신청이 도착했습니다."

    def __init__(self, db: Session, publisher_name: str, club: Club) -> None:
        self.db = db
        self.publisher_name = publisher_name
        self.club = club

    def create_schema(self, publisher_user_seq: int) -> CreateNotificationSchema:
        club_owner = (
            self.db.query(JoinClub)
            .filter(JoinClub.clubs_seq == self.club.seq, JoinClub.role == "owner")
            .first()
        )
        data = {
            "club_seq": self.club.seq,
            "club_name": self.club.name,
            "publisher_name": self.publisher_name,
        }
        notification_schema = CreateNotificationSchema(
            type=NotificationType.CLUB_REQUEST.value,
            title=self.TITLE,
            message=self.MESSAGE,
            from_user_seq=publisher_user_seq,
            to_user_seq=club_owner.user_seq,
            data=data,
        )
        return notification_schema


class GuestNotificationService(AbstractNotification):
    TITLE = "용병 신청 알림알림"
    MESSAGE = "새로운 용병 신청이 들어왔습니다."

    def __init__(self, db: Session, publisher_name: str, guest: Guest) -> None:
        self.db = db
        self.publisher_name = publisher_name
        self.guest = guest

    def create_schema(self, publisher_user_seq: int) -> CreateNotificationSchema:
        data = {
            "guest_seq": self.guest.seq,
            "publisher_name": self.publisher_name,
            "match_date": self.guest.match.match_date.strftime("%Y-%m-%d"),
        }
        notification_schema = CreateNotificationSchema(
            type=NotificationType.GUEST_REQUEST.value,
            title=self.TITLE,
            message=self.MESSAGE,
            from_user_seq=publisher_user_seq,
            to_user_seq=self.guest.user_seq,
            data=data,
        )
        return notification_schema


class CommonNotificationService(AbstractNotification):
    TITLE = ""
    MESSAGE = ""

    def __init__(
        self, db: Session, data: NotificationAppPushSchema, user: User
    ) -> None:
        self.db = db
        self.data = data
        self.user = user

    def create_schema(self, publisher_user_seq: int) -> CreateNotificationSchema:
        data = {
            "publisher_name": self.user.profile[0].nickname,
        }
        notification_schema = CreateNotificationSchema(
            type=self.data.type,
            title=self.data.title,
            message=self.data.message,
            from_user_seq=publisher_user_seq,
            to_user_seq=self.data.to_user_seq,
            data=data,
        )
        return notification_schema
