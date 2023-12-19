import logging

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.models import UserModel
from app.main import app

client = TestClient(app)
LOGGER = logging.getLogger(__name__)


def test_register_user_route(db_session: Session):
    user = {
        'username': 'fooo',
        'password': 'bar'
    }
    response = client.post('users/register', json=user)
    assert response.status_code == status.HTTP_201_CREATED
    user_on_db = db_session.query(UserModel).first()
    assert user_on_db.username == user['username']
    db_session.delete(user_on_db)
    db_session.commit()


def test_register_user_route_username_already_exists(
        db_session: Session,
        user_on_db: UserModel
):
    user = {
        'username': user_on_db.username,
        'password': 'bar'
    }
    response = client.post('users/register', json=user)
    assert response.status_code == status.HTTP_409_CONFLICT
    db_session.delete(user_on_db)
    db_session.commit()


def test_user_login_route(user_on_db: UserModel):
    body = {
        'username': user_on_db.username,
        'password': 'bar'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = client.post('users/login', data=body, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'access_token' in data
    assert 'expires_at' in data


def test_user_login_route_invalid_password(user_on_db):
    body = {
        'username': user_on_db.username,
        'password': 'barr'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = client.post('users/login', data=body, headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_login_route_invalid_username(user_on_db):
    body = {
        'username': 'fooo',
        'password': 'bar'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = client.post('users/login', data=body, headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
