from typing import Optional
from pydantic import constr
from app.schemas.base import CustomBaseModel as BaseModel

ValidPassword = constr(
    regex="^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&^])[^\s]{8,20}$"
)  # pylint: disable=[W1401]
ValidUsername = constr(regex="^[a-zA-Z0-9]{4,20}$")  # pylint: disable=[W1401]


class AccountRegisterSchema(BaseModel):
    username: ValidUsername  # type: ignore
    password: ValidPassword  # type: ignore
    repeat_password: ValidPassword  # type: ignore


class AccountUpdatePasswordSchema(BaseModel):
    before_password: Optional[ValidPassword]  # type: ignore
    password: Optional[ValidPassword]  # type: ignore
    repeat_password: Optional[ValidPassword]  # type: ignore


class AccountSchema(AccountRegisterSchema):
    user_id: Optional[int]
    repeat_password: Optional[str]


class CurrentUserSchema(BaseModel):
    user_id: int
    username: ValidUsername  # type: ignore


class AuthSchema(BaseModel):
    username: ValidUsername  # type: ignore
    password: ValidPassword  # type: ignore
