from fastapi import APIRouter
from typing import Dict

router = APIRouter()


@router.get("/ping")
async def ping() -> Dict[str, str]:
    return {"status": "ok"}


@router.get("/hello")
async def sanity_check() -> Dict[str, str]:
    return {"Hello": "World!"}
