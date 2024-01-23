from typing import List

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr

from .profile import GetProfileSchema
from .club.club import JoinClubSchema


class EmailLoginSchema(BaseModel):
    email: str = Field(title="이메일")
    password: str = Field(title="패스워드")


class EmailRegisterSchema(BaseModel):
    email: str = Field(title="이메일")
    password: str = Field(title="패스워드")


class ResetPasswordSchema(BaseModel):
    email: str = Field(title="이메일")
    password: str = Field(title="패스워드")


class UserSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    seq: int = Field(title="시퀀스")
    email: str = Field(title="이메일")
    is_active: bool = Field(title="계정 활성 여부")
    profile: List[GetProfileSchema]
    join_club: List[JoinClubSchema] = []


class JoinClubSchema(BaseModel):
    role: StrictStr = Field(title="클럽 시퀸스")


class QuitClubSchema(BaseModel):
    club_seq: StrictInt = Field(title="클럽 시퀸스")
