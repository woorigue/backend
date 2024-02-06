from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.token import (
    get_current_user,
)

from app.model.guest import Guest
from app.rest_api.schema.guest.guest import (
    GuestSchema,
    UpdateGuestSchema,
    FilterGuestSchema,
)

# from app.rest_api.controller.guest.guest import guest_controller as con
from app.helper.exception import ProfileRequired, GuestNotFoundException


guest_router = APIRouter(tags=["guest"], prefix="/guest")


@guest_router.post("")
def create_guest(
    token: Annotated[str, Depends(get_current_user)],
    guest_data: GuestSchema,
    db: Session = Depends(get_db),
):
    guest = Guest(
        club=guest_data.club_seq,
        match=guest_data.match_seq,
        position=guest_data.position,
        skill=guest_data.skill,
        guest_number=guest_data.guest_number,
        match_fee=guest_data.match_fee,
        status=guest_data.status,
        notice=guest_data.notice,
    )
    db.add(guest)
    db.commit()

    return {"success": True}


@guest_router.get("/{guest_seq}")
def get_guest(
    token: Annotated[str, Depends(get_current_user)],
    guest_seq: int,
    db: Session = Depends(get_db),
):
    guest = db.query(Guest).filter(Guest.seq == guest_seq).first()
    if guest is None:
        raise GuestNotFoundException
    return guest


@guest_router.patch("/{guest_seq}")
def update_guest(
    token: Annotated[str, Depends(get_current_user)],
    guest_seq: int,
    guest_data: UpdateGuestSchema,
    db: Session = Depends(get_db),
):
    guest = db.query(Guest).filter(Guest.seq == guest_seq).first()

    if not guest:
        raise GuestNotFoundException

    for key, value in guest_data.dict(exclude_none=True).items():
        setattr(guest, key, value)

    db.commit()

    return {"success": True}


@guest_router.delete("/{guest_seq}")
def delete_guest(
    token: Annotated[str, Depends(get_current_user)],
    guest_seq: int,
    db: Session = Depends(get_db),
):
    guest = db.query(Guest).filter(Guest.seq == guest_seq).first()

    if not guest:
        raise GuestNotFoundException

    db.delete(guest)
    db.commit()

    return {"message": "용병게시글이 성공적으로 삭제되었습니다."}


@guest_router.get("")
def filter_guests(
    token: Annotated[str, Depends(get_current_user)],
    guest_filter: FilterGuestSchema = FilterDepends(FilterGuestSchema),
    page: int = Query(1, title="페이지", ge=1),
    per_page: int = Query(10, title="페이지당 수", ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Guest)
    query = guest_filter.filter(query)
    offset = (page - 1) * per_page
    query = query.limit(per_page).offset(offset)
    guests = query.all()

    return guests
