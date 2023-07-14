from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def ping():
    return {"status": "ok"}


@router.get("/hello")
async def sanity_check():
    return {"Hello": "World!"}
