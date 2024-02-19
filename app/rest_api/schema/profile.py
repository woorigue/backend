from typing import List, Union

from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr

from .position import JoinPositionSchema


class UpdateProfileSchema(BaseModel):
    is_active: StrictBool = Field(title="활동 여부", default=True)
    nickname: StrictStr = Field(title="닉네임")
    gender: str = Field(title="성별", default=None)
    location: str = Field(title="활동 장소", default=None)
    age: str = Field(title="연령대", default=None)
    foot: str = Field(title="주발", default=None)
    level: int = Field(title="레벨", default=None)
    positions: List[StrictInt] = Field(title="포지션")


class GetProfileSchema(BaseModel):
    nickname: StrictStr = Field(title="닉네임", default=None)
    gender: Union[str, None] = Field(title="성별", default=None)
    location: Union[str, None] = Field(title="활동 장소", default=None)
    age: Union[str, None] = Field(title="연령대", default=None)
    foot: Union[str, None] = Field(title="주발", default=None)
    level: Union[int, None] = Field(title="레벨", default=None)
    join_position: List[JoinPositionSchema] = []
    img: Union[str, None] = Field(title="이미지 URL", default=None)
