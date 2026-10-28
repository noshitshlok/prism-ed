import re
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class Part(BaseModel):
    id: str
    name: str
    hotspotPosition: str
    hotspotNormal: Optional[str] = "0m 1m 0m"
    explodeOffset: Optional[str] = None
    partNode: Optional[str] = None
    explanation: str
    formulaOrLaw: Optional[str] = None

    @field_validator("hotspotPosition")
    @classmethod
    def validate_hotspot(cls, v: str) -> str:
        numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", v)
        if len(numbers) < 3:
            raise ValueError(f"hotspotPosition must contain at least 3 coordinates: {v}")
        return v

    @field_validator("hotspotNormal")
    @classmethod
    def validate_normal(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return "0m 1m 0m"
        numbers = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", v)
        if len(numbers) < 3:
            raise ValueError(f"hotspotNormal must contain at least 3 coordinates: {v}")
        return v

class TopicBase(BaseModel):
    id: str
    name: str
    description: str
    discipline: str
    subfield: Optional[str] = None
    academicLevel: Optional[str] = "Undergraduate"
    tags: List[str] = Field(default_factory=list)
    status: str = "ready"  # "ready" or "not_in_demo"
    modelSource: str = "cad"  # "scan", "cad", "uploaded", or "generated"

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed = {"ready", "not_in_demo"}
        if v not in allowed:
            raise ValueError(f"status must be one of {allowed}, got '{v}'")
        return v

    @field_validator("modelSource")
    @classmethod
    def validate_model_source(cls, v: str) -> str:
        allowed = {"scan", "cad", "uploaded", "generated", "analogue"}
        if v not in allowed:
            raise ValueError(f"modelSource must be one of {allowed}, got '{v}'")
        return v

class TopicListItem(TopicBase):
    partsCount: int = 0

class TopicDetail(TopicBase):
    prerequisites: List[str] = Field(default_factory=list)
    equationsCovered: List[str] = Field(default_factory=list)
    modelUrl: str
    modelFormat: str = "glb"  # glb or gltf
    autoRotate: bool = True
    animation: Optional[str] = None
    parts: List[Part] = Field(default_factory=list)

    @field_validator("parts")
    @classmethod
    def validate_parts_count(cls, v: List[Part]) -> List[Part]:
        if len(v) < 5:
            raise ValueError(f"Every topic must have at least 5 parts, found {len(v)}")
        # Check uniqueness of part IDs
        ids = [p.id for p in v]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate part IDs found: {ids}")
        return v

class TopicListResponse(BaseModel):
    topics: List[TopicDetail]
