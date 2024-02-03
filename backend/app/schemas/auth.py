from typing import Optional, Annotated
from pydantic import constr, StringConstraints, ConfigDict
from app.schemas.base import CustomBaseModel as BaseModel

valid_username = Annotated[
    str, StringConstraints(strip_whitespace=True, pattern="^[a-zA-Z0-9]{4," "20}$")
]
valid_password = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True, pattern=r"^(?=.*[A-Z])(?=.*\W)[^\s]{8,20}$"
    ),
]


class AccountRegisterSchema(BaseModel):
    model_config = ConfigDict(regex_engine="python-re")
    username: valid_username  # type: ignore
    password: valid_password  # type: ignore
    repeat_password: valid_password  # type: ignore


class AccountCreateSchema(BaseModel):
    username: valid_username  # type: ignore
    password: str


class AccountCredentialsSchema(AccountCreateSchema):
    user_id: int


class AccountUpdatePasswordSchema(BaseModel):
    before_password: Optional[valid_password]  # type: ignore
    password: Optional[valid_password]  # type: ignore
    repeat_password: Optional[valid_password]  # type: ignore


class AccountSchema(AccountRegisterSchema):
    user_id: Optional[int]
    repeat_password: Optional[str]


class CurrentUserSchema(BaseModel):
    user_id: int
    username: valid_username  # type: ignore


class CurrentUserWithJWTSchema(BaseModel):
    data: CurrentUserSchema
    access_token: str
    token_type: str
    exp: int


class AuthSchema(BaseModel):
    username: valid_username  # type: ignore
    password: valid_password  # type: ignore
