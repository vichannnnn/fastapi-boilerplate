from app.db.base_class import Base
from app.crud.base import CRUD
from sqlalchemy import Column, Integer, String


class Book(Base, CRUD["Books"]):
    __tablename__ = "books"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    pages = Column(Integer, nullable=False)
