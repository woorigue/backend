from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.token import (
    get_current_user,
)
from app.core.utils import error_responses
from app.helper.exception import (
    GuestNotFoundException,
    GuestPermissionDeniedException,
    JoinGuestNotFoundException,
    MatchNotFoundException,
)
from app.model.guest import Guest, JoinGuest
from app.model.match import Match
from app.model.poll import JoinPoll, Poll
from app.rest_api.controller.guest.guest import GuestController
from app.rest_api.schema.base import CreateResponse
from app.rest_api.schema.guest.guest import (
    FilterGuestSchema,
    GuestResponseSchema,
    GuestSchema,
    UpdateGuestSchema,
)

guest_router = APIRouter(tags=["guest"], prefix="/guest")


@guest_router.post(
    "",
    summary="용병 모집글 생성",
    responses={404: {"description": error_responses([MatchNotFoundException])}},
)
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


@guest_router.get(
    "/{guest_seq}",
    summary="용병 상세 조회",
    responses={404: {"description": error_responses([GuestNotFoundException])}},
    response_model=GuestResponseSchema,
)
def get_guest(
    token: Annotated[str, Depends(get_current_user)],
    guest_seq: int,
    db: Session = Depends(get_db),
):
    guest = db.query(Guest).filter(Guest.seq == guest_seq).first()
    if guest is None:
        raise GuestNotFoundException
    return guest


@guest_router.patch(
    "/{guest_seq}",
    summary="용병 공고글 수정",
    responses={
        400: {"description": error_responses([GuestPermissionDeniedException])},
        404: {"description": error_responses([GuestNotFoundException])},
    },
)
def update_guest(
    token: Annotated[str, Depends(get_current_user)],
    guest_seq: int,
    guest_data: UpdateGuestSchema,
    db: Session = Depends(get_db),
):
    guest = db.query(Guest).filter(Guest.seq == guest_seq).first()
    if not guest:
        raise GuestNotFoundException
    if guest.user_seq != token.seq:
        raise GuestPermissionDeniedException

    for key, value in guest_data.dict(exclude_none=True).items():
        setattr(guest, key, value)

    db.commit()

    return {"success": True}


@guest_router.delete(
    "/{guest_seq}",
    summary="용병 모집글 삭제",
    responses={
        400: {"description": error_responses([GuestPermissionDeniedException])},
        404: {"description": error_responses([GuestNotFoundException])},
    },
    response_model=CreateResponse,
)
def delete_guest(
    token: Annotated[str, Depends(get_current_user)],
    guest_seq: int,
    db: Session = Depends(get_db),
):
    guest = db.query(Guest).filter(Guest.seq == guest_seq).first()

    if not guest:
        raise GuestNotFoundException

    if guest.user_seq != token.seq:
        raise GuestPermissionDeniedException

    db.delete(guest)
    db.commit()

    return {"success": True}


@guest_router.get(
    "",
    summary="용병 모집글 조회",
    response_model=list[GuestResponseSchema],
)
def filter_guests(
    token: Annotated[str, Depends(get_current_user)],
    guest_filter: FilterGuestSchema = FilterDepends(FilterGuestSchema),
    page: int = Query(1, title="페이지", ge=1),
    per_page: int = Query(10, title="페이지당 수", ge=1, le=100),
    db: Session = Depends(get_db),
):
    today = datetime.today()
    query = (
        db.query(Guest)
        .join(Match, Guest.match_seq == Match.seq)
        .filter(
            Guest.closed == False, Match.matched == False, Match.match_date >= today
        )
    )
    guest_con = GuestController()
    filter_conditions = guest_con.build_filters(guest_filter.dict())
    if filter_conditions is not None:
        query = query.filter(filter_conditions)
    offset = (page - 1) * per_page
    query = query.limit(per_page).offset(offset)
    guests = query.all()

    return guests


@guest_router.post(
    "/{guest_seq}/join",
    summary="용병 참석 요청",
    responses={404: {"description": error_responses([GuestNotFoundException])}},
    response_model=CreateResponse,
)
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


@guest_router.patch(
    "/{guest_seq}/accept",
    summary="용병 수락",
    responses={
        400: {
            "description": error_responses([GuestPermissionDeniedException]),
        },
        404: {
            "description": error_responses(
                [GuestNotFoundException, JoinGuestNotFoundException]
            )
        },
    },
)
def accept_guest(
    guest_seq: int,
    user_seq: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    guest = db.query(Guest).filter(Guest.seq == guest_seq).first()

    if not guest:
        raise GuestNotFoundException

    if guest.user_seq != token.seq:
        raise GuestPermissionDeniedException

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
