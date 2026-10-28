from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Request
from app.schemas.topic import TopicListItem, TopicDetail
from app.services.topic_service import topic_service

router = APIRouter(prefix="/topics", tags=["Topics"])

@router.get("", response_model=List[TopicListItem])
@router.get("/", response_model=List[TopicListItem])
def list_topics(
    discipline: Optional[str] = Query(None, description="Filter by discipline"),
    tag: Optional[str] = Query(None, description="Filter by topic tag"),
    level: Optional[str] = Query(None, description="Filter by academic level"),
    status: Optional[str] = Query("ready", description="Filter by status"),
    include_all: bool = Query(False, description="Include all topics including not_in_demo")
):
    return topic_service.list_topics(
        discipline=discipline,
        tag=tag,
        level=level,
        status=status,
        include_all=include_all
    )

@router.get("/{topic_id}", response_model=TopicDetail)
def get_topic(topic_id: str, request: Request):
    topic = topic_service.get_topic_by_id(topic_id)
    if not topic:
        req_id = getattr(request.state, "request_id", "req-unknown")
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "message": f"Topic '{topic_id}' not found in registry",
                "requestId": req_id
            }
        )
    return topic