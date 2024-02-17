from typing import List, Optional, Union
from app.model.clubPosting import ClubPosting

from fastapi import Query
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field


class ClubPostingSchema(BaseModel):
    club_seq: int = Field(title="클럽 시퀸스")
    title: str = Field(title="제목")
    notice: str = Field(title="클럽 소개글")
    recruitment_number: int = Field(title="모집 회원 수")
    location: str = Field(title="활동 장소")
    age_group: str = Field(title="연령대")
    membership_fee: int = Field(0, title="회비")
    skill: str = Field(title="실력")
    gender: str = Field(title="성별")
    status: bool = Field(True, title="상태")


class UpdateClubPostingSchema(BaseModel):
    title: str = Field(None, title="제목")
    notice: str = Field(None, title="클럽 소개글")
    recruitment_number: int = Field(None, title="모집 회원 수")
    location: str = Field(None, title="활동 장소")
    age_group: str = Field(None, title="연령대")
    membership_fee: int = Field(None, title="회비")
    skill: str = Field(None, title="실력")
    gender: str = Field(None, title="성별")
    status: bool = Field(None, title="상태")


class JoinClubPostingSchema(BaseModel):
    club_posting: ClubPostingSchema


class FilterClubPostingSchema(Filter):
    seq__in: Optional[List[int]] = Field(None, title="시퀸스 리스트")
    club_seq__in: Optional[List[int]] = Field(None, title="클럽 시퀸스 리스트")
    title__ilike: Optional[str] = Field(None, title="이름")
    location__in: Optional[List[str]] = Field(None, title="장소 리스트")
    age_group__in: Optional[List[str]] = Field(None, title="연령대 리스트")
    skill__in: Optional[List[str]] = Field(None, title="실력 리스트")
    membership_fee__lte: Optional[int] = Field(None, title="최소 회비")
    membership_fee__gte: Optional[int] = Field(None, title="최대 회비")
    recruitment_number__lte: Optional[int] = Field(None, title="최소 모집 회원 수")
    recruitment_number__gte: Optional[int] = Field(None, title="최대 모집 회원 수")
    gender__in: Optional[List[str]] = Field(None, title="성별 리스트")
    status__isnull: Optional[bool] = Field(None, title="상태")
    user_seq__in: Optional[List[int]] = Field(None, title="유저 시퀸스 리스트")

    class Constants(Filter.Constants):
        model = ClubPosting
