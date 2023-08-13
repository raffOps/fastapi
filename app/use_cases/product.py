from typing import List, Type

from sqlalchemy.orm import Session, exc
from app.schemas.product import ProductSchema, ProductOutputSchema
from app.db.models import ProductModel, CategoryModel


class ProductUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, product: ProductSchema, category_slug: str):
        category = self.db_session.\
            query(CategoryModel).\
            filter_by(slug=category_slug).first()
        if not category:
            raise ValueError(f'Category {category_slug} not found')
        product_model = ProductModel(**product.model_dump())
        product_model.category_id = category.id
        self.db_session.add(product_model)
        self.db_session.commit()

    @staticmethod
    def serialize_product(product: Type[ProductModel]) -> ProductOutputSchema:
        product_dict = product.__dict__
        product_dict['category'] = product.category.__dict__
        return ProductOutputSchema(**product_dict)

    def update(self, id: int, product: ProductSchema):
        if not (
                product_on_db := self.db_session.
                        query(ProductModel).filter_by(id=id).first()
        ):
            raise ValueError(f'Product with id {id} not found')
        product_on_db.name = product.name
        product_on_db.slug = product.slug
        product_on_db.price = product.price
        product_on_db.stock = product.stock
        self.db_session.commit()

    def delete(self, id: int):
        if not (
                product := self.db_session.
                        query(ProductModel).filter_by(id=id).first()
        ):
            raise ValueError(f'Product with id {id} not found')
        self.db_session.delete(product)
        self.db_session.commit()


    def list_products(self) -> list[ProductOutputSchema]:
        products =  self.db_session.query(ProductModel).all()

        return [
            self.serialize_product(product)
            for product in products
        ]


    def search(self, key: str, value: str) -> ProductOutputSchema:
        if (
            product := self.db_session.\
                query(ProductModel).\
                filter_by(**{key: value}).first()
        ) is None:
            raise ValueError(f'Product with {key}:{value} not found')
        return self.serialize_product(product)
