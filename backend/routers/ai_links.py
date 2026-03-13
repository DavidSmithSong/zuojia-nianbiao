from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import Author, WorldEvent, AuthorWorldEventLink, AiAnnotation
from ..schemas import AiLinkRequest, AiLinkOut
from ..services.ai_engine import generate_link

router = APIRouter()


@router.post("/generate-link", response_model=AiLinkOut, status_code=201)
async def create_ai_link(body: AiLinkRequest, db: AsyncSession = Depends(get_db)):
    # 检查是否已存在
    existing = (await db.execute(
        select(AuthorWorldEventLink).where(
            AuthorWorldEventLink.author_id == body.author_id,
            AuthorWorldEventLink.world_event_id == body.world_event_id,
            AuthorWorldEventLink.relation_type == body.relation_type,
        )
    )).scalar_one_or_none()
    if existing:
        return _to_out(existing)

    # 取作家和事件
    author = (await db.execute(select(Author).where(Author.id == body.author_id))).scalar_one_or_none()
    event  = (await db.execute(select(WorldEvent).where(WorldEvent.id == body.world_event_id))).scalar_one_or_none()
    if not author or not event:
        raise HTTPException(status_code=404, detail="作家或事件不存在")

    # 调用 AI 引擎
    result = await generate_link(author, event, body.relation_type)

    link = AuthorWorldEventLink(
        author_id=body.author_id,
        world_event_id=body.world_event_id,
        relation_zh=result["summary"],
        relation_type=body.relation_type,
        confidence=result["confidence"],
        ai_model=result["model"],
    )
    db.add(link)
    await db.flush()

    annotation = AiAnnotation(
        link_id=link.id,
        annotation_zh=result["annotation"],
        prompt_used=result["prompt"],
        model=result["model"],
        tokens_used=result.get("tokens"),
    )
    db.add(annotation)
    await db.commit()
    await db.refresh(link)
    return _to_out(link, annotation)


def _to_out(link: AuthorWorldEventLink, annotation: AiAnnotation = None) -> AiLinkOut:
    return AiLinkOut(
        id=link.id,
        author_id=link.author_id,
        world_event_id=link.world_event_id,
        relation_zh=link.relation_zh,
        relation_type=link.relation_type,
        confidence=float(link.confidence),
        ai_model=link.ai_model or "",
        annotation_zh=annotation.annotation_zh if annotation else None,
    )
