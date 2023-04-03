from fastapi import status
from fastapi.testclient import TestClient

HELLO_WORLD_URL = "/hello"


def test_example(client: TestClient):
    response = client.get(HELLO_WORLD_URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Hello": "World!"}
