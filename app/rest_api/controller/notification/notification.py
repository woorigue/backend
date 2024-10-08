from __future__ import annotations
from abc import ABC, abstractmethod
from app.rest_api.schema.notification.notification import (
    CreateNotificationSchema,
)


class AbstractNotification(ABC):
    @abstractmethod
    def send(self, data: CreateNotificationSchema) -> str:
        pass

    @abstractmethod
    def save_notification(self) -> None:
        pass


class AbstractNotificationFactory(ABC):
    @abstractmethod
    def create_notification(self) -> AbstractNotification:
        pass


class MatchNotification(AbstractNotification):
    def __init__(self):
        self.title = "매치 신청 알림"
        self.message = ("매치 신청이 도착했습니다.",)

    def send(self, data: CreateNotificationSchema) -> str:
        return "매치 노티피케이션을 보냅니다."


class ClubNotification(AbstractNotification):
    def send(self, data: CreateNotificationSchema) -> str:
        return "클럽 노티피케이션을 보냅니다."


class MatchNotificationFactory(AbstractNotificationFactory):
    def create_notification(self) -> AbstractNotification:
        return MatchNotification()


def notification_client_code(
    factory: AbstractNotificationFactory, data: CreateNotificationSchema
):
    notification = factory.create_notification()
    notification.send(data)
