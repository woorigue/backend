from typing import List

from pydantic import BaseModel, Field

class BannerRegisterSchema(BaseModel):
    url: str = Field(title="주소")
    
class BannerDeleteSchema(BaseModel):
    seq: int = Field(title="아이디")