from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class GuestListSchema(BaseModel):
    position: Optional[List[int]] = Field(None, title="포지션")
    skill: Optional[str] = Field(None, title="레벨")


class GuestRegisterSchema(BaseModel):
    club: int = Field(title="클럽id")
    match: int = Field(title="매치id")
    position: List[int] = Field(title="포지션")
    skill: str = Field(title="레벨")
    guest_number: int = Field(title="모집인원")
    match_fee: int = Field(title="매치비용")
    status: str = Field(title="용병상태")
    notice: str = Field(title="공지사항")


class GuestUpdateSchema(BaseModel):
    club: Optional[int] = None
    match: Optional[int] = None
    position: Optional[List[int]] = None
    skill: Optional[str] = None
    guest_number: Optional[int] = None
    match_fee: Optional[int] = None
    status: Optional[str] = None
    notice: Optional[str] = None
