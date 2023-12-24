from typing import List, Optional, Union
from app.model.club import Club

from fastapi import Query
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field, StrictInt, StrictStr, StrictBool

from datetime import date


class UpdateClubSchema(BaseModel):
    edit_date: date = Field(title="수정일")
    location: StrictStr = Field(title="활동 장소", default=None)
    age_group: StrictStr = Field(title="연령대", default=None)
    membership_fee: StrictInt = Field(title="회비", default=None)
    skill: StrictStr = Field(title="실력", default=None)
    img: StrictStr = Field(title="클럽 이미지 URL", default=None)
    uniform_color: StrictStr = Field(title="유니폼 색", default=None)
    deleted: StrictBool = Field(title="팀 삭제", default=False)


class ClubSchema(BaseModel):
    name: StrictStr = Field(title="이름")
    register_date: date = Field(title="창단일")
    location: StrictStr = Field(title="활동 장소")
    age_group: StrictStr = Field(title="연령대")
    membership_fee: StrictInt = Field(title="회비", default=0)
    skill: StrictStr = Field(title="실력")
    img: Union[StrictStr, None] = Field(title="클럽 이미지 URL", default=None)
    uniform_color: Union[StrictStr, None] = Field(title="유니폼 색", default=None)


class JoinClubSchema(BaseModel):
    club: ClubSchema


class FilterClubSchema(Filter):
    seq__in: Optional[List[int]] = Query(None, title="시퀸스 리스트")
    name__ilike: Optional[str] = Query(None, title="이름")
    location__in: Optional[List[str]] = Query(None, title="장소 리스트")
    age_group__in: Optional[List[str]] = Query(None, title="연령대 리스트")
    skill__in: Optional[List[str]] = Query(None, title="실력 리스트")
    membership_fee__lt: Optional[int] = Query(None, title="최소 회비")
    membership_fee__gt: Optional[int] = Query(None, title="최대 회비")

    class Constants(Filter.Constants):
        model = Club
