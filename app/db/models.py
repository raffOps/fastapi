from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Float,
    func
)
from sqlalchemy.orm import relationship
from app.db.base import Base

class CategoryModel(Base):
    __tablename__ = 'category'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)
    slug = Column('slug', String, nullable=False)
    product = relationship('ProductModel', back_populates='category')

class ProductModel(Base):
    __tablename__ = 'product'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)
    slug = Column('slug', String, nullable=False)
    price = Column('price', Float, nullable=False)
    stock = Column('stock', Integer, nullable=False)
    created_at = Column('created_at', DateTime, server_default=func.now())
    updated_at = Column('updated_at', DateTime, onupdate=datetime.now())
    category_id = Column('category_id', ForeignKey('category.id'), nullable=False)
    category = relationship('CategoryModel', back_populates='product')