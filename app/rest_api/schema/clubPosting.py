from typing import List, Optional, Union
from app.model.clubPosting import ClubPosting

from fastapi import Query
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field, StrictInt, StrictStr, StrictBool


class ClubPostingSchema(BaseModel):
    club_seq: StrictInt = Field(title="클럽 시퀸스")
    title: StrictStr = Field(title="제목")
    intro: StrictStr = Field(title="클럽 소개글")
    recruitment_number: StrictInt = Field(title="모집 회원 수")
    location: StrictStr = Field(title="활동 장소")
    age_group: StrictStr = Field(title="연령대")
    membership_fee: StrictInt = Field(title="회비", default=0)
    skill: StrictStr = Field(title="실력")
    gender: StrictStr = Field(title="성별")
    status: StrictBool = Field(title="상태", default=True)


class UpdateClubPostingSchema(BaseModel):
    title: StrictStr = Field(title="제목")
    intro: StrictStr = Field(title="클럽 소개글")
    recruitment_number: StrictInt = Field(title="모집 회원 수")
    location: StrictStr = Field(title="활동 장소")
    age_group: StrictStr = Field(title="연령대")
    membership_fee: StrictInt = Field(title="회비", default=0)
    skill: StrictStr = Field(title="실력")
    gender: StrictStr = Field(title="성별")
    status: StrictBool = Field(title="상태", default=True)


class JoinClubPostingSchema(BaseModel):
    club: ClubPostingSchema


class FilterClubPostingSchema(Filter):
    seq__in: Optional[List[int]] = Query(None, title="시퀸스 리스트")
    club_seq__in: Optional[List[int]] = Query(None, title="클럽 시퀸스 리스트")
    title__ilike: Optional[str] = Query(None, title="이름")
    location__in: Optional[List[str]] = Query(None, title="장소 리스트")
    age_group__in: Optional[List[str]] = Query(None, title="연령대 리스트")
    skill__in: Optional[List[str]] = Query(None, title="실력 리스트")
    membership_fee__lt: Optional[int] = Query(None, title="최소 회비")
    membership_fee__gt: Optional[int] = Query(None, title="최대 회비")
    recruitment_number__lt: Optional[int] = Query(None, title="최소 모집 회원 수")
    recruitment_number__gt: Optional[int] = Query(None, title="최대 모집 회원 수")
    gender__in: Optional[List[str]] = Query(None, title="성별 리스트")
    status__isnull: Optional[bool] = Query(None, title="상태")
    user_seq__in: Optional[List[int]] = Query(None, title="유저 시퀸스 리스트")

    class Constants(Filter.Constants):
        model = ClubPosting
