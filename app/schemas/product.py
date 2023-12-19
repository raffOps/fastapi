from pydantic import Field

from app.schemas.base import CustomBaseSchema
from app.schemas.category import CategoryOutputSchema


class ProductSchema(CustomBaseSchema):
    name: str
    slug: str = Field(pattern='^([a-z]|-|_)+$', min_length=3, max_length=256)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class ProductOutputSchema(ProductSchema):
    id: int
    category: CategoryOutputSchema
