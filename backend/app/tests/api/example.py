from fastapi import status
from fastapi.testclient import TestClient

PING_URL = "/ping"
HELLO_WORLD_URL = "/hello"
TRIGGER_TASK_URL = "/trigger_ping_task"
CHECK_PING_TASK_URL = "/check_ping_task"


def test_ping_example(test_client: TestClient) -> None:
    response = test_client.get(PING_URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}


def test_hello_world_example(test_client: TestClient) -> None:
    response = test_client.get(HELLO_WORLD_URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Hello": "World!"}


def test_trigger_ping_task(test_client: TestClient) -> None:
    response = test_client.post(TRIGGER_TASK_URL)
    assert response.status_code == status.HTTP_200_OK

    task_id = response.json()["task_id"]
    assert task_id

    response = test_client.get(f"{CHECK_PING_TASK_URL}/{task_id}")
    assert response.status_code == status.HTTP_200_OK
