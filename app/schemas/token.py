from pydantic import BaseModel, Field


class TokenPayload(BaseModel):
    user_id: int = Field(serialization_alias='u', gt=0)
    expire_at: int = Field(serialization_alias='e', gt=0)
    not_before: int = Field(serialization_alias='u', gt=0)
