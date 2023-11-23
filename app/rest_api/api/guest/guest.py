from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.deps import get_db
from app.core.token import (
    get_current_user,
)

from app.model.guest import Guest
from sqlalchemy.sql import func
from sqlalchemy import extract

# Schema
from app.rest_api.schema.guest.guest import (
    GuestListSchema,
    GuestRegisterSchema,
    GuestUpdateSchema,
)

# Controller
from app.rest_api.controller.guest.guest import guest_controller as con

from app.helper.exception import ProfileRequired, GuestNotFoundException

from datetime import datetime, time
from typing import List

guest_router = APIRouter(tags=["guest"], prefix="/guest")


def get_user_info_with_profile(token: Annotated[str, Depends(get_current_user)]):
    if not token.profile:
        raise ProfileRequired

    return True


@guest_router.get("")
def list_guests(
    # token: Annotated[str, Depends(get_current_user)],
    # guest_data: GuestListSchema = Depends(),
    position: Optional[List[int]] = Query(None, title="포지션"),
    skill: Optional[str] = Query(None, title="레벨"),
    db: Session = Depends(get_db),
):
    # get_user_info_with_profile(token)

    query = db.query(Guest)
    if position:
        query = query.filter(Guest.position == position)
    if skill:
        query = query.filter(Guest.skill == skill)

    guests = query.all()
    return guests


@guest_router.get("/{guest_id}")
def get_guest(
    # token: Annotated[str, Depends(get_current_user)],
    guest_id: int,
    db: Session = Depends(get_db),
):
    # get_user_info_with_profile(token)

    guest = db.query(Guest).filter(Guest.seq == guest_id).first()
    if guest is None:
        raise GuestNotFoundException
    return guest


@guest_router.post("")
def create_guest(
    # token: Annotated[str, Depends(get_current_user)],
    guest_data: GuestRegisterSchema,
    db: Session = Depends(get_db),
):
    # get_user_info_with_profile(token)

    con.register_guest(guest_data, db)
    return {"success": True}


@guest_router.patch("/{guest_id}")
def edit_guest(
    # token: Annotated[str, Depends(get_current_user)],
    guest_id: int,
    guest_data: GuestUpdateSchema,
    db: Session = Depends(get_db),
):
    # get_user_info_with_profile(token)

    guest = db.query(Guest).filter(Guest.seq == guest_id).first()
    if not guest:
        raise GuestNotFoundException

    for key, value in guest_data.dict(exclude_unset=True).items():
        setattr(guest, key, value)

    db.commit()
    return {"success": True}


@guest_router.delete("/{guest_id}")
def delete_guest(
    # token: Annotated[str, Depends(get_current_user)],
    guest_id: int,
    db: Session = Depends(get_db),
):
    # get_user_info_with_profile(token)

    guest = db.query(Guest).filter(Guest.seq == guest_id).first()
    if not guest:
        raise GuestNotFoundException

    db.delete(guest)
    db.commit()
    return {"message": "용병게시글이 성공적으로 삭제되었습니다."}
