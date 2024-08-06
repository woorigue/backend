import datetime as dt
from typing import Literal

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict, Field, conint

from app.model.match import Match
from app.rest_api.schema.club.club import ClubResponseSchema


class MatchSchema(BaseModel):
    home_club_seq: int = Field(title="홈 클럽 시퀸스")
    match_type: Literal["public", "private"] = Field(None, title="매치유형")
    location: str = Field(title="매치장소")
    match_date: dt.date = Field(title="매치일")
    start_time: dt.time = Field(title="매치 시작 시간")
    end_time: dt.time = Field(title="매치 종료 시간")
    level: conint(ge=1, le=5) = Field(title="레벨")
    team_size: int = Field(title="매치인원")
    gender: Literal["M", "F", "U"] = Field(title="성별")
    match_fee: int = Field(title="매치비용")
    notice: str = Field(title="공지사항")
    latitude: str = Field(None, title="위도")
    longitude: str = Field(None, title="경도")


class UpdateMatchSchema(BaseModel):
    match_type: Literal["public", "private"] = Field(None, title="매치유형")
    location: str = Field(None, title="매치장소")
    match_date: dt.date = Field(None, title="매치일")
    start_time: dt.time = Field(None, title="매치 시작 시간")
    end_time: dt.time = Field(None, title="매치 종료 시간")
    level: conint(ge=1, le=5) = Field(None, title="레벨")
    team_size: int = Field(None, title="매치인원")
    gender: Literal["M", "F", "U"] = Field(None, title="성별")
    match_fee: int = Field(None, title="매치비용")
    notice: str = Field(None, title="공지사항")
    matched: bool = Field(None, title="매치 성사 여부")
    home_club_guest_seq: int = Field(None, title="홈 클럽 용병 게시글 시퀸스")
    away_club_guest_seq: int = Field(None, title="원정 클럽 용병 게시글 시퀸스")
    latitude: str = Field(None, title="위도")
    longitude: str = Field(None, title="경도")


class FilterMatchSchema(Filter):
    seq__in: list[int] | None = Field(None, title="시퀸스 리스트")
    user_seq__in: list[int] | None = Field(None, title="유저 시퀸스")
    home_club_seq__in: list[int] | None = Field(None, title="홈 클럽 시퀸스")
    away_club_seq__in: list[int] | None = Field(None, title="원정 클럽 시퀸스")
    match_type__in: list[str] | None = Field(None, title="매치 유형")
    location__ilike: str | None = Field(None, title="장소 리스트")
    match_date: dt.date | None = Field(None, title="매치 날짜")
    match_date__gte: dt.date | None = Field(None, title="최소 매치 날짜")
    match_date__lte: dt.date | None = Field(None, title="최대 매치 날짜")
    start_time__gte: dt.time | None = Field(None, title="최소 매치시간")
    end_time__lte: dt.time | None = Field(None, title="최대 매치시간")
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


class GuestSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    seq: int = Field(title="유저 시퀸스")
    date: dt.datetime = Field(title="유저 시퀸스")
    user_seq: int = Field(title="유저 시퀸스")
    club_seq: int = Field(title="클럽 시퀸스")
    level: int = Field(title="레벨")
    gender: str = Field(title="성별")
    position: list[int] = Field(title="포지션")
    match_fee: int = Field(title="매치비용")
    guest_number: int = Field(title="모집 인원")
    guest_accpeted_number: int | None = Field(title="수락 인원")
    notice: str = Field(title="공지사항")
    closed: bool = Field(title="공고 마감 여부")


class MatchResponseSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    seq: int = Field(title="시퀸스")
    date: dt.datetime = Field(title="게시일")
    user_seq: int = Field(title="유저 시퀸스")
    home_club: ClubResponseSchema = Field(title="클럽 정보")
    away_club: ClubResponseSchema | None = Field(title="클럽 정보")
    match_type: str = Field(title="매치유형")
    location: str = Field(title="매치장소")
    match_date: dt.date = Field(title="매치일")
    start_time: dt.time = Field(title="매치 시작 시간")
    end_time: dt.time = Field(title="매치 종료 시간")
    level: int = Field(title="레벨")
    team_size: int = Field(title="매치인원")
    gender: str = Field(title="성별")
    match_fee: int = Field(title="매치비용")
    notice: str = Field(title="공지사항")
    matched: bool = Field(title="매치 성사 여부")
    home_club_guest: GuestSchema | None = Field(title="용병 게시글 시퀸스")
    away_club_guest: GuestSchema | None = Field(title="용병 게시글 시퀸스")
    home_club_poll_seq: int = Field(title="홈 클럽 투표 시퀸스")
    away_club_poll_seq: int | None = Field(title="원정 클럽 투표 시퀸스")
    latitude: str = Field(None, title="위도")
    longitude: str = Field(None, title="경도")
