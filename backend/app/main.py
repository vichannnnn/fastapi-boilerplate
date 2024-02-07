import os
import time
import json
import logging
from app.api.api import api_router
from fastapi import FastAPI, Request
from fastapi.middleware import cors
from app.observability import PrometheusMiddleware, metrics, setting_otlp, logger


APP_NAME = os.environ.get("APP_NAME", "backend")
EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 8000)
OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "http://tempo:4317")


class LoggingMiddleware:
    @staticmethod
    async def log_request(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time_seconds = time.time() - start_time
        process_time_ms = round(
            process_time_seconds * 1000, 6
        )  # Convert to milliseconds and round to 6 decimal places
        process_time_str = f"{process_time_ms} ms"

        log_data = {
            "request_method": request.method,
            "request_url": request.url.path,
            "response_status": response.status_code,
            "process_time_ms": process_time_str,
        }
        logger.info(json.dumps(log_data))
        return response


app = FastAPI(
    title="FastAPI Boilerplate Microservice",
    description="""This is a boilerplate microservice for setting up CRUD operations quickly.""",
    root_path="/api/v1",
)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    return await LoggingMiddleware.log_request(request, call_next)


app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(PrometheusMiddleware, app_name=APP_NAME)
app.add_route("/metrics", metrics)

app.include_router(api_router)

setting_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)


class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
