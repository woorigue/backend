from typing import List, Optional

from pydantic import BaseModel, Field


class FaqDeleteSchema(BaseModel):
    id: int = Field(title="아이디")


class FaqCreateSchema(BaseModel):
    title: str = Field(title="제목")
    body: str = Field(title="본문")


class FaqGetSchema(BaseModel):
    title: str = Field(title="제목")
    body: str = Field(title="본문")


class FaqEditSchema(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
