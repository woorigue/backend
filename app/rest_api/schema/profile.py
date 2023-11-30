from typing import List

from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr

from .position import JoinPositionSchema


class UpdateProfileSchema(BaseModel):
    is_active: StrictBool = Field(title="활동 여부", default=True)
    nickname: StrictStr = Field(title="닉네임", default=None)
    position: List[StrictInt] = None


class GetProfileSchema(BaseModel):
    nickname: StrictStr = Field(title="닉네임", default=None)
    img: str = Field(title="이미지 URL", default=None)
    join_profile: List[JoinPositionSchema] = []
