import pytest

from app.schemas.category import CategorySchema


def test_category_schema():
    category = CategorySchema(
        name='Roupa',
        slug='roupa'
    )

    assert category.model_dump() == {
        'name': 'Roupa',
        'slug': 'roupa'
    }

def test_category_schema_invalid_slug():
    with pytest.raises(ValueError):
        category = CategorySchema(
            name='Roupa',
            slug='roupa de cama'
        )