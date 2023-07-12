import random
import sys

import pytest
from sqlalchemy.orm import Session
from app.use_cases.product import ProductUseCases
from app.use_cases.category import CategoryUseCases
from app.schemas.product import ProductSchema
from app.schemas.category import CategorySchema
from app.db.models import ProductModel, CategoryModel

def test_add_product(db_session: Session, product_schema_camisa: ProductSchema, category_roupa_on_db: CategoryModel):
    uc_product = ProductUseCases(db_session)
    uc_product.add(product_schema_camisa, category_slug=category_roupa_on_db.slug)
    product_on_db = db_session.query(ProductModel).first()
    assert product_on_db is not None
    assert product_on_db.name == product_schema_camisa.name
    assert product_on_db.slug == product_schema_camisa.slug
    assert product_on_db.stock == product_schema_camisa.stock
    assert product_on_db.price == product_schema_camisa.price


def test_add_product_category_non_existent(db_session: Session, product_schema_camisa: ProductSchema):
    uc_product = ProductUseCases(db_session)
    with pytest.raises(ValueError):
        uc_product.add(product_schema_camisa, category_slug='FOO')
