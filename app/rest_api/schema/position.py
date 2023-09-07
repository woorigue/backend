from pydantic import BaseModel, Field


class PositionSchema(BaseModel):
    seq: int = Field(title="시퀀스")
    name: str = Field(title="이름")


class JoinPositionSchema(BaseModel):
    position: PositionSchema
