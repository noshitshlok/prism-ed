from typing import List, Optional
from pydantic import BaseModel, Field

class MarkerItem(BaseModel):
    markerId: str
    topicId: str
    displayName: str
    thumbnailUrl: str
    highlightPartId: Optional[str] = None
    source: str = "render"
    licence: str = "project"
    credit: str = ""
    # For backward-compatibility with older frontends
    id: Optional[str] = None

    def model_post_init(self, __context):
        if not self.id:
            self.id = self.markerId

class ScannerMarkersResponse(BaseModel):
    markers: List[MarkerItem]
    count: int
    previewNotice: str = "PrismEd Scanner Glimpse Preview (Verified 3D Models)"

# Alias for backward-compatibility with older schema imports
MarkerMetadata = MarkerItem

class ScannerMatchResponse(BaseModel):
    matched: bool
    markerId: Optional[str] = None
    topicId: Optional[str] = None
    topicName: Optional[str] = None
    highlightPartId: Optional[str] = None
    confidence: float = 0.0
    message: str = "Preview scanner match result"
    inliers: int = 0
