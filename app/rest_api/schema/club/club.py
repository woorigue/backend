from datetime import date
from typing import List, Optional

from app.model.club import Club

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field


class ClubSchema(BaseModel):
    name: str = Field(title="이름")
    register_date: date = Field(title="창단일")
    location: str = Field(title="활동 장소")
    age_group: str = Field(title="연령대")
    membership_fee: int = Field(0, title="회비")
    skill: str = Field(title="실력")
    emblem_img: Optional[str] = Field(None, title="클럽 엠블럼 URL")
    img: Optional[str] = Field(None, title="클럽 이미지 URL")
    uniform_color: Optional[str] = Field(None, title="유니폼 색")


class UpdateClubSchema(BaseModel):
    edit_date: date = Field(title="수정일")
    location: str = Field(None, title="활동 장소")
    age_group: str = Field(None, title="연령대")
    membership_fee: int = Field(None, title="회비")
    skill: str = Field(None, title="실력")
    img: str = Field(None, title="클럽 이미지 URL")
    uniform_color: str = Field(None, title="유니폼 색")
    deleted: bool = Field(False, title="팀 삭제")


class JoinClubSchema(BaseModel):
    club: ClubSchema


class FilterClubSchema(Filter):
    seq__in: Optional[List[int]] = Field(None, title="시퀸스 리스트")
    name__ilike: Optional[str] = Field(None, title="이름")
    location__in: Optional[List[str]] = Field(None, title="장소 리스트")
    age_group__in: Optional[List[str]] = Field(None, title="연령대 리스트")
    skill__in: Optional[List[str]] = Field(None, title="실력 리스트")
    membership_fee__lte: Optional[int] = Field(None, title="최소 회비")
    membership_fee__gte: Optional[int] = Field(None, title="최대 회비")

    class Constants(Filter.Constants):
        model = Club
