from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field

from app.model.memberPosting import MemberPosting


class MemberPostingSchema(BaseModel):
    title: str = Field(title="제목")
    notice: str = Field(title="팀원 모집 소개글")
    status: str = Field("recruit", title="상태")


class UpdateMemberPostingSchema(BaseModel):
    title: str = Field(None, title="제목")
    notice: str = Field(None, title="클럽 소개글")
    status: str = Field(None, title="상태")


class JoinMemberPostingSchema(BaseModel):
    member_posting: MemberPostingSchema


class FilterMemberPostingSchema(Filter):
    seq__in: list[int] | None = Field(None, title="시퀸스 리스트")
    user_seq__in: list[int] | None = Field(None, title="유저 시퀸스 리스트")
    title__ilike: str | None = Field(None, title="이름")
    status__isnull: str | None = Field(None, title="상태")

    class Constants(Filter.Constants):
        model = MemberPosting
