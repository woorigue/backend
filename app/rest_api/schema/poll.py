from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional

from pydantic import Field


class CreatePollSchema(BaseModel):
    match_seq: int
    club_seq: int
    expired_at: Optional[date] = None


class RetrievePollSchema(BaseModel):
    seq: int
    match_seq: int
    user_seq: int
    expired_at: Optional[date]
    vote_closed: Optional[bool]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UpdatePollSchema(BaseModel):
    expired_at: Optional[date] = None
    vote_closed: Optional[bool] = None

    class Config:
        orm_mode = True
