from fastapi import status
from fastapi.testclient import TestClient
from app import schemas
from fastapi.encoders import jsonable_encoder

BOOK_URL = "/book"
BOOKS_URL = "/books"


def test_add_book(
    test_client: TestClient, test_book_insert: schemas.core.BookCreateSchema
):
    payload = jsonable_encoder(test_book_insert)
    response = test_client.post(BOOK_URL, json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 1
    assert response.json()["title"] == test_book_insert.title
    assert response.json()["content"] == test_book_insert.content
    assert response.json()["pages"] == test_book_insert.pages


def test_get_books(
    test_client: TestClient, test_book_insert: schemas.core.BookCreateSchema
):
    payload = jsonable_encoder(test_book_insert)
    response = test_client.post(BOOK_URL, json=payload)
    assert response.status_code == status.HTTP_200_OK
    response = test_client.get(BOOKS_URL)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == test_book_insert.title


def test_get_one_book(
    test_client: TestClient, test_book_insert: schemas.core.BookCreateSchema
):
    payload = jsonable_encoder(test_book_insert)
    response = test_client.post(BOOK_URL, json=payload)
    assert response.status_code == status.HTTP_200_OK
    book_id = 1
    response = test_client.get(BOOK_URL + "/" + str(book_id))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == book_id
    assert response.json()["title"] == test_book_insert.title


def test_update_book(
    test_client: TestClient,
    test_book_insert: schemas.core.BookCreateSchema,
    test_book_update: schemas.core.BookUpdateSchema,
):
    payload = jsonable_encoder(test_book_insert)
    response = test_client.post(BOOK_URL, json=payload)
    assert response.status_code == status.HTTP_200_OK
    payload = jsonable_encoder(test_book_update)
    book_id = 1
    response = test_client.put(BOOK_URL + "/" + str(book_id), json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 1
    assert response.json()["title"] == test_book_update.title
    assert response.json()["content"] == test_book_update.content
    assert response.json()["pages"] == test_book_update.pages


def test_delete_book(test_client: TestClient,test_book_insert: schemas.core.BookCreateSchema,):

    payload = jsonable_encoder(test_book_insert)
    response = test_client.post(BOOK_URL, json=payload)
    assert response.status_code == status.HTTP_200_OK

    exist_book_id = 1
    response = test_client.delete(BOOK_URL + "/" + str(exist_book_id))
    assert response.status_code == status.HTTP_204_NO_CONTENT

    does_not_exist_id = 2
    response = test_client.delete(BOOK_URL + "/" + str(does_not_exist_id))
    assert response.status_code == status.HTTP_404_NOT_FOUND
