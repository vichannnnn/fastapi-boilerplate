from typing import AsyncGenerator, Generator
from app.db.database import SessionLocal, async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


CurrentSession = Annotated[AsyncSession, Depends(get_session)]

