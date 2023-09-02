from pydantic import BaseModel, Field


class RefreshTokenSchema(BaseModel):
    refresh_token: str = Field(title="리프레시 토큰")
