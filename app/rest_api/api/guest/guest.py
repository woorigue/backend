from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.token import (
    get_current_user,
)
from app.helper.exception import (
    GuestNotFoundException,
    JoinGuestNotFoundException,
    MatchNotFoundException,
)
from app.model.guest import Guest, JoinGuest
from app.model.match import Match
from app.model.poll import JoinPoll, Poll
from app.rest_api.schema.guest.guest import (
    FilterGuestSchema,
    GuestResponseSchema,
    GuestSchema,
    UpdateGuestSchema,
)


guest_router = APIRouter(tags=["guest"], prefix="/guest")


@guest_router.post("")
def create_guest(
    guest_data: GuestSchema,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    guest = Guest(
        date=datetime.now(),
        user_seq=token.seq,
        club_seq=guest_data.club_seq,
        match_seq=guest_data.match_seq,
        level=guest_data.level,
        gender=guest_data.gender,
        position=guest_data.position,
        match_fee=guest_data.match_fee,
        guest_number=guest_data.guest_number,
        notice=guest_data.notice,
        status="pending",
    )
    db.add(guest)
    db.commit()
    db.refresh(guest)

    match = db.query(Match).filter(Match.seq == guest.match_seq).first()
    if match is None:
        raise MatchNotFoundException

    if match.home_club_seq == guest.club_seq:
        match.home_club_guest_seq = guest.seq
    elif match.away_club_seq == guest.club_seq:
        match.away_club_guest_seq = guest.seq

    db.commit()

    return {"success": True}


@guest_router.get("/{guest_seq}", response_model=GuestResponseSchema)
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


@guest_router.get(
    "",
    response_model=list[GuestResponseSchema],
)
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


@guest_router.post("/{guest_seq}/join")
def join_guest(
    guest_seq: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    guest = db.query(Guest).filter(Guest.seq == guest_seq).first()

    if not guest:
        raise GuestNotFoundException

    join_guest = JoinGuest(
        guest_seq=guest.seq,
        user_seq=token.seq,
        accepted=False,
    )
    db.add(join_guest)
    db.commit()

    return {"success": True}


@guest_router.patch("/{guest_seq}/accept")
def accept_guest(
    guest_seq: int,
    user_seq: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    guest = db.query(Guest).filter(Guest.seq == guest_seq).first()

    if not guest:
        raise GuestNotFoundException

    join_guest = (
        db.query(JoinGuest)
        .filter(
            JoinGuest.guest_seq == guest_seq,
            JoinGuest.user_seq == user_seq,
        )
        .first()
    )

    if not join_guest:
        raise JoinGuestNotFoundException

    # TODO: validate club owner / matcher poster

    join_guest.accepted = True

    poll = (
        db.query(Poll)
        .filter(Poll.match_seq == guest.match_seq, Poll.club_seq == guest.club_seq)
        .first()
    )
    join_poll = JoinPoll(
        attend=True, user_seq=user_seq, poll_seq=poll.seq, attendee_type="guest"
    )

    db.add(join_poll)
    db.commit()

    return {"success": True}
