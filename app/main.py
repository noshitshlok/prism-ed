import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.logging import logger
from app.core.security import limiter
from app.core.database import init_db
from app.routers import (
    health_router,
    topics_router,
    quiz_router,
    tutor_router,
    scanner_router,
    progress_router
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: 1. Validate content
    from scripts.validate_content import validate_all_content
    try:
        validate_all_content()
    except SystemExit:
        logger.error("Content validation failed on startup! Halting server.")
        raise RuntimeError("Startup content validation failed.")

    # Startup: 2. Initialize database tables
    init_db()
    logger.info("PrismEd database and tables initialized.")
    yield
    # Shutdown
    logger.info("PrismEd API shutting down.")

app = FastAPI(
    title="PrismEd API",
    version="3.0.0",
    description="Interactive 3D / AR Engineering Pedagogy and AI Tutoring Platform",
    lifespan=lifespan
)

# Attach SlowAPI limiter state
app.state.limiter = limiter

# Middleware: Request ID, Timing, and Logging
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-Id") or f"req-{uuid.uuid4().hex[:12]}"
    request.state.request_id = request_id
    start_time = time.time()

    response: Response = await call_next(request)

    process_time = round((time.time() - start_time) * 1000, 2)
    response.headers["X-Request-Id"] = request_id
    response.headers["X-Process-Time-Ms"] = str(process_time)

    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"duration={process_time}ms "
        f"requestId={request_id}"
    )
    return response

# CORS Middleware (Configured strictly from environment settings)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Standardized Error Handlers
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    req_id = getattr(request.state, "request_id", "req-unknown")
    return JSONResponse(
        status_code=429,
        content={
            "error": {
                "code": "RATE_LIMITED",
                "message": "Too many requests. Please slow down.",
                "requestId": req_id
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    req_id = getattr(request.state, "request_id", "req-unknown")
    errors = exc.errors()
    first_error = errors[0] if errors else {}
    msg = f"{first_error.get('loc', ['field'])[-1]}: {first_error.get('msg', 'Invalid input')}"
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": msg,
                "requestId": req_id
            }
        }
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    req_id = getattr(request.state, "request_id", "req-unknown")
    detail = exc.detail
    if isinstance(detail, dict):
        code = detail.get("code", "ERROR")
        message = detail.get("message", "An error occurred")
    else:
        code = "NOT_FOUND" if exc.status_code == 404 else "ERROR"
        message = str(detail)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "requestId": req_id
            }
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    req_id = getattr(request.state, "request_id", "req-unknown")
    logger.exception(f"Unhandled exception on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected server error occurred.",
                "requestId": req_id
            }
        }
    )

# Root liveness check
@app.get("/")
def root():
    return {"status": "PrismEd API running"}

# Mount v1 API Routers under /api/v1
v1_prefix = "/api/v1"
app.include_router(health_router, prefix=v1_prefix)
app.include_router(topics_router, prefix=v1_prefix)
app.include_router(quiz_router, prefix=v1_prefix)
app.include_router(tutor_router, prefix=v1_prefix)
app.include_router(scanner_router, prefix=v1_prefix)
app.include_router(progress_router, prefix=v1_prefix)

# Also mount legacy prefixes for backward compatibility with existing frontend calls
app.include_router(topics_router)
app.include_router(quiz_router)
app.include_router(tutor_router)