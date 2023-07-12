from pydantic import Field, field_validator
from app.schemas.base import CustomBaseModel

class ProductSchema(CustomBaseModel):
    name: str
    slug: str = Field(pattern='^([a-z]|-|_)+$', min_length=3, max_length=256)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
