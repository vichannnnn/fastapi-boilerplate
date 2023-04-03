from app.api.deps import get_session
from app.exceptions import AppError
from app.auth_handler import Authenticator
from app.schemas.auth import AccountSchema
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from app.auth_handler import ALGORITHM, SECRET_KEY

router = APIRouter()


@router.post("/create")
async def create_account(
    data: AccountSchema,
    session: AsyncSession = Depends(get_session),
):
    await Authenticator.register(session, data.username, data.password)
    return {"username": data.username}


@router.get("/get")
async def get_account_name(
    user: AccountSchema = Depends(Authenticator.get_current_user),
):
    return {"username": user.username}


@router.post("/login")
async def user_login(
    data: AccountSchema,
    session: AsyncSession = Depends(get_session),
):
    if not await Authenticator.login(session, data.username, data.password):
        raise AppError.INVALID_CREDENTIALS_ERROR

    access_token = Authenticator.create_access_token(data={"sub": data.username})
    decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    return {
        "data": {"username": data.username},
        "access_token": access_token,
        "token_type": "bearer",
        "exp": decoded_token["exp"],
    }
