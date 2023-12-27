from typing import List
from pydantic import BaseModel, Field
from datetime import datetime 
from typing import Optional


class MatchListSchema(BaseModel):
    match_type: Optional[str] = Field(None, title="매치유형")
    location: Optional[str] = Field(None, title="매치장소")
    match_time: Optional[datetime] = Field(None, title="매치일정")
    time_range: Optional[str] = Field(None, title="매치시간필터")
    skill: Optional[str] = Field(None, title="레벨")
    team_size: Optional[int] = Field(None, title="매치인원")
    gender: Optional[str] = Field(None, title="성별")
    match_fee: Optional[int] = Field(None, title="매치비용")
    notice: Optional[str] = Field(None, title="공지사항")
    status: Optional[str] = Field(None, title="매치상태")
    guests: Optional[int] = Field(None, title="용병id")
    club_seq: Optional[int] = Field(None, title="클럽id")

class MatchRegisterSchema(BaseModel):
    match_type: str = Field(title="매치유형")
    location: str = Field(title="매치장소")
    match_time: datetime = Field(title="매치일정")
    skill: str = Field(title="레벨")
    team_size: int = Field(title="매치인원")
    gender: str = Field(title="성별")
    match_fee:int = Field(title="매치비용")
    notice:str = Field(title="공지사항")
    status:str = Field(title="매치상태")
    guests:int = Field(title="용병id")
    club_seq:int = Field(title="클럽id")
    
class MatchUpdateSchema(BaseModel):
    match_type: Optional[str] = None
    location: Optional[str] = None
    match_time: Optional[datetime] = None
    skill: Optional[str] = None
    team_size: Optional[int] = None
    gender: Optional[str] = None
    match_fee: Optional[int] = None
    notice: Optional[str] = None
    status: Optional[str] = None
    guests: Optional[int] = None
    club_seq: Optional[int] = None