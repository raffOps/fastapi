from datetime import datetime, timedelta, timezone
import pytest
from decouple import config
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.schemas.user import UserSchema
from app.db.models import UserModel
from app.use_cases.user import UserUseCases

crypt_context = CryptContext(schemes=['sha256_crypt'])
SECRET_KEY=config('SECRET_KEY')
ALGORITHM=config('ALGORITHM')


def test_register_user(db_session):
    uc = UserUseCases(db_session)
    user = UserSchema(username='fooooo', password='bar')
    uc.register(user)

    user_on_db = db_session.query(UserModel).first()
    assert user_on_db is not None
    assert user_on_db.username == user.username
    assert crypt_context.verify(user.password, user_on_db.password)
    db_session.delete(user_on_db)
    db_session.commit()


def test_register_user_username_already_exists(
        db_session: Session,
        user_on_db: UserModel
):
    uc = UserUseCases(db_session)
    user = UserSchema(
        username=user_on_db.username,
        password='bar'
    )
    with pytest.raises(ValueError):
        uc.register(user)


def test_user_login(db_session: Session, user_on_db: UserModel):
    db_session.expire_all()
    uc = UserUseCases(db_session)
    user = UserSchema(username=user_on_db.username, password='bar')
    token_data = uc.login(user=user, expires_in=30)
    assert token_data.expires_at < datetime.now(timezone.utc) + timedelta(31)


def test_user_login_invalid_password(db_session: Session, user_on_db: UserModel):
    uc = UserUseCases(db_session)
    user = UserModel(username=user_on_db.username, password='barr')
    with pytest.raises(ValueError):
        uc.login(user=user, expires_in=30)


def test_user_login_invalid_username(db_session: Session):
    uc = UserUseCases(db_session)
    user = UserModel(username='fooooo', password='bar')
    with pytest.raises(ValueError):
        uc.login(user=user, expires_in=30)


def test_verify_token(db_session: Session, user_on_db: UserModel):
    uc = UserUseCases(db_session)
    data = {
        'sub': user_on_db.username,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    uc.verify_token(token=access_token)


def test_verify_token_expired(db_session: Session, user_on_db: UserModel):
    uc = UserUseCases(db_session)
    data = {
        'sub': user_on_db.username,
        'exp': datetime.now(timezone.utc) - timedelta(minutes=30)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(JWTError):
        uc.verify_token(token=access_token)


def test_verify_username_invalid(db_session: Session):
    uc = UserUseCases(db_session)
    data = {
        'sub': 'foooooo',
        'exp': datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(JWTError):
        uc.verify_token(token=access_token)