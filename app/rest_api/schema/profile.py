from datetime import date, time, datetime
from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    StrictBool,
    StrictStr,
    conint,
)

from .position import JoinPositionSchema


class UpdateProfileSchema(BaseModel):
    is_active: StrictBool = Field(title="활동 여부", default=True)
    nickname: StrictStr = Field(title="닉네임")
    gender: Literal["M", "F", "U"] = Field(title="성별", default=None)
    location: str = Field(title="활동 장소", default=None)
    age: datetime = Field(title="나이", default=None)
    foot: Literal["R", "L", "B"] = Field(title="주발", default=None)
    level: conint(ge=1, le=5) = Field(title="레벨", default=None)
    positions: list[conint(ge=1, le=15)] = Field(title="포지션")

    class Config:
        orm_mode = True
        from_attributes = True


class GetProfileSchema(BaseModel):
    nickname: StrictStr = Field(title="닉네임", default=None)
    gender: str | None = Field(title="성별", default=None)
    location: str | None = Field(title="활동 장소", default=None)
    age: datetime | None = Field(title="나이", default=None)
    foot: str | None = Field(title="주발", default=None)
    level: int | None = Field(title="레벨", default=None)
    join_position: list[JoinPositionSchema] = []
    img: str | None = Field(title="이미지 URL", default=None)

    class Config:
        orm_mode = True
        from_attributes = True
