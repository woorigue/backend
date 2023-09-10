from pydantic import BaseModel, ConfigDict, Field

from .profile import GetProfileSchema


class EmailLoginSchema(BaseModel):
    email: str = Field(title="이메일")
    password: str = Field(title="패스워드")


class EmailRegisterSchema(BaseModel):
    email: str = Field(title="이메일")
    password: str = Field(title="패스워드")


class ResetPasswordSchema(BaseModel):
    email: str = Field(title="이메일")
    password: str = Field(title="패스워드")


class UserSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    seq: int = Field(title="시퀀스")
    email: str = Field(title="이메일")
    is_active: bool = Field(title="계정 활성 여부")
    profile: GetProfileSchema
