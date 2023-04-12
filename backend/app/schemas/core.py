from app.schemas.base import CustomBaseModel as BaseModel


class BookCreateSchema(BaseModel):
    title: str
    content: str
    pages: int


class BookUpdateSchema(BaseModel):
    title: str = None
    content: str = None
    pages: int = None


class BookSchema(BookCreateSchema):
    id: int
