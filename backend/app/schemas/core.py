from typing import Optional

from app.schemas.base import CustomBaseModel as BaseModel


class BookCreateSchema(BaseModel):
    title: str
    content: str
    pages: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Book Title",
                    "content": "This is the content of a book.",
                    "pages": 5,
                }
            ]
        }
    }


class BookUpdateSchema(BaseModel):
    title: Optional[str]
    content: Optional[str]
    pages: Optional[int]


class BookSchema(BookCreateSchema):
    id: int
