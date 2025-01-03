from typing import Annotated, AsyncGenerator, Generator

from fastapi import Depends
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.database import SessionLocal, async_session
from app.models.auth import Account
from app.schemas.auth import CurrentUserSchema
from app.utils.auth import ALGORITHM, SECRET_KEY, Authenticator
from app.utils.exceptions import AppError


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


CurrentSession = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user(
    session: CurrentSession,
    token: str = Depends(Authenticator.oauth2_scheme),
) -> CurrentUserSchema:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        if username := payload.get("sub"):
            if user := await Account.select_from_username(session, username):
                return CurrentUserSchema(
                    user_id=user.user_id,
                    username=username,
                )

    except JWTError as exc:
        raise AppError.INVALID_CREDENTIALS_ERROR from exc
    raise AppError.INVALID_CREDENTIALS_ERROR


CurrentUser = Annotated[CurrentUserSchema, Depends(get_current_user)]
