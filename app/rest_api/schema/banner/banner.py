from typing import List

from pydantic import BaseModel, Field


class BannerRegisterSchema(BaseModel):
    url: str = Field(title="주소")


class BannerDeleteSchema(BaseModel):
<<<<<<< HEAD:app/rest_api/schema/banner/banner.py
    seq: int = Field(title="아이디")
=======
    id: int = Field(title="아이디")
>>>>>>> 93a53a9 (feature: rabbitmq):app/rest_api/schema/banner.py
