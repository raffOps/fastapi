import json

from sqlalchemy.orm import Session
from sqlalchemy.exc import InvalidRequestError
from fastapi import APIRouter, Depends, status, HTTPException

from app.use_cases.product import ProductUseCases
from app.schemas.product import ProductSchema, ProductOutputSchema
from app.routes.deps import get_db_session

product_router = APIRouter(prefix='/product', tags=['Product'])

@product_router.post('/add', status_code=status.HTTP_201_CREATED)
def add_product(
        product: ProductSchema,
        category_slug: str,
        db_session: Session =
        Depends(get_db_session)
):
    uc = ProductUseCases(db_session)
    try:
        uc.add(product, category_slug)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e


@product_router.post('/update/{id}', status_code=status.HTTP_200_OK)
def update_product(
        id: int,
        product: ProductSchema,
        db_session: Session = Depends(get_db_session)
):
    uc = ProductUseCases(db_session)
    try:
        uc.update(id, product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e

@product_router.delete('{id}')
def delete(
        id: int,
        db_session: Session = Depends(get_db_session)
):
    uc = ProductUseCases(db_session=db_session)
    try:
        uc.delete(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e

@product_router.get('/list')
def list_products(db_session: Session = Depends(get_db_session)) -> list[ProductOutputSchema]:
    uc = ProductUseCases(db_session=db_session)
    return uc.list_products()


@product_router.get('/search')
def search(key: str, value: str, db_session: Session = Depends(get_db_session)) -> ProductOutputSchema:
    uc = ProductUseCases(db_session)
    try:
        return uc.search(key, value)
    except ValueError as e1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e1
    except InvalidRequestError as e2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e2