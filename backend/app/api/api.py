from app.api.endpoints import core, example, auth, tasks
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(example.router, tags=["Example"])
api_router.include_router(core.router, tags=["Core"], prefix="/book")
api_router.include_router(core.books_router, tags=["Core"], prefix="/books")
api_router.include_router(tasks.router, tags=["Tasks"])
api_router.include_router(auth.router, tags=["Authentication"], prefix="/auth")
