from typing import List, Optional, Union
from app.model.memberPosting import MemberPosting

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field


class MemberPostingSchema(BaseModel):
    club_seq: int = Field(title="클럽 시퀸스")
    title: str = Field(title="제목")
    notice: str = Field(title="팀원 모집 소개글")
    status: bool = Field(True, title="상태")


class UpdateMemberPostingSchema(BaseModel):
    title: str = Field(None, title="제목")
    notice: str = Field(None, title="클럽 소개글")
    status: bool = Field(None, title="상태")


class JoinMemberPostingSchema(BaseModel):
    member_posting: MemberPostingSchema


class FilterMemberPostingSchema(Filter):
    seq__in: Optional[List[int]] = Field(None, title="시퀸스 리스트")
    user_seq__in: Optional[List[int]] = Field(None, title="유저 시퀸스 리스트")
    club_seq__in: Optional[List[int]] = Field(None, title="클럽 시퀸스 리스트")
    title__ilike: Optional[str] = Field(None, title="이름")
    status__isnull: Optional[bool] = Field(None, title="상태")

    class Constants(Filter.Constants):
        model = MemberPosting
