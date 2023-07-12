from sqlalchemy.orm import Session
from app.schemas.product import ProductSchema
from app.db.models import ProductModel, CategoryModel
class ProductUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, product: ProductSchema, category_slug: str):
        category = self.db_session.query(CategoryModel).filter_by(slug=category_slug).first()
        if not category:
            raise ValueError(f'Category {category_slug} not found')
        product_model = ProductModel(**product.model_dump())
        product_model.category_id = category.id
        self.db_session.add(product_model)
        self.db_session.commit()
