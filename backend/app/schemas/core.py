from app.schemas.base import CustomBaseModel as BaseModel


class BookCreateSchema(BaseModel):
    title: str
    content: str
    pages: int


class BookUpdateSchema(BaseModel):
    title: str | None = None
    content: str | None = None
    pages: int | None = None


class BookSchema(BookCreateSchema):
    id: int
