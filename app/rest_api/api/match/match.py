from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session, joinedload

from app.core.deps import get_db
from app.core.token import (
    get_current_user,
)
from app.helper.exception import (
    JoinMatchNotFoundException,
    MatchNotFoundException,
    RegisterMatchError,
)
from app.model.match import JoinMatch, Match
from app.rest_api.controller.match.match import MatchController
from app.rest_api.controller.poll import PollController
from app.rest_api.schema.match.match import (
    FilterMatchSchema,
    MatchSchema,
    UpdateMatchSchema,
    MatchResponseSchema,
)
from app.rest_api.schema.poll import (
    CreatePollSchema,
)

match_router = APIRouter(tags=["match"], prefix="/match")


@match_router.post("")
def create_match(
    token: Annotated[str, Depends(get_current_user)],
    match_data: MatchSchema,
    db: Session = Depends(get_db),
):
    controller = MatchController(db)
    is_validate = controller.validate_match_register(match_data, token.seq)

    if not is_validate:
        raise RegisterMatchError

    match = Match(
        date=datetime.now(),
        user_seq=token.seq,
        home_club_seq=match_data.home_club_seq,
        location=match_data.location,
        match_date=match_data.match_date,
        start_time=match_data.start_time,
        end_time=match_data.end_time,
        level=match_data.level,
        team_size=match_data.team_size,
        gender=match_data.gender,
        match_fee=match_data.match_fee,
        notice=match_data.notice,
        status="default",
    )
    db.add(match)
    db.commit()

    poll_data = CreatePollSchema(
        match_seq=match.seq,
        club_seq=match.home_club_seq,
        expired_at=datetime.combine(match.match_date, match.end_time),
    )
    poll_controller = PollController(token, db)
    poll = poll_controller.create_poll(poll_data)
    match.home_club_poll_seq = poll.seq

    db.commit()

    return {"success": True}


@match_router.get("/{match_seq}", response_model=MatchResponseSchema)
def get_match(
    token: Annotated[str, Depends(get_current_user)],
    match_seq: int,
    db: Session = Depends(get_db),
):
    match = (
        db.query(Match)
        .options(joinedload(Match.home_club), joinedload(Match.away_club))
        .filter(Match.seq == match_seq)
        .first()
    )

    if match is None:
        raise MatchNotFoundException

    return match


@match_router.patch("/{match_seq}")
def update_match(
    token: Annotated[str, Depends(get_current_user)],
    match_seq: int,
    match_data: UpdateMatchSchema,
    db: Session = Depends(get_db),
):
    match = db.query(Match).filter(Match.seq == match_seq).first()

    if not match:
        raise MatchNotFoundException

    for key, value in match_data.dict(exclude_none=True).items():
        setattr(match, key, value)

    db.commit()

    return {"success": True}


@match_router.delete("/{match_seq}")
def delete_match(
    token: Annotated[str, Depends(get_current_user)],
    match_seq: int,
    db: Session = Depends(get_db),
):
    match = db.query(Match).filter(Match.seq == match_seq).first()

    if not match:
        raise MatchNotFoundException

    db.delete(match)
    db.commit()

    return {"message": "매치게시글이 성공적으로 삭제되었습니다."}


@match_router.get("", response_model=list[MatchResponseSchema])
def filter_match(
    token: Annotated[str, Depends(get_current_user)],
    match_filter: FilterMatchSchema = FilterDepends(FilterMatchSchema),
    page: int = Query(1, title="페이지", ge=1),
    per_page: int = Query(10, title="페이지당 수", ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Match)
    query = match_filter.filter(query)
    offset = (page - 1) * per_page
    query = query.limit(per_page).offset(offset)
    matches = query.all()

    return matches


@match_router.post("/{match_seq}/join")
def join_match(
    match_seq: int,
    away_club_seq: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    match = db.query(Match).filter(Match.seq == match_seq).first()

    if not match:
        raise MatchNotFoundException

    if match.away_club_seq is not None:
        # TODO: validate match is pending/accepted
        raise MatchNotFoundException

    join_match = JoinMatch(
        match_seq=match.seq,
        user_seq=token.seq,
        away_club_seq=away_club_seq,
        accepted=False,
    )
    db.add(join_match)
    db.commit()

    return {"success": True}


@match_router.patch("/{match_seq}/accept")
def accept_match(
    match_seq: int,
    away_club_seq: int,
    token: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    match = db.query(Match).filter(Match.seq == match_seq).first()
    join_match = (
        db.query(JoinMatch)
        .filter(
            JoinMatch.match_seq == match_seq, JoinMatch.away_club_seq == away_club_seq
        )
        .first()
    )

    if not match:
        raise MatchNotFoundException

    if not join_match:
        raise JoinMatchNotFoundException

    # TODO: validate club owner / matcher poster

    match.status = "found"
    match.away_club_seq = away_club_seq
    join_match.accepted = True

    poll_data = CreatePollSchema(
        match_seq=match.seq,
        club_seq=match.away_club_seq,
        expired_at=datetime.combine(match.match_date, match.end_time),
    )
    poll_controller = PollController(token, db)
    poll = poll_controller.create_poll(poll_data)
    match.away_club_poll_seq = poll.seq

    db.commit()

    return {"success": True}
