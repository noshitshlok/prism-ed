from fastapi import APIRouter
from app.core.config import settings
from app.services.scanner_service import scanner_service

router = APIRouter(tags=["Health & Diagnostics"])

@router.get("/health")
def health_check():
    has_groq = bool(settings.active_groq_key)
    has_gemini = bool(settings.GEMINI_API_KEY)

    return {
        "status": "healthy",
        "service": "PrismEd API",
        "version": "3.0.0",
        "environment": settings.ENVIRONMENT,
        "ai": {
            "primaryProvider": "groq",
            "primaryConfigured": has_groq,
            "tutorModel": settings.GROQ_TUTOR_MODEL,
            "quizModel": settings.GROQ_QUIZ_MODEL,
            "fallbackProvider": "gemini",
            "fallbackConfigured": has_gemini,
            "fallbackModel": settings.GEMINI_MODEL
        },
        "scanner": {
            "markersLoaded": scanner_service.markers_count,
            "descriptorsLoaded": scanner_service.descriptors_count
        },
        "rateLimitPerMinute": settings.RATE_LIMIT_PER_MINUTE
    }
