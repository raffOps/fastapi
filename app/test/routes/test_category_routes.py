from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi import status
from typing import Any

from app.main import app
from app.db.models import CategoryModel

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
