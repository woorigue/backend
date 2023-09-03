from pydantic import BaseModel, Field


class ProfileSchema(BaseModel):
    nickname: str = Field(title="닉네임")
