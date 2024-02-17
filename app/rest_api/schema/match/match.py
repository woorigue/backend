from datetime import datetime
from typing import List, Optional

from app.model.match import Match

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field


class MatchSchema(BaseModel):
    home_club_seq: int = Field(title="홈 클럽 시퀸스")
    match_type: str = Field(title="매치유형")
    location: str = Field(title="매치장소")
    match_time: datetime = Field(title="매치일정")
    skill: str = Field(title="레벨")
    team_size: int = Field(title="매치인원")
    gender: str = Field(title="성별")
    match_fee: int = Field(title="매치비용")
    notice: str = Field(title="공지사항")
    status: str = Field(title="매치상태")
    guest_seq: int = Field(title="용병 게시글 시퀸스")


class UpdateMatchSchema(BaseModel):
    away_club_seq: int = Field(title="원정 클럽 시퀸스")
    match_type: str = Field(None, title="매치유형")
    location: str = Field(None, title="매치장소")
    match_time: datetime = Field(None, title="매치일정")
    skill: str = Field(None, title="레벨")
    team_size: int = Field(None, title="매치인원")
    gender: str = Field(None, title="성별")
    match_fee: int = Field(None, title="매치비용")
    notice: str = Field(None, title="공지사항")
    status: str = Field(None, title="매치상태")
    guest_seq: int = Field(None, title="용병 게시글 시퀸스")


class FilterMatchSchema(Filter):
    seq__in: Optional[List[int]] = Field(None, title="시퀸스 리스트")
    user_seq__in: Optional[List[int]] = Field(None, title="유저 시퀸스")
    home_club_seq__in: Optional[List[int]] = Field(None, title="홈 클럽 시퀸스")
    away_club_seq__in: Optional[List[int]] = Field(None, title="원정 클럽 시퀸스")
    match_type: Optional[List[str]] = Field(None, title="매치 유형")
    location__in: Optional[List[str]] = Field(None, title="장소 리스트")
    match_time__gte: Optional[datetime] = Field(None, title="최소 매치시간")
    match_time__lte: Optional[datetime] = Field(None, title="최대 매치시간")
    skill__in: Optional[List[str]] = Field(None, title="실력 리스트")
    team_size__in: Optional[List[int]] = Field(None, title="매치인원")
    gender__in: Optional[List[str]] = Field(None, title="성별")
    match_fee__gte: Optional[int] = Field(None, title="최소 회비")
    match_fee__lte: Optional[int] = Field(None, title="최대 회비")
    status: Optional[str] = Field(None, title="매치상태")
    guest_seq__in: Optional[List[int]] = Field(None, title="용별 게시글 시퀸스")

    class Constants(Filter.Constants):
        model = Match


class JoinMatchSchema(BaseModel):
    match: MatchSchema
