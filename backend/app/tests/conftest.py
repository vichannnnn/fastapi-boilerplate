import asyncio
from asyncio import AbstractEventLoop
from typing import AsyncGenerator, Generator
from app.api.deps import get_session, get_current_user
from app.main import app
from app.db.base_class import Base
from app.db.database import (
    engine as test_engine,
    async_session as TestingSessionLocal,
    SQLALCHEMY_DATABASE_URL_WITHOUT_DB,
)
from app import schemas
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import sqlalchemy.exc as SQLAlchemyExceptions
import pytest


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    return asyncio.get_event_loop()


@pytest.fixture(scope="session", autouse=True)
async def create_test_database() -> AsyncGenerator[None, None]:
    postgres_engine = create_async_engine(str(SQLALCHEMY_DATABASE_URL_WITHOUT_DB))

    async with postgres_engine.connect() as conn:
        await conn.execute(text("COMMIT"))
        try:
            await conn.execute(text("CREATE DATABASE test;"))
        except SQLAlchemyExceptions.ProgrammingError as exc:
            pass

    yield

    async with postgres_engine.connect() as conn:
        await conn.execute(text("COMMIT"))
        await conn.execute(text("DROP DATABASE test;"))
        await conn.close()


@pytest.fixture(scope="function", autouse=True)
async def init_models(event_loop: AbstractEventLoop) -> None:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    app.dependency_overrides[get_session] = override_session


async def override_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
        await session.close()


async def override_get_current_user() -> schemas.auth.CurrentUserSchema:
    return schemas.auth.CurrentUserSchema(user_id=1, username="testuser")


@pytest.fixture(name="test_client")
def test_client() -> Generator[TestClient, None, None]:
    yield TestClient(app)


@pytest.fixture(name="test_logged_in_client")
def test_logged_in_client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield TestClient(app)
    app.dependency_overrides = {}


@pytest.fixture(name="test_valid_user")
def test_valid_user() -> Generator[schemas.auth.AccountRegisterSchema, None, None]:
    yield schemas.auth.AccountRegisterSchema(
        username="validusername",
        password="Validpassword123!",
        repeat_password="Validpassword123!",
    )


@pytest.fixture(name="test_book_insert")
def test_book_insert() -> Generator[schemas.core.BookCreateSchema, None, None]:
    yield schemas.core.BookCreateSchema(
        title="Testing Book 1", content="This is the content.", pages=2
    )


@pytest.fixture(name="test_book_update")
def test_book_update() -> Generator[schemas.core.BookUpdateSchema, None, None]:
    yield schemas.core.BookUpdateSchema(
        title="Updated Testing Book 1", content="This is the updated content.", pages=2
    )
