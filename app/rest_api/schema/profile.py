from typing import List, Optional

from pydantic import BaseModel, Field, StrictInt, StrictStr

from .position import JoinPositionSchema


class ProfileSchema(BaseModel):
    nickname: StrictStr = Field(title="닉네임", default=None)
    position: List[StrictInt] = None


class GetProfileSchema(BaseModel):
    nickname: StrictStr = Field(title="닉네임", default=None)
    join_profile: List[JoinPositionSchema] = []
