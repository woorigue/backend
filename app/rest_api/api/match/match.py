from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.deps import get_db
from app.core.token import (
    get_current_user,
)

from app.model.match import Match
from sqlalchemy.sql import func
from sqlalchemy import extract

# Schema
from app.rest_api.schema.match.match import (
    MatchListSchema,
    MatchRegisterSchema,
    MatchUpdateSchema,
)

# Controller
from app.rest_api.controller.match.match import match_controller as con

from app.helper.exception import ProfileRequired, MatchNotFoundException

from datetime import datetime, time

match_router = APIRouter(tags=["match"], prefix="/match")


def get_time_range(range_str):
    ranges = {
        "0-4": (0, 4),
        "4-8": (4, 8),
        "8-12": (8, 12),
        "12-16": (12, 16),
        "16-20": (16, 20),
        "20-24": (20, 24),
    }
    return ranges.get(range_str, (0, 23))


def get_user_info_with_profile(token: Annotated[str, Depends(get_current_user)]):
    if not token.profile:
        raise ProfileRequired

    return True


@match_router.get("")
def list_matches(
    # token: Annotated[str, Depends(get_current_user)],
    match_data: MatchListSchema = Depends(),
    # match_data: MatchListSchema
    db: Session = Depends(get_db),
):
    # get_user_info_with_profile(token)

    match_type = match_data.match_type
    location = match_data.location
    match_time = match_data.match_time
    time_range = match_data.time_range
    skill = match_data.skill
    team_size = match_data.team_size
    gender = match_data.gender
    match_fee = match_data.match_fee
    notice = match_data.notice
    status = match_data.status
    guests = match_data.guests
    club_seq = match_data.club_seq

    query = db.query(Match)
    if match_type:
        query = query.filter(Match.match_type == match_type)
    if location:
        query = query.filter(Match.location == location)
    if skill:
        query = query.filter(Match.skill == skill)
    if team_size:
        query = query.filter(Match.team_size == team_size)
    if gender:
        query = query.filter(Match.gender == gender)

    if time_range:
        start_hour, end_hour = get_time_range(time_range)
        # 종료 시간 조정
        end_hour = end_hour if end_hour < 24 else 23
        query = query.filter(
            extract("hour", Match.match_time).between(start_hour, end_hour)
        )

    matches = query.all()
    return matches


@match_router.get("/{match_id}")
def get_match(
    # token: Annotated[str, Depends(get_current_user)],
    match_id: int,
    db: Session = Depends(get_db),
):
    # get_user_info_with_profile(token)

    match = db.query(Match).filter(Match.seq == match_id).first()
    if match is None:
        raise MatchNotFoundException
    return match


@match_router.post("")
def create_match(
    # token: Annotated[str, Depends(get_current_user)],
    match_data: MatchRegisterSchema,
    db: Session = Depends(get_db),
):
    # get_user_info_with_profile(token)

    con.register_match(match_data, db)
    return {"success": True}


@match_router.patch("/{match_id}")
def edit_match(
    # token: Annotated[str, Depends(get_current_user)],
    match_id: int,
    match_data: MatchUpdateSchema,
    db: Session = Depends(get_db),
):
    # get_user_info_with_profile(token)

    match = db.query(Match).filter(Match.seq == match_id).first()
    if not match:
        raise MatchNotFoundException

    for key, value in match_data.dict(exclude_unset=True).items():
        setattr(match, key, value)

    # 데이터베이스 커밋
    db.commit()
    return {"success": True}


@match_router.delete("/{match_id}")
def delete_match(
    # token: Annotated[str, Depends(get_current_user)],
    match_id: int,
    db: Session = Depends(get_db),
):
    # get_user_info_with_profile(token)

    match = db.query(Match).filter(Match.seq == match_id).first()
    if not match:
        raise MatchNotFoundException

    db.delete(match)
    db.commit()
    return {"message": "매치게시글이 성공적으로 삭제되었습니다."}
