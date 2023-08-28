from pydantic import BaseModel, Field


class EmailVerifySchema(BaseModel):
    email: str = Field(title="이메일")


class EmailAuthCodeSchema(BaseModel):
    email: str = Field(title="이메일")
    auth_number: str = Field(title="인증번호")


class EmailPasswordResetSchema(BaseModel):
    email: str = Field(title="이메일")
