from datetime import datetime, timedelta, timezone
from typing import Type

from decouple import config
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.schemas.user import UserSchema, TokenData
from app.db.models import UserModel

crypt_context = CryptContext(schemes=['sha256_crypt'])
SECRET_KEY=config('SECRET_KEY')
ALGORITHM=config('ALGORITHM')

class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def register(self, user: UserSchema):
        user_on_db = UserModel(
            username=user.username,
            password=crypt_context.hash(user.password)
        )
        self.db_session.add(user_on_db)
        try:
            self.db_session.commit()
        except IntegrityError as e:
            self.db_session.rollback()
            raise ValueError('Username already exists') from e


    def _get_user(self, username: str) -> Type[UserModel] | None:
        return self.db_session.query(UserModel).\
            filter_by(username=username).first()


    def login(self, user: UserSchema, expires_in: int = 30):
        if not (user_on_db := self._get_user(user.username)):
            raise ValueError('Invalid Username')
        if not crypt_context.verify(user.password, user_on_db.password):
            raise ValueError('Invalid password')

        expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_in)
        data = {
            'sub': user.username,
            'exp': expires_at
        }
        access_token = jwt.encode(data, key=SECRET_KEY, algorithm=ALGORITHM)
        return TokenData(access_token=access_token, expires_at=expires_at)


    def verify_token(self, token: str):
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not self._get_user(data['sub']):
            raise JWTError