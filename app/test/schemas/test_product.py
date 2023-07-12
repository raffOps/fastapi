import pytest
from pydantic import ValidationError

from app.schemas.product import ProductSchema


def test_product_schema():
    product = ProductSchema(
        name='Camisa Nike',
        slug='camisa-nike',
        price=22.99,
        stock=3
    )
    assert product.model_dump() == {
        'name': 'Camisa Nike',
        'slug': 'camisa-nike',
        'price': 22.99,
        'stock': 3
    }


def test_product_schema_invalid_slug():
    with pytest.raises(ValueError):
        product = ProductSchema(
            name='Camisa Nike',
            slug='camisa-nikE',
            price=22.99,
            stock=3
        )


def test_product_schema_invalid_stock():
    with pytest.raises(ValidationError):
        product = ProductSchema(
            name='Camisa Nike',
            slug='camisa-nikE',
            price=22.99,
            stock=-3
        )
    with pytest.raises(ValueError):
        product = ProductSchema(
            name='Camisa Nike',
            slug='camisa-nikE',
            price=22.99,
            stock='3,0'
        )

def test_product_schema_invalid_price():
    with pytest.raises(ValueError):
        product = ProductSchema(
            name='Camisa Nike',
            slug='camisa-nikE',
            price='22,9',
            stock=1
        )


    with pytest.raises(ValidationError):
        product = ProductSchema(
            name='Camisa Nike',
            slug='camisa-nikE',
            price=-22,
            stock=1
        )
