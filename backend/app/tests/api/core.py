from fastapi import status
from fastapi.testclient import TestClient

PING_URL = "/ping"


def test_example(client: TestClient):
    response = client.get(PING_URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
