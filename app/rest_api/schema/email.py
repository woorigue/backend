from pydantic import BaseModel, Field


class EmailVerifySchema(BaseModel):
    email: str = Field(title="이메일")
