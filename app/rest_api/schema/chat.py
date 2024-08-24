from pydantic import BaseModel, Field


class CreateMatchChatSchema(BaseModel):
    contents: str = Field(title="채팅 내용")
