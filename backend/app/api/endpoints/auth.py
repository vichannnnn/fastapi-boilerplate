from app.models.auth import Account
from app.schemas.auth import (
    AccountRegisterSchema,
    CurrentUserSchema,
    AuthSchema,
    CurrentUserWithJWTSchema,
)
from app.api.deps import CurrentSession, CurrentUser
from fastapi import APIRouter


router = APIRouter()


@router.post("/create", response_model=CurrentUserSchema)
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


@router.post("/login", response_model=CurrentUserWithJWTSchema)
async def user_login(session: CurrentSession, data: AuthSchema):
    res = await Account.login(session, data)
    return res
