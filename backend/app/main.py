from app.api.api import api_router
from fastapi import FastAPI
from fastapi.middleware import cors

app = FastAPI(
    title="FastAPI Boilerplate Microservice",
    description="""This is a boilerplate microservice for setting up CRUD operations quickly.""",
    root_path="/api/v1",
)

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
