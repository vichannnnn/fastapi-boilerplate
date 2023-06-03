from app.db.base_class import Base
from app.crud.base import CRUD
from sqlalchemy.orm import Mapped, mapped_column


class Book(Base, CRUD["Books"]):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    pages: Mapped[int] = mapped_column(nullable=False)
