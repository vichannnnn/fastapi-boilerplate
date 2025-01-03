from sqlalchemy.orm import Mapped, mapped_column, synonym

from app.crud.base import CRUD
from app.db.base_class import Base


class Book(Base, CRUD["Book"]):
    __tablename__: str = "book"  # type: ignore

    book_id: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True
    )
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    pages: Mapped[int] = mapped_column(nullable=False)

    id: Mapped[int] = synonym("book_id")
