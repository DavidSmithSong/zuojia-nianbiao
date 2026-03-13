from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import Work
from ..schemas import WorkOut

router = APIRouter()


@router.get("", response_model=List[WorkOut])
async def list_works(author_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Work).where(Work.author_id == author_id).order_by(Work.year)
    )
    return result.scalars().all()


@router.get("/{work_id}", response_model=WorkOut)
async def get_work(work_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Work).where(Work.id == work_id))
    work = result.scalar_one_or_none()
    if not work:
        raise HTTPException(status_code=404, detail="作品不存在")
    return work
