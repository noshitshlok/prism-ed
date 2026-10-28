import json
from pathlib import Path
from typing import List, Optional
from app.schemas.topic import TopicDetail, TopicListItem, Part
from app.core.config import settings

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "topics.json"

class TopicService:
    def __init__(self):
        self._topics_cache: Optional[List[TopicDetail]] = None
        self._load_topics()

    def _load_topics(self):
        if not DATA_FILE.exists():
            self._topics_cache = []
            return
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            self._topics_cache = [TopicDetail(**t) for t in data.get("topics", [])]

    def list_topics(
        self,
        discipline: Optional[str] = None,
        tag: Optional[str] = None,
        level: Optional[str] = None,
        status: Optional[str] = "ready",
        include_all: bool = False,
    ) -> List[TopicListItem]:
        if self._topics_cache is None:
            self._load_topics()

        results = []
        for t in self._topics_cache:
            if not include_all and status and t.status != status:
                continue
            if discipline and t.discipline.lower() != discipline.lower():
                continue
            if level and t.academicLevel and t.academicLevel.lower() != level.lower():
                continue
            if tag and tag.lower() not in [x.lower() for x in t.tags]:
                continue

            results.append(TopicListItem(
                id=t.id,
                name=t.name,
                description=t.description,
                discipline=t.discipline,
                subfield=t.subfield,
                academicLevel=t.academicLevel,
                tags=t.tags,
                status=t.status,
                modelSource=t.modelSource,
                partsCount=len(t.parts)
            ))
        return results

    def get_topic_by_id(self, topic_id: str) -> Optional[TopicDetail]:
        if self._topics_cache is None:
            self._load_topics()

        for t in self._topics_cache:
            if t.id == topic_id:
                return t
        return None

    def get_part(self, topic_id: str, part_id: str) -> Optional[Part]:
        topic = self.get_topic_by_id(topic_id)
        if not topic:
            return None
        for p in topic.parts:
            if p.id == part_id:
                return p
        return None

topic_service = TopicService()