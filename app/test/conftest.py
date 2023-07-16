from typing import Any, Iterator

import pytest
from sqlalchemy.orm import Session as sqlalchemy_session

from app.schemas.category import CategorySchema
from app.schemas.product import ProductSchema
from app.db.models import CategoryModel, ProductModel
from app.db.connection import Session

@pytest.fixture()
def db_session() -> Any:
    try:
        session = Session()
        yield session
    finally:
        session.close()

@pytest.fixture()
def category_schema_roupa() -> CategorySchema:
    return CategorySchema(
        name='Roupa',
        slug='roupa'
    )


@pytest.fixture()
def category_roupa() -> CategoryModel:
    return CategoryModel(
        name='Roupa',
        slug='roupa'
    )

@pytest.fixture()
def category_calcado() -> CategoryModel:
    return CategoryModel(
        name='Calçado',
        slug='calcado'
    )


@pytest.fixture()
def category_infantil() -> CategoryModel:
    return CategoryModel(
        name='Infantil',
        slug='infantil'
    )


@pytest.fixture()
def body_roupa() -> dict[str, Any]:
    return {
        'name': 'Roupa',
        'slug': 'roupa'
    }

@pytest.fixture()
def categories_list(
        category_roupa: CategoryModel,
        category_calcado: CategoryModel,
        category_infantil: CategoryModel
) -> list[CategoryModel]:
    return [
        category_roupa,
        category_calcado,
        category_infantil
    ]

@pytest.fixture()
def categories_on_db(
        db_session: sqlalchemy_session,
        categories_list: list[CategoryModel]
):
    for category in categories_list:
        db_session.add(category)

    db_session.commit()

    for category in categories_list:
        db_session.refresh(category)

    yield categories_list

    for category in categories_list:
        db_session.delete(category)
    db_session.commit()


@pytest.fixture()
def category_roupa_on_db(db_session, category_roupa: CategoryModel):
    db_session.add(category_roupa)
    db_session.commit()
    yield category_roupa
    db_session.delete(category_roupa)
    db_session.commit()

@pytest.fixture()
def product_json_camisa(categories_on_db: list[CategoryModel]) -> dict[str, Any]:
    return {
        'category_slug': categories_on_db[0].slug,
        'product': {
            'name': 'camisa nike',
            'slug': 'camisa_nike',
            'stock': 2,
            'price': 4
        }
    }
@pytest.fixture()
def product_schema_camisa() -> ProductSchema:
    return ProductSchema(
        name='Camisa Nike',
        slug='camisa-nike',
        stock=1,
        price=1.99
    )
@pytest.fixture()
def product_model_camisa() -> ProductModel:
    return ProductModel(
        name='Camisa Nike',
        slug='camisa-nike',
        stock=1,
        price=1.99
    )

@pytest.fixture()
def product_model_calcado() -> ProductModel:
    return ProductModel(
        name='Tênis Adidas',
        slug='tenis-adidas',
        stock=1,
        price=1.99
    )

@pytest.fixture()
def products_on_db(
        db_session: Session,
        product_model_camisa: ProductModel,
        product_model_calcado: ProductModel,
        categories_on_db: list[CategoryModel]
) -> Iterator[ProductModel]:
    product_model_camisa.category_id = categories_on_db[0].id
    product_model_calcado.category_id = categories_on_db[1].id

    products_list = [product_model_camisa, product_model_calcado]
    for product in products_list:
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

    yield products_list
    for product in products_list:
        db_session.delete(product)
        db_session.commit()
