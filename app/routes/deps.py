from fastapi import Depends

from app.db.connection import Session
from fastapi.security import OAuth2PasswordBearer

#oauth_schema = OAuth2PasswordBearer(tokenUrl='/user/login')


def get_db_session() -> Session:
    try:
        session = Session()
        yield session
    finally:
        session.close()


# def auth(
#     db_session: Session = Depends(get_db_session),
#     token = Depends(oauth_schema)
# ):
#     uc = Us