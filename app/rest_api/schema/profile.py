from typing import List, Union

from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr

from .position import JoinPositionSchema


class UpdateProfileSchema(BaseModel):
    is_active: StrictBool = Field(title="활동 여부", default=True)
    nickname: StrictStr = Field(title="닉네임", default=None)
    gender: str = Field(title="성별", default="M")
    location: str = Field(title="활동 장소")
    age_group: str = Field(title="연령대")
    foot: str = Field(title="주발")
    position: List[StrictInt] = None


class GetProfileSchema(BaseModel):
    nickname: StrictStr = Field(title="닉네임", default=None)
    gender: str = Field(title="성별", default="M")
    location: str = Field(title="활동 장소")
    age_group: str = Field(title="연령대")
    foot: str = Field(title="주발")
    join_profile: List[JoinPositionSchema] = []
    img: Union[str, None] = Field(title="이미지 URL", default=None)
