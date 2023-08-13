from pydantic import field_validator, Field

from app.schemas.base import CustomBaseSchema


class CategorySchema(CustomBaseSchema):
    name: str
    slug: str = Field(pattern='^([a-z]|-|_)+$', min_length=3, max_length=256)


class CategoryOutputSchema(CategorySchema):
    id: int
