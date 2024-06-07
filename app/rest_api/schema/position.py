from pydantic import BaseModel, Field


class PositionSchema(BaseModel):
    seq: int = Field(title="시퀀스")
    name: str = Field(title="이름")

    class Config:
        orm_mode = True
        from_attributes = True


class JoinPositionSchema(BaseModel):
    position: PositionSchema

    class Config:
        orm_mode = True
        from_attributes = True
