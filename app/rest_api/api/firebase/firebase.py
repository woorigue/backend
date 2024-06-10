from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session

# from app.helper.exception import FirebaseRefreshTokenNotFoundException

from app.core.deps import get_db
from app.core.token import (
    get_current_user,
)
from app.model.firebase import Firebase

import firebase_admin
from firebase_admin import credentials, messaging

firebase_router = APIRouter(tags=["firebase"], prefix="/firebase")


# cred = credentials.Certificate(
#     "C:/development/backend/app/rest_api/api/firebase/service_account.json"
# )
# firebase_admin.initialize_app(cred)


@firebase_router.post("")
def create_firebase_refresh_token(
    token: Annotated[str, Depends(get_current_user)],
    refresh_token: str,
    db: Session = Depends(get_db),
):
    firebase_refresh_token = Firebase(
        user_seq=token.seq,
        refresh_token=refresh_token,
    )
    db.add(firebase_refresh_token)
    db.commit()

    db.commit()

    return {"success": True}


@firebase_router.get("/{user_seq}")
def get_firebase_refresh_token(
    token: Annotated[str, Depends(get_current_user)],
    user_seq: int,
    db: Session = Depends(get_db),
):
    firebase_refresh_token = (
        db.query(Firebase).filter(Firebase.user_seq == user_seq).first()
    )

    # if firebase_refresh_token is None:
    #     raise FirebaseRefreshTokenNotFoundException

    return {"refresh_token": firebase_refresh_token.refresh_token}


@firebase_router.patch("/{user_seq}")
def update_firebase_refresh_token(
    token: Annotated[str, Depends(get_current_user)],
    user_seq: int,
    refresh_token: str,
    db: Session = Depends(get_db),
):
    firebase_refresh_token = (
        db.query(Firebase).filter(Firebase.user_seq == user_seq).first()
    )

    # if not firebase_refresh_token:
    #     raise FirebaseRefreshTokenNotFoundException

    firebase_refresh_token.refresh_token = refresh_token

    db.commit()

    return {"success": True}


@firebase_router.post("/notification")
def sendPush(title, msg, registration_token, data=None):
    # See documentation on defining a message payload.
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=msg),
        data=data,
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send_multicast(message)
    # Response is a message ID string.
    print("Successfully sent message:", response)
