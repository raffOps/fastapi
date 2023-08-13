import fastapi.exceptions
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response, status
from app.schemas.category import CategorySchema, CategoryOutputSchema
from app.db.models import CategoryModel
from app.routes.deps import get_db_session
from app.use_cases.category import CategoryUseCases


category_router = APIRouter(prefix='/category', tags=['Category'])

@category_router.post('/add',
                      status_code=status.HTTP_201_CREATED,
                      description='Add new category')
def add_category(category: CategorySchema, db_session: Session = Depends(get_db_session)) -> Response:
    uc = CategoryUseCases(db_session)
    uc.add_category(category)
    return Response(status_code=status.HTTP_201_CREATED)


@category_router.get('/list')
def list_categories(
        db_session: Session = Depends(get_db_session)
) -> list[CategoryOutputSchema]:
    uc = CategoryUseCases(db_session)
    return uc.list_categories()


@category_router.delete('/delete/{id}')
def delete_category(id: int, db_session: Session = Depends(get_db_session)) -> Response:
    uc = CategoryUseCases(db_session)
    try:
        uc.delete_category(id)
        return Response(status_code=fastapi.status.HTTP_200_OK)
    except NoResultFound:
        return Response(status_code=fastapi.status.HTTP_404_NOT_FOUND)


