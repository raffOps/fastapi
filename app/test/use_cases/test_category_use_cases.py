import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.db.models import CategoryModel as CategoryModel
from app.schemas.category import CategorySchema, CategoryOutputSchema
from app.use_cases.category import CategoryUseCases


def test_add_category_use_case(db_session: Session, category_schema_roupa: CategorySchema):
    use_case = CategoryUseCases(db_session)
    use_case.add_category(category_schema_roupa)
    category_on_db = db_session.query(CategoryModel).all()
    assert len(category_on_db) == 1
    assert category_on_db[0].name == category_schema_roupa.name
    assert category_on_db[0].slug == category_schema_roupa.slug

    db_session.delete(category_on_db[0])
    db_session.commit()


def test_list_category_use_case(db_session: Session, categories_on_db):
    use_case = CategoryUseCases(db_session)
    categories = use_case.list_categories()
    assert len(categories) == 3
    assert type(categories[0]) == CategoryOutputSchema
    assert categories[0].name == categories_on_db[0].name
    assert categories[0].slug == categories_on_db[0].slug
    assert categories[0].id == categories_on_db[0].id


def test_delete_category_use_case_non_exist(db_session: Session, category_calcado: CategoryModel):
    use_case = CategoryUseCases(db_session)
    with pytest.raises(NoResultFound):
        use_case.delete_category(id=category_calcado.id)


def test_delete_category_use_case(db_session: Session, category_calcado: CategoryModel):
    db_session.add(category_calcado)
    db_session.commit()
    use_case = CategoryUseCases(db_session)
    use_case.delete_category(id=category_calcado.id)
    category = db_session.query(CategoryModel).filter_by(id=category_calcado.id).first()
    assert category is None
#
