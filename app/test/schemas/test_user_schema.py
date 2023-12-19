from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas.user import UserSchema, TokenData


def test_user_schema():
    user = UserSchema(username='rafael', password='foo')
    assert user.model_dump() == {
        'username': 'rafael',
        'password': 'foo'
    }


def test_user_schema_invalid_name():
    with pytest.raises(ValidationError):
        UserSchema(username='rafael$', password='foo')


def test_token_data():
    expire_at = datetime.now()
    token_data = TokenData(
        access_token='foo',
        expires_at=expire_at
    )
    assert token_data.model_dump() == {
        'access_token': 'foo',
        'expires_at': expire_at
    }
