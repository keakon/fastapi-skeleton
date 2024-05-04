from pydantic import BaseModel, Field


class Resp(BaseModel):
    code: int = Field(default=0, ge=0)
    msg: str | None = None
    data: dict | None = None
