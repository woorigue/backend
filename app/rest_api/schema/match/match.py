from datetime import date, datetime, time
from typing import Literal

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict, Field, conint

from app.model.match import Match
from app.rest_api.schema.club.club import ClubResponseSchema
from app.rest_api.schema.guest.guest import GuestResponseSchema


class MatchSchema(BaseModel):
    home_club_seq: int = Field(title="홈 클럽 시퀸스")
    match_type: Literal["public", "private"] = Field(None, title="매치유형")
    location: str = Field(title="매치장소")
    match_date: date = Field(title="매치일")
    start_time: time = Field(title="매치 시작 시간")
    end_time: time = Field(title="매치 종료 시간")
    level: conint(ge=1, le=5) = Field(title="레벨")
    team_size: int = Field(title="매치인원")
    gender: Literal["M", "F", "U"] = Field(title="성별")
    match_fee: int = Field(title="매치비용")
    notice: str = Field(title="공지사항")


class UpdateMatchSchema(BaseModel):
    match_type: Literal["public", "private"] = Field(None, title="매치유형")
    location: str = Field(None, title="매치장소")
    match_date: date = Field(None, title="매치일")
    start_time: time = Field(None, title="매치 시작 시간")
    end_time: time = Field(None, title="매치 종료 시간")
    level: conint(ge=1, le=5) = Field(None, title="레벨")
    team_size: int = Field(None, title="매치인원")
    gender: Literal["M", "F", "U"] = Field(None, title="성별")
    match_fee: int = Field(None, title="매치비용")
    notice: str = Field(None, title="공지사항")
    matched: bool = Field(None, title="매치 성사 여부")
    home_club_guest_seq: int = Field(None, title="홈 클럽 용병 게시글 시퀸스")
    away_club_guest_seq: int = Field(None, title="원정 클럽 용병 게시글 시퀸스")


class FilterMatchSchema(Filter):
    seq__in: list[int] | None = Field(None, title="시퀸스 리스트")
    user_seq__in: list[int] | None = Field(None, title="유저 시퀸스")
    home_club_seq__in: list[int] | None = Field(None, title="홈 클럽 시퀸스")
    away_club_seq__in: list[int] | None = Field(None, title="원정 클럽 시퀸스")
    match_type__in: list[str] | None = Field(None, title="매치 유형")
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
    home_club_guest_seq__in: list[int] | None = Field(None, title="홈 클럽 용별 게시글 시퀸스")
    away_club_guest_seq__in: list[int] | None = Field(None, title="원정 클럽용별 게시글 시퀸스")

    class Constants(Filter.Constants):
        model = Match


class JoinMatchSchema(BaseModel):
    match: MatchSchema


class MatchResponseSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    seq: int = Field(title="시퀸스")
    date: datetime = Field(title="게시일")
    user_seq: int = Field(title="유저 시퀸스")
    home_club: ClubResponseSchema = Field(title="클럽 정보")
    away_club: ClubResponseSchema | None = Field(title="클럽 정보")
    match_type: str = Field(title="매치유형")
    location: str = Field(title="매치장소")
    match_date: date = Field(title="매치일")
    start_time: time = Field(title="매치 시작 시간")
    end_time: time = Field(title="매치 종료 시간")
    level: int = Field(title="레벨")
    team_size: int = Field(title="매치인원")
    gender: str = Field(title="성별")
    match_fee: int = Field(title="매치비용")
    notice: str = Field(title="공지사항")
    matched: bool = Field(title="매치 성사 여부")
    home_club_guest: GuestResponseSchema | None = Field(title="용병 게시글 시퀸스")
    away_club_guest: GuestResponseSchema | None = Field(title="용병 게시글 시퀸스")
    home_club_poll_seq: int = Field(title="홈 클럽 투표 시퀸스")
    away_club_poll_seq: int | None = Field(title="원정 클럽 투표 시퀸스")
