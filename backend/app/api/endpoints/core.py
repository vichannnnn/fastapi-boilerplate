from typing import List
from fastapi import APIRouter
from app.models.core import Book
from app.schemas.core import BookCreateSchema, BookUpdateSchema, BookSchema
from app.api.deps import CurrentSession

router = APIRouter()
books_router = APIRouter()


@router.post("", response_model=BookSchema)
async def create_book(
    session: CurrentSession,
    book: BookCreateSchema,
):
    new_book = await Book.create(session, data=book.dict())
    return new_book


@books_router.get("", response_model=List[BookSchema])
async def read_books(session: CurrentSession):
    books = await Book.get_all(session)
    return books


@router.get("/{book_id}", response_model=BookSchema)
async def read_book(session: CurrentSession, book_id: int):
    book = await Book.get(session, book_id)
    return book


@router.put("/{book_id}", response_model=BookSchema)
async def update_book(session: CurrentSession, book_id: int, book: BookUpdateSchema):
    updated_book = await Book.update(
        session, book_id, data=book.dict(exclude_unset=True)
    )
    return updated_book


@router.delete("/{book_id}")
async def delete_book(session: CurrentSession, book_id: int):
    deleted_book = await Book.delete(session, book_id)
    return deleted_book
