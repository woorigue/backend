from datetime import date, datetime

from pydantic import BaseModel


class CreatePollSchema(BaseModel):
    match_seq: int
    club_seq: int
    expired_at: datetime = None


class RetrievePollSchema(BaseModel):
    seq: int
    match_seq: int
    user_seq: int
    expired_at: date | None
    vote_closed: bool | None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UpdatePollSchema(BaseModel):
    expired_at: date | None = None
    vote_closed: bool | None = None

    class Config:
        orm_mode = True
