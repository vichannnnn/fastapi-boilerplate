from pydantic import BaseModel, constr


class AccountSchema(BaseModel):
    username: constr(min_length=6, max_length=20)  # type: ignore
    password: constr(min_length=8, max_length=20)  # type: ignore