from fastapi import status
from fastapi.testclient import TestClient
from app import schemas
from fastapi.encoders import jsonable_encoder

PING_URL = "/ping"
BOOK_URL = "/books"


def test_example(client: TestClient):
    response = client.get(PING_URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}


def test_add_book(client: TestClient, test_book_insert: schemas.core.BookCreateSchema):
    payload = jsonable_encoder(test_book_insert)
    response = client.post(BOOK_URL, json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == 1
    assert response.json()['title'] == test_book_insert.title
    assert response.json()['content'] == test_book_insert.content
    assert response.json()['pages'] == test_book_insert.pages
