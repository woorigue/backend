import datetime
from datetime import date
from typing import Literal

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict, Field, conint

from app.model.club import Club
from app.rest_api.schema.profile import GetProfileSchema


class ClubSchema(BaseModel):
    name: str = Field(title="이름")
    register_date: date = Field(title="창단일")
    intro: str = Field(title="소개글")
    location: str = Field(title="활동 장소")
    age_group: str = Field(title="연령대")
    membership_fee: int = Field(0, title="회비")
    level: conint(ge=1, le=5) = Field(title="레벨")
    gender: Literal["M", "F", "U"] = Field(title="성별")
    uniform_color: str | None = Field(None, title="유니폼 색")


class UpdateClubSchema(BaseModel):
    edit_date: date = Field(title="수정일")
    intro: str = Field(None, title="소개글")
    location: str = Field(None, title="활동 장소")
    age_group: str = Field(None, title="연령대")
    membership_fee: int = Field(None, title="회비")
    level: conint(ge=1, le=5) = Field(None, title="실력")
    gender: Literal["M", "F", "U"] = Field(None, title="성별")
    img: str = Field(None, title="클럽 이미지 URL")
    uniform_color: str = Field(None, title="유니폼 색")
    deleted: bool = Field(False, title="팀 삭제")


class FilterClubSchema(Filter):
    seq__in: list[int] | None = Field(None, title="시퀸스 리스트")
    name__ilike: str | None = Field(None, title="이름")
    location__in: list[str] | None = Field(None, title="장소 리스트")
    age_group__in: list[str] | None = Field(None, title="연령대 리스트")
    level__in: list[int] | None = Field(None, title="실력 리스트")
    gender__in: list[Literal["M", "F", "U"]] | None = Field(None, title="성별")
    membership_fee__lte: int | None = Field(None, title="최대 회비")
    membership_fee__gte: int | None = Field(None, title="최소 회비")

    class Constants(Filter.Constants):
        model = Club


class ClubResponseSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    seq: int = Field(title="클럽 시퀸스")
    name: str = Field(title="이름")
    register_date: datetime = Field(title="창단일")
    intro: str | None = Field(title="소개글")
    location: str = Field(title="활동 장소")
    age_group: str = Field(title="연령대")
    membership_fee: int = Field(title="회비")
    level: int = Field(title="레벨")
    gender: Literal["M", "F", "U"] | None = Field(title="성별")
    emblem_img: str | None = Field(None, title="클럽 엠블럼 URL")
    img: str | None = Field(None, title="클럽 이미지 URL")
    uniform_color: str | None = Field(None, title="유니폼 색")
    roles: dict = Field(title="클럽 소유주들")
    team_size: int = Field(title="가입된 멤버 수")


class ClubUserDetailSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    seq: int = Field(title="클럽 시퀸스")
    name: str = Field(title="이름")
    register_date: datetime = Field(title="창단일")
    intro: str | None = Field(title="소개글")
    location: str = Field(title="활동 장소")
    age_group: str = Field(title="연령대")
    membership_fee: int = Field(title="회비")
    level: int = Field(title="레벨")
    team_size: int | None = Field(title="클럽 인원")
    gender: Literal["M", "F", "U"] | None = Field(title="성별")
    emblem_img: str | None = Field(None, title="클럽 엠블럼 URL")
    img: str | None = Field(None, title="클럽 이미지 URL")
    uniform_color: str | None = Field(None, title="유니폼 색")


class ClubListSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    seq: int = Field(title="클럽 시퀸스")
    name: str = Field(title="이름")
    register_date: datetime = Field(title="창단일")
    intro: str | None = Field(title="소개글")
    location: str = Field(title="활동 장소")
    age_group: str = Field(title="연령대")
    membership_fee: int = Field(title="회비")
    level: int = Field(title="레벨")
    team_size: int | None = Field(title="클럽 인원")
    gender: Literal["M", "F", "U"] | None = Field(title="성별")
    emblem_img: str | None = Field(None, title="클럽 엠블럼 URL")
    img: str | None = Field(None, title="클럽 이미지 URL")
    uniform_color: str | None = Field(None, title="유니폼 색")


class JoinClubSchema(BaseModel):
    club: ClubResponseSchema


class GetClubMemberSchema(BaseModel):
    profile: GetProfileSchema
    role: str | None = Field(title="역할", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
