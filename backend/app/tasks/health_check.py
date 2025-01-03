from typing import Any

import requests
from app.utils.worker import celery_app


@celery_app.task(name="ping")  # type: ignore
def ping() -> Any:
    resp = requests.get("http://backend:8000/ping")
    return resp.json()
