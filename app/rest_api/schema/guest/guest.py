import datetime
from typing import Literal

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict, Field, conint

from app.model.guest import Guest


class GuestSchema(BaseModel):
    title: str = Field(title="제목")
    club_seq: int = Field(title="클럽 시퀸스")
    match_seq: int = Field(title="매치 시퀸스")
    level: conint(ge=1, le=5) = Field(title="레벨")
    gender: Literal["M", "F", "U"] = Field(title="성별")
    position: list[conint(ge=1, le=15)] = Field(title="포지션")
    match_fee: int = Field(title="매치비용")
    guest_number: int = Field(title="모집인원")
    notice: str = Field(title="공지사항")


class UpdateGuestSchema(BaseModel):
    title: str = Field(title="제목")
    club_seq: int = Field(None, title="클럽 시퀸스")
    match_seq: int = Field(None, title="매치 시퀸스")
    level: conint(ge=1, le=5) = Field(None, title="레벨")
    gender: Literal["M", "F", "U"] = Field(None, title="성별")
    position: list[conint(ge=1, le=15)] = Field(None, title="포지션")
    match_fee: int = Field(None, title="매치비용")
    guest_number: int = Field(None, title="모집인원")
    closed: str = Field(None, title="공고 마감 여부")
    notice: str = Field(None, title="공지사항")


class FilterGuestSchema(Filter):
    seq__in: list[int] | None = Field(None, title="시퀸스 리스트")
    user_seq__in: list[int] | None = Field(None, title="유저 시퀸스 리스트")
    club_seq__in: list[int] | None = Field(None, title="매치 시퀸스 리스트")
    match_seq__in: list[int] | None = Field(None, title="매치 시퀸스 리스트")
    level__in: list[int] | None = Field(None, title="실력 리스트")
    gender__in: list[Literal["M", "F", "U"]] | None = Field(None, title="성별")
    position__in: list[conint(ge=1, le=5)] = Field(None, title="포지션")
    closed: bool | None = Field(None, title="공고 마감 여부")

    class Constants(Filter.Constants):
        model = Guest


class JoinGuestSchema(BaseModel):
    guest: GuestSchema


class GuestResponseSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    seq: int = Field(title="유저 시퀸스")
    title: str = Field(title="제목")
    date: datetime = Field(title="유저 시퀸스")
    user_seq: int = Field(title="유저 시퀸스")
    club_seq: int = Field(title="클럽 시퀸스")
    match_seq: int = Field(title="매치 시퀸스")
    level: int = Field(title="레벨")
    gender: str = Field(title="성별")
    position: list[int] = Field(title="포지션")
    match_fee: int = Field(title="매치비용")
    guest_number: int = Field(title="모집인원")
    notice: str = Field(title="공지사항")
    closed: bool = Field(title="공고 마감 여부")
