from app.exceptions import AppError
from app.models.auth import Authenticator, ALGORITHM, SECRET_KEY, Account
from app.schemas.auth import (
    AccountRegisterSchema,
    CurrentUserSchema,
    AuthSchema,
)
from app.api.deps import CurrentSession
from app.models.auth import CurrentUser
from fastapi import APIRouter
import jwt

router = APIRouter()


@router.post("/create")
async def create_account(
    session: CurrentSession,
    data: AccountRegisterSchema,
):
    created_user = await Account().register(session, data)
    return created_user


@router.get("/get", response_model=CurrentUserSchema)
async def get_account_name(
    session: CurrentSession,
    user: CurrentUser,
):
    return user


@router.post("/login")
async def user_login(session: CurrentSession, data: AuthSchema):
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
