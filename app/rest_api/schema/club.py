from typing import List

from pydantic import BaseModel, Field, StrictInt, StrictStr

from datetime import date


class UpdateClubSchema(BaseModel):
    seq: int = Field(title="시퀀스", default=None)
    name: str = Field(title="이름", default=None)
    location: str = Field(title="활동 장소", default=None)
    age_group: str = Field(title="연령대", default=None)
    membership_fee: int = Field(title="회비", default=None)
    skill: str = Field(title="실력", default=None)
    img: str = Field(title="클럽 이미지 URL", default=None)
    color: str = Field(title="유니폼 색", default=None)


class ClubSchema(BaseModel):
    name: str = Field(title="이름", default=None)
    register_date: date = Field(title="창단일", default=None)
    location: str = Field(title="활동 장소", default=None)
    age_group: str = Field(title="연령대", default=None)
    membership_fee: int = Field(title="회비", default=None)
    skill: str = Field(title="실력", default=None)
    img: str = Field(title="클럽 이미지 URL", default=None)
    color: str = Field(title="유니폼 색", default=None)


class DeleteClubSchema(BaseModel):
    seq: int = Field(title="스퀀스")


class JoinClubSchema(BaseModel):
    club: ClubSchema
