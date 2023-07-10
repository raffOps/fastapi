import re
from pydantic import field_validator

#from app.schemas.base import CustomBaseModel
from pydantic import BaseModel


class CategorySchema(BaseModel):
    name: str
    slug: str

    @field_validator('slug')
    def validate_slug(cls, slug: str) -> str:
        if not re.match('^([a-z]|-|_)+$', slug):
            raise ValueError(f'Invalid slug: {slug}')
        return slug

class CategoryOutputSchema(CategorySchema):
    id: int
