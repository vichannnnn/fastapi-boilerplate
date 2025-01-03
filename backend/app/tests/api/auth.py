from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from app import schemas

CREATE_URL = "/auth/create"
GET_USER_URL = "/auth/get"
LOGIN_URL = "/auth/login"


def test_create_valid_user(
    test_client: TestClient, test_valid_user: schemas.auth.AccountSchema
) -> None:
    payload = jsonable_encoder(test_valid_user)
    response = test_client.post(CREATE_URL, json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user_id": 1, "username": test_valid_user.username}


def test_login(
    test_client: TestClient, test_valid_user: schemas.auth.AccountSchema
) -> None:
    payload = jsonable_encoder(test_valid_user)
    response = test_client.post(CREATE_URL, json=payload)
    assert response.status_code == status.HTTP_200_OK
    response = test_client.post(LOGIN_URL, json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["username"] == test_valid_user.username
