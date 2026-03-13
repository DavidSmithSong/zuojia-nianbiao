"""
Pydantic 请求/响应模型
"""
from typing import Optional, List
from pydantic import BaseModel


# ── Author ──────────────────────────────────────────────

class WorkOut(BaseModel):
    id: int
    title: str
    title_zh: str
    year: int
    genre: Optional[str] = None

    model_config = {"from_attributes": True}


class AuthorEventOut(BaseModel):
    id: int
    year: int
    event_zh: str
    event_type: str

    model_config = {"from_attributes": True}


class AuthorOut(BaseModel):
    id: int
    name: str
    name_zh: str
    birth: int
    death: Optional[int] = None
    nationality: str
    bio_zh: Optional[str] = None
    portrait_url: Optional[str] = None
    tags: List[str] = []

    model_config = {"from_attributes": True}


class AuthorDetail(AuthorOut):
    works: List[WorkOut] = []
    events: List[AuthorEventOut] = []


class AuthorCreate(BaseModel):
    name: str
    name_zh: str
    birth: int
    death: Optional[int] = None
    nationality: str
    bio_zh: Optional[str] = None
    tags: List[str] = []


# ── WorldEvent ───────────────────────────────────────────

class WorldEventOut(BaseModel):
    id: int
    year: int
    month: Optional[int] = None
    event_zh: str
    event_en: Optional[str] = None
    category: str
    region: Optional[str] = None
    significance: int

    model_config = {"from_attributes": True}


class WorldEventCreate(BaseModel):
    year: int
    month: Optional[int] = None
    event_zh: str
    event_en: Optional[str] = None
    category: str = "general"
    region: Optional[str] = None
    significance: int = 3


# ── Timeline ─────────────────────────────────────────────

class TimelineEvent(BaseModel):
    year: int
    type: str          # "birth" | "death" | "work" | "life" | "world"
    label: str
    author_id: Optional[int] = None
    author_name_zh: Optional[str] = None
    event_id: Optional[int] = None
    category: Optional[str] = None


class TimelineResponse(BaseModel):
    from_year: int
    to_year: int
    events: List[TimelineEvent]


# ── AI ───────────────────────────────────────────────────

class AiLinkRequest(BaseModel):
    author_id: int
    world_event_id: int
    relation_type: str = "influence"   # influence | response | parallel | contrast


class AiLinkOut(BaseModel):
    id: int
    author_id: int
    world_event_id: int
    relation_zh: str
    relation_type: str
    confidence: float
    ai_model: str
    annotation_zh: Optional[str] = None

    model_config = {"from_attributes": True}
