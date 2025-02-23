from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator
from src.exceptions import (
    ClientException,
    SensorAppException,
    ServerException,
)
from starlette.middleware.cors import CORSMiddleware
from opentelemetry import trace

from webapp.routers import (
    health,
    sensor,
)
from webapp.container import ApplicationContainer, create_container

logger = logging.getLogger(__name__)


def create_app(container: ApplicationContainer = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # set up
        logger.info("Setting up application")
        yield
        # tear down
        logger.info("Tearing down application")

    app = FastAPI(
        title="Sensor Server",
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        servers=[
            {"url": "/", "description": "Local Test"},
            {"url": "http://localhost", "description": "Local Test"},
        ],
        lifespan=lifespan,
        generate_unique_id_function=lambda route: route.name,
    )

    app.include_router(health.router, tags=["health"], include_in_schema=False)
    app.include_router(sensor.router, tags=["sensor"])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,
    )

    # 프로메테우스 Metric 설정
    Instrumentator().instrument(app).expose(app, include_in_schema=False)

    # opentelemetry 설정
    FastAPIInstrumentor.instrument_app(app)
    AsyncPGInstrumentor().instrument()

    def get_trace_id():
        """opentelemetry 의 trace_id 를 가져옵니다."""
        try:
            span_context = trace.get_current_span().get_span_context()
            return format(span_context.trace_id, "032x")
        except Exception as e:
            return ""

    @app.exception_handler(ClientException)
    async def client_exception_handler(request: Request, exc: ClientException):
        logger.error(f"Client exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=400,
            content={
                "message": exc.message,
                "code": exc.__class__.__name__,
                "trace_id": get_trace_id(),
            },
        )

    @app.exception_handler(ServerException)
    async def server_exception_handler(request: Request, exc: ServerException):
        logger.error(f"Server exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "message": exc.message,
                "code": exc.__class__.__name__,
                "trace_id": get_trace_id(),
            },
        )

    @app.exception_handler(SensorAppException)
    async def sensor_exception_handler(request: Request, exc: SensorAppException):
        logger.error(f"Sensor App exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "message": exc.message,
                "code": exc.__class__.__name__,
                "trace_id": get_trace_id(),
            },
        )

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        logger.error(f"Exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=503,
            content={"message": str(exc), "code": exc.__class__.__name__},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        logger.error(f"Validation error: {exc.errors()}", exc_info=True)
        return JSONResponse(
            status_code=422,
            content={
                "message": exc.errors(),
                "code": exc.__class__.__name__,
                "trace_id": get_trace_id(),
            },
        )

    app.container = container or create_container()
    return app
