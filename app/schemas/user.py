from datetime import datetime
from pydantic import Field
from app.schemas.base import CustomBaseSchema


class UserSchema(CustomBaseSchema):
    username: str = Field(pattern='^([a-z]|[A-Z]|[0-9]|-|_|@)+$')
    password: str


class TokenData(CustomBaseSchema):
    access_token: str
    expires_at: datetime