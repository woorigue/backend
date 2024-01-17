from pydantic import BaseModel, Field


class CreateMatchChatRoomSchema(BaseModel):
    match_id: int = Field(title="match 아이디")


class CreateMatchChatSchema(BaseModel):
    contents: str = Field(title="채팅 내용")
