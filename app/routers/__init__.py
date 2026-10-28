from app.routers.health import router as health_router
from app.routers.topics import router as topics_router
from app.routers.quiz import router as quiz_router
from app.routers.tutor import router as tutor_router
from app.routers.scanner import router as scanner_router
from app.routers.progress import router as progress_router

__all__ = [
    "health_router",
    "topics_router",
    "quiz_router",
    "tutor_router",
    "scanner_router",
    "progress_router"
]
