from app.utils.worker import celery_app
from typing import Any
import requests


@celery_app.task(name="ping")  # type: ignore
def ping() -> Any:
    resp = requests.get("http://backend:8000/ping")
    return resp.json()
