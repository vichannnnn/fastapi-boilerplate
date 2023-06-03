from app.api.deps import get_session
from app.exceptions import AppError
from app.models.auth import Authenticator, ALGORITHM, SECRET_KEY, Account
from app.schemas.auth import (
    AccountRegisterSchema,
    CurrentUserSchema,
    AuthSchema,
)
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

router = APIRouter()


@router.post("/create")
async def create_account(
    data: AccountRegisterSchema,
    session: AsyncSession = Depends(get_session),
):
    if data.password != data.repeat_password:
        raise AppError.PASSWORD_MISMATCH_ERROR

    created_user = await Account().register(session, data)
    return created_user


@router.get("/get", response_model=CurrentUserSchema)
async def get_account_name(
    user: AuthSchema = Depends(Authenticator.get_current_user),
):
    return user


@router.post("/login")
async def user_login(
    data: AuthSchema,
    session: AsyncSession = Depends(get_session),
):
    credentials = await Account.login(session, data.username, data.password)

    if not credentials:
        raise AppError.INVALID_CREDENTIALS_ERROR

    access_token = Authenticator.create_access_token(data={"sub": data.username})
    decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    return {
        "data": credentials,
        "access_token": access_token,
        "token_type": "bearer",
        "exp": decoded_token["exp"],
    }
