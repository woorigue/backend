from datetime import date, time
from typing import Literal, List

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field, conint

from app.model.match import Match


class MatchSchema(BaseModel):
    home_club_seq: int = Field(title="홈 클럽 시퀸스")
    match_type: str = Field(title="매치유형")
    location: str = Field(title="매치장소")
    match_date: date = Field(title="매치일")
    start_time: time = Field(title="매치 시작 시간")
    end_time: time = Field(title="매치 종료 시간")
    level: conint(ge=0, le=4) = Field(title="레벨")
    team_size: int = Field(title="매치인원")
    gender: Literal["M", "F", "U"] = Field(title="성별")
    match_fee: int = Field(title="매치비용")
    notice: str = Field(title="공지사항")
    guest_seq: int = Field(title="용병 게시글 시퀸스")


class UpdateMatchSchema(BaseModel):
    match_type: str = Field(None, title="매치유형")
    location: str = Field(None, title="매치장소")
    match_date: date = Field(None, title="매치일")
    start_time: time = Field(None, title="매치 시작 시간")
    end_time: time = Field(None, title="매치 종료 시간")
    level: conint(ge=0, le=4) = Field(None, title="레벨")
    team_size: int = Field(None, title="매치인원")
    gender: Literal["M", "F", "U"] = Field(None, title="성별")
    match_fee: int = Field(None, title="매치비용")
    notice: str = Field(None, title="공지사항")
    status: str = Field(None, title="매치상태")
    guest_seq: int = Field(None, title="용병 게시글 시퀸스")


class FilterMatchSchema(Filter):
    seq__in: list[int] | None = Field(None, title="시퀸스 리스트")
    user_seq__in: list[int] | None = Field(None, title="유저 시퀸스")
    home_club_seq__in: list[int] | None = Field(None, title="홈 클럽 시퀸스")
    away_club_seq__in: list[int] | None = Field(None, title="원정 클럽 시퀸스")
    match_type: list[str] | None = Field(None, title="매치 유형")
    location__in: list[str] | None = Field(None, title="장소 리스트")
    match_date__gte: date | None = Field(None, title="최소 매치 날짜")
    match_date__lte: date | None = Field(None, title="최대 매치 날짜")
    start_time__gte: time | None = Field(None, title="최소 매치시간")
    end_time__lte: time | None = Field(None, title="최대 매치시간")
    level__in: list[int] | None = Field(None, title="실력 리스트")
    team_size__in: list[int] | None = Field(None, title="매치인원")
    gender__in: list[Literal["M", "F", "U"]] | None = Field(None, title="성별")
    match_fee__gte: int | None = Field(None, title="최소 회비")
    match_fee__lte: int | None = Field(None, title="최대 회비")
    status: str | None = Field(None, title="매치상태")
    guest_seq__in: list[int] | None = Field(None, title="용별 게시글 시퀸스")

    class Constants(Filter.Constants):
        model = Match


class JoinMatchSchema(BaseModel):
    match: MatchSchema
