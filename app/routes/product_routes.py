from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response, status
from app.use_cases.product import ProductUseCases
from app.schemas.product import ProductSchema
from app.routes.deps import get_db_session

product_router = APIRouter(prefix='/product', tags=['Product'])

@product_router.post('/add')
def add_product(product: ProductSchema, category_slug: str,  db_session: Session = Depends(get_db_session)) -> Response:
    uc = ProductUseCases(db_session)
    try:
        uc.add(product, category_slug)
        return Response(status_code=status.HTTP_201_CREATED)
    except ValueError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)