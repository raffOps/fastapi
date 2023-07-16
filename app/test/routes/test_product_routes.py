from typing import Any

from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session
import logging

from app.main import app
from app.db.models import ProductModel, CategoryModel
from app.schemas.product import ProductOutputSchema


client = TestClient(app)

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

def test_add_product_route_non_existent_route(db_session: Session, product_json_camisa: dict[str, Any]):
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