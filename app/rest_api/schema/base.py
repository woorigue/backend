from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    success: bool = Field(default=True)


class CreateResponse(SuccessResponse):
    pass
