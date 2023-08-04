import random
import sys
from typing import Iterator

import pytest
from sqlalchemy.orm import Session
from app.use_cases.product import ProductUseCases
from app.schemas.product import ProductSchema
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

    db_session.delete(product_on_db)
    db_session.commit()


def test_add_product_category_non_existent(db_session: Session, product_schema_camisa: ProductSchema) -> None:
    uc_product = ProductUseCases(db_session)
    with pytest.raises(ValueError):
        uc_product.add(product_schema_camisa, category_slug='FOO')


def test_update_product(db_session: Session, products_on_db: list[ProductModel]):
    product = ProductSchema(
        name=products_on_db[0].name,
        slug=products_on_db[0].slug,
        price=9898,
        stock=123
    )
    uc_product = ProductUseCases(db_session)
    uc_product.update(products_on_db[0].id, product)
    new_product = db_session.query(ProductModel).filter_by(id=products_on_db[0].id).first()
    assert new_product is not None
    assert new_product.stock == product.stock
    assert new_product.price == product.price


def test_update_product_non_existent(db_session: Session):
    product = ProductSchema(
        name='foo',
        slug='bar',
        price=9,
        stock=1
    )
    uc_product = ProductUseCases(db_session)

    with pytest.raises(ValueError):
        uc_product.update(9999999, product)


def test_delete_product(
        db_session: Session,
        product_model_camisa: ProductModel,
        category_roupa_on_db: CategoryModel
) -> None:
    product_model_camisa.category_id = category_roupa_on_db.id
    db_session.add(product_model_camisa)
    db_session.commit()
    db_session.refresh(product_model_camisa)
    uc_product = ProductUseCases(db_session)
    uc_product.delete(product_model_camisa.id)
    db_session.expire_all()
    product_on_db = db_session.query(ProductModel).filter_by(id=product_model_camisa.id).first()
    try:
        assert product_on_db is None
    except AssertionError:
        db_session.delete(product_model_camisa)


def test_delete_product_non_existent(db_session: Session, product_model_camisa: ProductModel) -> None:
    uc_product = ProductUseCases(db_session)
    with pytest.raises(ValueError):
        uc_product.delete(product_model_camisa.id)


# def test_list_products(db_session: Session, products_on_db: Iterator[ProductModel]) -> None:
#     uc_product = ProductUseCases(db_session)
#     products = uc_product.list_products()
#
#     assert products_on_db[0].name == products[0].name
#     assert products_on_db[0].id == products[0].id
#     assert products_on_db[0].price == products[0].price
#     assert products_on_db[0].category_id == products[0].category_id
#
#     assert products_on_db[1].name == products[1].name
#     assert products_on_db[1].id == products[1].id
#     assert products_on_db[1].price == products[1].price
#     assert products_on_db[1].category_id == products[1].category_id
