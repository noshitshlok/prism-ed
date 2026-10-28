import json
from fastapi import APIRouter, HTTPException, Request
from sse_starlette.sse import EventSourceResponse
from app.schemas.tutor import TutorRequest, TutorResponse
from app.services.tutor_service import tutor_service
from app.services.topic_service import topic_service

router = APIRouter(prefix="/tutor", tags=["Tutor"])

@router.post("", response_model=TutorResponse)
@router.post("/", response_model=TutorResponse)
@router.post("/ask", response_model=TutorResponse)
async def ask_tutor(req: TutorRequest, request: Request):
    # 1. Verify topic exists
    topic = topic_service.get_topic_by_id(req.topicId)
    if not topic:
        req_id = getattr(request.state, "request_id", "req-unknown")
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "message": f"Topic '{req.topicId}' not found",
                "requestId": req_id
            }
        )

    # 2. If partId is provided, verify part exists in topic (§4.1, §4.2)
    if req.partId:
        part = topic_service.get_part(req.topicId, req.partId)
        if not part:
            req_id = getattr(request.state, "request_id", "req-unknown")
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "NOT_FOUND",
                    "message": f"Part '{req.partId}' not found in topic '{req.topicId}'",
                    "requestId": req_id
                }
            )

    try:
        return await tutor_service.ask(req)
    except Exception as e:
        req_id = getattr(request.state, "request_id", "req-unknown")
        raise HTTPException(
            status_code=503,
            detail={
                "code": "AI_UNAVAILABLE",
                "message": f"AI Tutor unavailable: {str(e)}",
                "requestId": req_id
            }
        )

@router.post("/stream")
async def stream_tutor(req: TutorRequest, request: Request):
    # 1. Verify topic exists
    topic = topic_service.get_topic_by_id(req.topicId)
    if not topic:
        req_id = getattr(request.state, "request_id", "req-unknown")
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "message": f"Topic '{req.topicId}' not found",
                "requestId": req_id
            }
        )

    # 2. If partId is provided, verify part exists
    if req.partId:
        part = topic_service.get_part(req.topicId, req.partId)
        if not part:
            req_id = getattr(request.state, "request_id", "req-unknown")
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "NOT_FOUND",
                    "message": f"Part '{req.partId}' not found in topic '{req.topicId}'",
                    "requestId": req_id
                }
            )

    async def event_generator():
        try:
            async for token in tutor_service.stream(req):
                yield {
                    "event": "token",
                    "data": json.dumps({"token": token})
                }
            yield {
                "event": "done",
                "data": json.dumps({"done": True})
            }
        except Exception as e:
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }

    return EventSourceResponse(event_generator())
