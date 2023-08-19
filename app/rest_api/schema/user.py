from pydantic import BaseModel, Field


class EmailLoginSchema(BaseModel):
    email: str = Field(title="이메일")
    password: str = Field(title="패스워드")


class EmailRegisterSchema(BaseModel):
    email: str = Field(title="이메일")
    password: str = Field(title="패스워드")
