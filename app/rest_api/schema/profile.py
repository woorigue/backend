from datetime import date
from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    StrictBool,
    StrictStr,
    conint,
    model_validator,
)

from .position import JoinPositionSchema


class UpdateProfileSchema(BaseModel):
    is_active: StrictBool = Field(title="활동 여부", default=True)
    nickname: StrictStr = Field(title="닉네임")
    gender: Literal["M", "F", "U"] = Field(title="성별", default=None)
    location: str = Field(title="활동 장소", default=None)
    birth_date: date = Field(title="연령대", default=None)
    foot: Literal["R", "L", "B"] = Field(title="주발", default=None)
    level: conint(ge=0, le=4) = Field(title="레벨", default=None)
    positions: list[conint(ge=1, le=15)] = Field(title="포지션")

    class Config:
        orm_mode = True
        from_attributes = True


class GetProfileSchema(BaseModel):
    nickname: StrictStr = Field(title="닉네임", default=None)
    gender: str | None = Field(title="성별", default=None)
    location: str | None = Field(title="활동 장소", default=None)
    age: str | None = Field(title="연령대", default=None)
    foot: str | None = Field(title="주발", default=None)
    level: int | None = Field(title="레벨", default=None)
    join_position: list[JoinPositionSchema] = []
    img: str | None = Field(title="이미지 URL", default=None)

    @model_validator(mode="after")
    def representation_fields(self):
        gender_map = {"F": "여성", "M": "남성"}
        self.gender = gender_map.get(self.gender)
        return self

    class Config:
        orm_mode = True
        from_attributes = True
