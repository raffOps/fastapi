from typing import Any

import pytest
from sqlalchemy.orm import Session as sqlalchemy_session

from app.schemas.category import CategorySchema
from app.schemas.product import ProductSchema
from app.db.models import CategoryModel
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
    db_session.refresh(category_roupa)
    yield category_roupa
    db_session.delete(category_roupa)
    db_session.commit()

@pytest.fixture()
def product_schema_camisa():
    return ProductSchema(
        name='Camisa Nike',
        slug='camisa-nike',
        stock=1,
        price=1.99
    )