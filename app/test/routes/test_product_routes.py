from typing import Any

from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session

from app.main import app
from app.db.models import ProductModel, CategoryModel
from app.schemas.product import ProductOutputSchema


client = TestClient(app)


def test_add_product_route(db_session: Session, product_json_camisa: dict[str, Any]):
    response = client.post(
        url='product/add',
        json=product_json_camisa
    )

    assert response.status_code == status.HTTP_201_CREATED
    db_session.delete(ProductModel(**product_json_camisa['product']))
    db_session.commit()