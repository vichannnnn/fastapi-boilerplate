from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_session
from app.models.core import Book
from app.schemas.core import BookCreateSchema, BookUpdateSchema, BookSchema

router = APIRouter()


@router.get("/ping")
async def ping():
    return {"status": "ok"}


@router.post("/books", response_model=BookSchema)
async def create_book(
    book: BookCreateSchema, session: AsyncSession = Depends(get_session)
):
    new_book = await Book.create(session, data=book.dict())
    return new_book


@router.get("/books", response_model=List[BookSchema])
async def read_books(session: AsyncSession = Depends(get_session)):
    books = await Book.get_all(session)
    return books


@router.get("/books/{book_id}", response_model=BookSchema)
async def read_book(book_id: int, session: AsyncSession = Depends(get_session)):
    book = await Book.get(session, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/books/{book_id}", response_model=BookSchema)
async def update_book(
    book_id: int, book: BookUpdateSchema, session: AsyncSession = Depends(get_session)
):
    updated_book = await Book.update(
        session, book_id, data=book.dict(exclude_unset=True)
    )
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@router.delete("/books/{book_id}", response_model=BookSchema)
async def delete_book(book_id: int, session: AsyncSession = Depends(get_session)):
    deleted_book = await Book.delete(session, book_id)
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book
