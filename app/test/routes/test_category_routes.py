from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi import status
from typing import Any

from app.main import app
from app.db.models import CategoryModel
from app.schemas.category import CategoryOutputSchema

client = TestClient(app)

def test_add_category_route(db_session: Session, body_roupa: dict[str, Any]):
    response = client.post(
        url='/category/add',
        json=body_roupa
    )

    assert response.status_code == status.HTTP_201_CREATED

    category_on_db = db_session.query(CategoryModel).all()
    assert len(category_on_db) == 1
    assert category_on_db[0].name == body_roupa['name']
    assert category_on_db[0].slug == body_roupa['slug']
    db_session.delete(category_on_db[0])
    db_session.commit()

def test_list_categories_routes(db_session: Session, categories_on_db: list[CategoryModel]):
    response = client.get('/category/list')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3
    assert data[0] == CategoryOutputSchema(**categories_on_db[0].__dict__).model_dump()
    assert data[1] == CategoryOutputSchema(**categories_on_db[1].__dict__).model_dump()
    assert data[2] == CategoryOutputSchema(**categories_on_db[2].__dict__).model_dump()

