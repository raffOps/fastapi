from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response, status
from app.schemas.category import CategorySchema, CategoryOutputSchema
from app.db.models import CategoryModel
from app.routes.deps import get_db_session
from app.use_cases.category import CategoryUseCases


category_router = APIRouter(prefix='/category', tags=['Category'])

@category_router.post('/add')
def add_category(category: CategorySchema, db_session: Session = Depends(get_db_session)) -> Response:
    uc = CategoryUseCases(db_session)
    uc.add_category(category)
    return Response(status_code=status.HTTP_201_CREATED)


@category_router.get('/list')
def list_categories(db_session: Session = Depends(get_db_session)) -> list[CategoryOutputSchema]:
    uc = CategoryUseCases(db_session)
    return uc.list_categories()


