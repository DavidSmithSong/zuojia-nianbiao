from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import Author, Work, WorldEvent, AuthorEvent
from ..schemas import TimelineEvent, TimelineResponse

router = APIRouter()


@router.get("", response_model=TimelineResponse)
async def get_timeline(
    from_year: int = Query(1800, alias="from"),
    to_year:   int = Query(2030, alias="to"),
    db: AsyncSession = Depends(get_db),
):
    events: List[TimelineEvent] = []

    # 作家生卒
    authors = (await db.execute(
        select(Author).where(Author.birth >= from_year, Author.birth <= to_year)
    )).scalars().all()
    for a in authors:
        events.append(TimelineEvent(
            year=a.birth, type="birth",
            label=f"{a.name_zh} 出生", author_id=a.id, author_name_zh=a.name_zh,
        ))
        if a.death and from_year <= a.death <= to_year:
            events.append(TimelineEvent(
                year=a.death, type="death",
                label=f"{a.name_zh} 逝世", author_id=a.id, author_name_zh=a.name_zh,
            ))

    # 作品
    works = (await db.execute(
        select(Work).where(Work.year >= from_year, Work.year <= to_year)
    )).scalars().all()
    for w in works:
        events.append(TimelineEvent(
            year=w.year, type="work",
            label=f"《{w.title_zh}》出版", author_id=w.author_id, event_id=w.id,
        ))

    # 作家生平事件
    aevents = (await db.execute(
        select(AuthorEvent).where(AuthorEvent.year >= from_year, AuthorEvent.year <= to_year)
    )).scalars().all()
    for e in aevents:
        events.append(TimelineEvent(
            year=e.year, type="life",
            label=e.event_zh, author_id=e.author_id, event_id=e.id,
        ))

    # 世界大事
    wevents = (await db.execute(
        select(WorldEvent).where(WorldEvent.year >= from_year, WorldEvent.year <= to_year)
    )).scalars().all()
    for e in wevents:
        events.append(TimelineEvent(
            year=e.year, type="world",
            label=e.event_zh, event_id=e.id, category=e.category,
        ))

    events.sort(key=lambda x: x.year)
    return TimelineResponse(from_year=from_year, to_year=to_year, events=events)
