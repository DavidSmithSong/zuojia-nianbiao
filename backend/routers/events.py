from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import WorldEvent
from ..schemas import WorldEventOut, WorldEventCreate

router = APIRouter()


@router.get("", response_model=List[WorldEventOut])
async def list_events(
    category: Optional[str] = None,
    from_year: Optional[int] = None,
    to_year: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    q = select(WorldEvent).order_by(WorldEvent.year)
    if category:
        q = q.where(WorldEvent.category == category)
    if from_year:
        q = q.where(WorldEvent.year >= from_year)
    if to_year:
        q = q.where(WorldEvent.year <= to_year)
    result = await db.execute(q)
    return result.scalars().all()


@router.post("", response_model=WorldEventOut, status_code=201)
async def create_event(body: WorldEventCreate, db: AsyncSession = Depends(get_db)):
    event = WorldEvent(**body.model_dump())
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event
