from app.db.models import CategoryModel
from app.schemas.category import CategorySchema, CategoryOutputSchema
from sqlalchemy.orm import Session

class CategoryUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_category(self, category: CategorySchema):
        category = CategoryModel(**category.model_dump())
        self.db_session.add(category)
        self.db_session.commit()

    def list_categories(self) -> list[CategoryOutputSchema]:
        categories = self.db_session.query(CategoryModel).all()
        return [
            self.serialize_category(category)
            for category in categories
        ]

    def serialize_category(self, category: CategoryModel) -> CategoryOutputSchema:
        return CategoryOutputSchema(**category.__dict__)