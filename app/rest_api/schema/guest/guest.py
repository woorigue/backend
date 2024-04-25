import datetime

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict, Field

from app.model.guest import Guest


class GuestSchema(BaseModel):
    club_seq: int = Field(title="클럽 시퀸스")
    match_seq: int = Field(title="매치 시퀸스")
    position: list[int] = Field(title="포지션")
    skill: str = Field(title="레벨")
    guest_number: int = Field(title="모집인원")
    match_fee: int = Field(title="매치비용")
    status: str = Field(title="용병상태")
    notice: str = Field(title="공지사항")


class UpdateGuestSchema(BaseModel):
    club_seq: int = Field(None, title="클럽 시퀸스")
    match_seq: int = Field(None, title="매치 시퀸스")
    position: list[int] = Field(None, title="포지션")
    skill: str = Field(None, title="레벨")
    guest_number: int = Field(None, title="모집인원")
    match_fee: int = Field(None, title="매치비용")
    status: str = Field(None, title="용병상태")
    notice: str = Field(None, title="공지사항")


class FilterGuestSchema(Filter):
    seq__in: list[int] | None = Field(None, title="시퀸스 리스트")
    user_seq__in: list[int] | None = Field(None, title="유저 시퀸스 리스트")
    club_seq__in: list[int] | None = Field(None, title="매치 시퀸스 리스트")
    match_seq__in: list[int] | None = Field(None, title="매치 시퀸스 리스트")
    # position: Optional[List[int]] = Field(None, title="포지션")
    skill__in: list[str] | None = Field(None, title="실력 리스트")
    status: str | None = Field(None, title="용병 상태")

    class Constants(Filter.Constants):
        model = Guest


class JoinGuestSchema(BaseModel):
    guest: GuestSchema


class GuestResponseSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    seq: int = Field(title="유저 시퀸스")
    date: datetime = Field(title="유저 시퀸스")
    user_seq: int = Field(title="유저 시퀸스")
    club_seq: int = Field(title="클럽 시퀸스")
    match_seq: int = Field(title="매치 시퀸스")
    position: list[int] = Field(title="포지션")
    skill: str = Field(title="레벨")
    guest_number: int = Field(title="모집인원")
    match_fee: int = Field(title="매치비용")
    status: str = Field(title="용병상태")
    notice: str = Field(title="공지사항")
