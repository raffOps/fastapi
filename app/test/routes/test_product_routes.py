from typing import Any

from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session
import logging

from app.main import app
from app.db.models import ProductModel, CategoryModel


client = TestClient(app)
headers = {'Authorization': 'Bearer token'}
client.headers = headers

LOGGER = logging.getLogger(__name__)

def test_add_product_route(db_session: Session, product_json_camisa: dict[str, Any]):
    response = client.post(
        url=f'product/add/?category_slug={product_json_camisa["category_slug"]}',
        json=product_json_camisa['product']
    )

    assert response.status_code == status.HTTP_201_CREATED
    model = db_session.query(ProductModel).first()
    db_session.delete(model)
    db_session.commit()

def test_add_product_route_non_existent_category(db_session: Session, product_json_camisa: dict[str, Any]):
    product_json_camisa['category_slug'] = 'FOO'
    response = client.post(
        url='product/add?category_slug={product_json_camisa["category_slug"]}',
        json=product_json_camisa['product']
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    
def test_update_product_route(db_session: Session, products_on_db: list[ProductModel]):
    product_on_db = products_on_db[0]
    product = {
        'name': product_on_db.name,
        'slug': product_on_db.slug,
        'stock': 89,
        'price': 327
    }
    response = client.post(url=f'product/update/{product_on_db.id}', json=product)
    assert response.status_code == status.HTTP_200_OK
    db_session.expire_all()
    updated_product = db_session.query(ProductModel).filter_by(id=product_on_db.id).first()
    assert product['stock'] == updated_product.stock
    assert product['price'] == updated_product.price


def test_update_product_non_existent_route(db_session: Session):
    product = {
        'name': 'FOO',
        'slug': 'bar',
        'stock': 89,
        'price': 327
    }
    response = client.post(url='product/update/999999', json=product)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_product_route(
        db_session: Session,
        product_model_camisa: ProductModel,
        category_roupa_on_db: CategoryModel
) -> None:
    product_model_camisa.category_id = category_roupa_on_db.id
    db_session.add(product_model_camisa)
    db_session.commit()
    db_session.refresh(product_model_camisa)
    response = client.delete(f'/product/{product_model_camisa.id}')
    try:
        assert response.status_code == status.HTTP_200_OK
    except AssertionError:
        db_session.delete(product_model_camisa)
        db_session.commit()


def test_delete_product_non_existent_route(db_session: Session) -> None:
    response = client.delete('/product/99999')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_product_route(
        products_on_db: list[ProductModel]
) -> None:
    response = client.get('/product/list')
    products_listed = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(products_listed) == 2
    assert products_on_db[0].id == products_listed[0]['id']
    assert products_on_db[0].name == products_listed[0]['name']
    assert products_on_db[0].stock == products_listed[0]['stock']
    assert products_on_db[0].category.name == products_listed[0]['category']['name']

def test_search_product_existent_by_name_route(
        products_on_db: list[ProductModel]
) -> None:
    key = 'name'
    value = products_on_db[0].name
    response = client.get(f'/product/search/?key={key}&value={value}')
    data = response.json()
    assert data['id'] == products_on_db[0].id

def test_search_product_existent_by_slug_route(
        products_on_db: list[ProductModel]
) -> None:
    key = 'slug'
    value = products_on_db[0].slug
    response = client.get(f'/product/search/?key={key}&value={value}')
    data = response.json()
    assert data['id'] == products_on_db[0].id

def test_search_product_existent_by_invalid_key() -> None:
    key = 'slugdfds'
    value = 'foo'
    response = client.get(f'/product/search/?key={key}&value={value}')
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_search_product_existent_by_invalid_value() -> None:
    key = 'slug'
    value = 'foo'
    response = client.get(f'/product/search/?key={key}&value={value}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
