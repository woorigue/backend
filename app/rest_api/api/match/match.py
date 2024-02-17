from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.token import (
    get_current_user,
)
from app.model.match import Match
from app.rest_api.schema.match.match import (
    MatchSchema,
    UpdateMatchSchema,
    FilterMatchSchema,
)

from app.helper.exception import MatchNotFoundException


match_router = APIRouter(tags=["match"], prefix="/match")


@match_router.post("")
def create_match(
    token: Annotated[str, Depends(get_current_user)],
    match_data: MatchSchema,
    db: Session = Depends(get_db),
):
    match = Match(
        match_type=match_data.match_type,
        location=match_data.location,
        match_time=match_data.match_time,
        skill=match_data.skill,
        team_size=match_data.team_size,
        gender=match_data.gender,
        match_fee=match_data.match_fee,
        notice=match_data.notice,
        status=match_data.status,
        guests=match_data.guests,
        club_seq=match_data.club_seq,
    )
    db.add(match)
    db.commit()

    return {"success": True}


@match_router.get("/{match_seq}")
def get_match(
    token: Annotated[str, Depends(get_current_user)],
    match_seq: int,
    db: Session = Depends(get_db),
):
    match = db.query(Match).filter(Match.seq == match_seq).first()

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


@match_router.get("")
def filter_matches(
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
