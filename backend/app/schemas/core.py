from app.schemas.base import CustomBaseModel as BaseModel
from typing import Optional

class BookCreateSchema(BaseModel):
    title: str
    content: str
    pages: int


class BookUpdateSchema(BaseModel):
    title: Optional[str]
    content: Optional[str]
    pages: Optional[int]


class BookSchema(BookCreateSchema):
    id: int
