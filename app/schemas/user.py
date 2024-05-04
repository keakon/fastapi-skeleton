from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    name: str = Field(min_length=3)
    password: str = Field(min_length=3)
