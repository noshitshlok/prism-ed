from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse

from app.schemas.scanner import ScannerMarkersResponse, ScannerMatchResponse
from app.services.scanner_service import scanner_service, BASE_DIR

router = APIRouter(prefix="/scanner", tags=["Scanner"])

MARKERS_DIR = BASE_DIR / "data" / "markers"
THUMBS_DIR = MARKERS_DIR / "thumbnails"
IMAGES_DIR = MARKERS_DIR / "images"

@router.get("/markers", response_model=ScannerMarkersResponse)
def get_supported_markers():
    """List supported preview markers and thumbnail URLs."""
    return scanner_service.list_supported_markers()

@router.get("/markers/{marker_id}/thumbnail")
def get_marker_thumbnail(marker_id: str):
    """Serve a reduced thumbnail copy of the marker reference image."""
    marker = scanner_service.get_marker_by_id(marker_id)
    if not marker:
        raise HTTPException(
            status_code=404,
            detail={"code": "NOT_FOUND", "message": f"Marker {marker_id} not found"}
        )

    # Check thumbnail directory first
    thumb_path = THUMBS_DIR / f"{marker.topicId}_thumb.png"
    if thumb_path.exists():
        return FileResponse(thumb_path, media_type="image/png")

    # Fallback to full marker image
    img_path = IMAGES_DIR / f"{marker.topicId}.png"
    if img_path.exists():
        return FileResponse(img_path, media_type="image/png")

    raise HTTPException(
        status_code=404,
        detail={"code": "NOT_FOUND", "message": f"Thumbnail image for {marker_id} not found"}
    )

@router.post("/match", response_model=ScannerMatchResponse)
async def match_uploaded_photo(
    request: Request,
    file: UploadFile = File(...)
):
    """Match query photograph against precomputed reference markers."""
    try:
        contents = await file.read()
        return scanner_service.match_image(
            image_bytes=contents,
            filename=file.filename or "upload.png",
            content_type=file.content_type
        )
    except HTTPException:
        raise
    except Exception as e:
        req_id = getattr(request.state, "request_id", "req-unknown")
        raise HTTPException(
            status_code=400,
            detail={
                "code": "VALIDATION_ERROR",
                "message": f"Failed to process scanner image: {str(e)}",
                "requestId": req_id
            }
        )
