from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import Author
from ..schemas import AuthorOut, AuthorDetail, AuthorCreate

router = APIRouter()


@router.get("", response_model=List[AuthorOut])
async def list_authors(
    nationality: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    q = select(Author).order_by(Author.birth)
    if nationality:
        q = q.where(Author.nationality.contains(nationality))
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{author_id}", response_model=AuthorDetail)
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)):
    q = (
        select(Author)
        .where(Author.id == author_id)
        .options(selectinload(Author.works), selectinload(Author.events))
    )
    result = await db.execute(q)
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="作家不存在")
    return author


@router.post("", response_model=AuthorOut, status_code=201)
async def create_author(body: AuthorCreate, db: AsyncSession = Depends(get_db)):
    author = Author(**body.model_dump())
    db.add(author)
    await db.commit()
    await db.refresh(author)
    return author
