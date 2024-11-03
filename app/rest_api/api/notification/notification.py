from datetime import datetime
from typing import Annotated
import requests
import secrets

import httpx
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, Request, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session
from starlette.config import Config
from app.helper.exception import NotificationNotFoundException
from app.model.device import Device
from firebase_admin import messaging

from app.core.config import settings
from app.core.deps import get_db
from app.core.token import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    validate_refresh_token,
    verify_password,
    create_rls_refresh_token,
    create_rls_access_token,
)
from app.core.utils import error_responses
from app.model.notification import Notification
from app.rest_api.controller.email import email_controller as email_con
from app.rest_api.controller.file import file_controller as file_con
from app.rest_api.controller.user import user_controller as con
from app.rest_api.schema.base import CreateResponse
from app.rest_api.schema.email import (
    EmailAuthCodeSchema,
    EmailPasswordResetSchema,
    EmailVerifySchema,
)
from app.rest_api.schema.notification.notification import (
    GetNotificationSchema,
    UpdateIsReadNotificationSchema,
    NotificationAppPushSchema,
)
from app.rest_api.schema.profile import UpdateProfileSchema
from app.rest_api.schema.token import RefreshTokenSchema
from app.rest_api.schema.user import (
    EmailLoginSchema,
    EmailRegisterSchema,
    ResetPasswordSchema,
    UserLoginResponse,
    UserSchema,
    GoogleLoginSchema,
    UserSnsLoginSchema,
    UserDeviceTokenSchema,
)
from app.rest_api.controller.notification.notification import CommonNotificationService


notification_router = APIRouter(tags=["notification"], prefix="/notification")


@notification_router.get(
    "/app/push",
    summary="앱 푸시 조회",
    response_model=list[GetNotificationSchema],
)
def get_app_push_notification(
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    notification_list = (
        db.query(Notification)
        .order_by(Notification.created_at.desc())
        .filter(Notification.to_user_seq == token.seq)
        .all()
    )
    return notification_list


@notification_router.patch(
    "/app/push/read",
    summary="앱 푸시 읽음 처리",
)
def update_app_push_notification_is_read(
    data: UpdateIsReadNotificationSchema,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    notification = (
        db.query(Notification)
        .order_by(Notification.created_at.desc())
        .filter(Notification.to_user_seq == token.seq, Notification.seq == data.seq)
    ).first()

    if not notification:
        raise NotificationNotFoundException

    notification.is_read = True
    db.add(notification)
    db.commit()
    return {"success": True}


@notification_router.post(
    "/app/push",
    summary="앱 푸시",
)
def app_push_notification(
    notification_data: NotificationAppPushSchema,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    service = CommonNotificationService(db, notification_data, token)
    service.send(db, token)
    return {"success": True}


@notification_router.delete(
    "/app/push/{notification_id}",
    summary="앱 푸시 삭제",
)
def app_push_notification(
    notification_id: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.seq == notification_id,
            Notification.to_user_seq == token.seq,
        )
        .first()
    )
    if notification is not None:
        db.delete(notification)
        db.commit()
    return {"success": True}
