from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.routes.deps import get_db_session
from app.schemas.user import UserSchema
from app.use_cases.user import UserUseCases

user_routes = APIRouter(prefix='/users', tags=['User'])
@user_routes.post(
    path='/register',
    status_code=status.HTTP_201_CREATED,
    description='Register new user'
)
def register(user: UserSchema, db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session)
    try:
        return uc.register(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT) from e


@user_routes.post('/login')
def login(
        login_request_form: OAuth2PasswordRequestForm = Depends(),
        db_session: Session = Depends(get_db_session),
) -> Response:
    uc = UserUseCases(db_session)
    user = UserSchema(
        username=login_request_form.username,
        password=login_request_form.password
    )
    try:
        return uc.login(user, expires_in=60)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from e
