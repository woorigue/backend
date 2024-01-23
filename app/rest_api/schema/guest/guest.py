from typing import Optional, List

from app.model.guest import Guest

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field


class GuestSchema(BaseModel):
    club_seq: int = Field(title="클럽 시퀸스")
    match_seq: int = Field(title="매치 시퀸스")
    position: List[int] = Field(title="포지션")
    skill: str = Field(title="레벨")
    guest_number: int = Field(title="모집인원")
    match_fee: int = Field(title="매치비용")
    status: str = Field(title="용병상태")
    notice: str = Field(title="공지사항")


class UpdateGuestSchema(BaseModel):
    club_seq: int = Field(None, title="클럽 시퀸스")
    match_seq: int = Field(None, title="매치 시퀸스")
    position: List[int] = Field(None, title="포지션")
    skill: str = Field(None, title="레벨")
    guest_number: int = Field(None, title="모집인원")
    match_fee: int = Field(None, title="매치비용")
    status: str = Field(None, title="용병상태")
    notice: str = Field(None, title="공지사항")


class FilterGuestSchema(Filter):
    seq__in: Optional[List[int]] = Field(None, title="시퀸스 리스트")
    match__in: Optional[List[int]] = Field(None, title="매치 시퀸스 리스트")
    position__in: Optional[List[int]] = Field(None, title="포지션")
    skill__in: Optional[List[str]] = Field(None, title="실력 리스트")
    status: Optional[str] = Field(None, title="용병 상태")

    class Constants(Filter.Constants):
        model = Guest
