import jwt
from typing import Optional
from fastapi import Response as FastAPIResponse
from sqlalchemy import exc as SQLAlchemyExceptions
from sqlalchemy import select, update, Index
from sqlalchemy.orm import Mapped, mapped_column, synonym
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import text
from app.crud.base import CRUD
from app.db.base_class import Base
from app.utils.auth import Authenticator, ALGORITHM, SECRET_KEY
from app.utils.exceptions import AppError
from app.schemas.auth import (
    AccountRegisterSchema,
    AccountCreateSchema,
    AccountCredentialsSchema,
    AccountUpdatePasswordSchema,
    AuthSchema,
    CurrentUserWithJWTSchema,
    CurrentUserSchema,
)


class Account(Base, CRUD["Account"]):
    __tablename__: str = "account"  # type: ignore
    __table_args__ = (
        Index("username_case_sensitive_index", text("upper(username)"), unique=True),
    )

    user_id: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True
    )
    username: Mapped[str] = mapped_column(nullable=False, index=True, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

    id: Mapped[int] = synonym("user_id")

    @classmethod
    async def register(
        cls, session: AsyncSession, data: AccountRegisterSchema
    ) -> CurrentUserSchema:
        username = data.username
        password = data.password
        repeat_password = data.repeat_password

        if password != repeat_password:  # type: ignore
            raise AppError.PASSWORD_MISMATCH_ERROR

        hashed_password = Authenticator.pwd_context.hash(password)
        insert_data = AccountCreateSchema(username=username, password=hashed_password)
        res = await super().create(session, insert_data.dict())
        await session.refresh(res)
        return CurrentUserSchema(**res.__dict__)

    @classmethod
    async def select_from_username(
        cls, session: AsyncSession, username: str
    ) -> Optional[AccountCredentialsSchema]:
        try:
            stmt = select(Account).where(Account.username.ilike(username))
            res = await session.execute(stmt)
            return res.scalars().one()  # type: ignore

        except SQLAlchemyExceptions.NoResultFound:
            return None

    @classmethod
    async def login(
        cls, session: AsyncSession, data: AuthSchema
    ) -> CurrentUserWithJWTSchema:
        if not (credentials := await cls.select_from_username(session, data.username)):
            raise AppError.INVALID_CREDENTIALS_ERROR
        if not Authenticator.pwd_context.verify(data.password, credentials.password):
            raise AppError.INVALID_CREDENTIALS_ERROR

        access_token = Authenticator.create_access_token(data={"sub": data.username})
        decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])

        current_user = CurrentUserSchema(
            user_id=credentials.user_id, username=credentials.username
        )
        res = CurrentUserWithJWTSchema(
            data=current_user,
            access_token=access_token,
            token_type="bearer",
            exp=decoded_token["exp"],
        )

        return res

    @classmethod
    async def update_password(
        cls, session: AsyncSession, user_id: int, data: AccountUpdatePasswordSchema
    ) -> FastAPIResponse:
        if data.before_password is None or data.password is None:
            raise AppError.BAD_REQUEST_ERROR

        curr = await Account.get(session, id=user_id)
        if (
            not Authenticator.pwd_context.verify(data.before_password, curr.password)
            or not curr
        ):
            raise AppError.INVALID_CREDENTIALS_ERROR

        if data.password != data.repeat_password:
            raise AppError.PASSWORD_MISMATCH_ERROR

        hashed_updated_password = Authenticator.pwd_context.hash(data.password)

        stmt = (
            update(Account)
            .returning(Account)
            .where(Account.user_id == user_id)
            .values({"password": hashed_updated_password})
        )
        await session.execute(stmt)
        await session.commit()
        return FastAPIResponse(status_code=204)
