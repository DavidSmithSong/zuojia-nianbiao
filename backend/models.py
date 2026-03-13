"""
SQLAlchemy ORM 模型（对应 data_schema.sql）
"""
from datetime import datetime
from typing import Optional, List

from sqlalchemy import (
    Integer, SmallInteger, Text, Numeric, ARRAY,
    ForeignKey, UniqueConstraint, CheckConstraint, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import TIMESTAMPTZ

from .database import Base


class Author(Base):
    __tablename__ = "authors"

    id:            Mapped[int]           = mapped_column(Integer, primary_key=True)
    name:          Mapped[str]           = mapped_column(Text, nullable=False)
    name_zh:       Mapped[str]           = mapped_column(Text, nullable=False, unique=True)
    birth:         Mapped[int]           = mapped_column(SmallInteger, nullable=False)
    death:         Mapped[Optional[int]] = mapped_column(SmallInteger)
    nationality:   Mapped[str]           = mapped_column(Text, nullable=False)
    bio_zh:        Mapped[Optional[str]] = mapped_column(Text)
    portrait_url:  Mapped[Optional[str]] = mapped_column(Text)
    wikipedia_url: Mapped[Optional[str]] = mapped_column(Text)
    tags:          Mapped[List[str]]     = mapped_column(ARRAY(Text), server_default="{}")
    created_at:    Mapped[datetime]      = mapped_column(TIMESTAMPTZ, server_default=func.now())
    updated_at:    Mapped[datetime]      = mapped_column(TIMESTAMPTZ, server_default=func.now())

    works:         Mapped[List["Work"]]        = relationship(back_populates="author", cascade="all, delete")
    events:        Mapped[List["AuthorEvent"]] = relationship(back_populates="author", cascade="all, delete")


class Work(Base):
    __tablename__ = "works"
    __table_args__ = (UniqueConstraint("author_id", "title_zh"),)

    id:             Mapped[int]           = mapped_column(Integer, primary_key=True)
    author_id:      Mapped[int]           = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
    title:          Mapped[str]           = mapped_column(Text, nullable=False)
    title_zh:       Mapped[str]           = mapped_column(Text, nullable=False)
    year:           Mapped[int]           = mapped_column(SmallInteger, nullable=False)
    genre:          Mapped[Optional[str]] = mapped_column(Text)
    language:       Mapped[Optional[str]] = mapped_column(Text)
    description_zh: Mapped[Optional[str]] = mapped_column(Text)
    cover_url:      Mapped[Optional[str]] = mapped_column(Text)
    created_at:     Mapped[datetime]      = mapped_column(TIMESTAMPTZ, server_default=func.now())

    author: Mapped["Author"] = relationship(back_populates="works")


class WorldEvent(Base):
    __tablename__ = "world_events"

    id:           Mapped[int]           = mapped_column(Integer, primary_key=True)
    year:         Mapped[int]           = mapped_column(SmallInteger, nullable=False)
    month:        Mapped[Optional[int]] = mapped_column(SmallInteger)
    day:          Mapped[Optional[int]] = mapped_column(SmallInteger)
    event_zh:     Mapped[str]           = mapped_column(Text, nullable=False)
    event_en:     Mapped[Optional[str]] = mapped_column(Text)
    category:     Mapped[str]           = mapped_column(Text, nullable=False, server_default="general")
    region:       Mapped[Optional[str]] = mapped_column(Text)
    significance: Mapped[int]           = mapped_column(SmallInteger, server_default="3")
    source_url:   Mapped[Optional[str]] = mapped_column(Text)
    created_at:   Mapped[datetime]      = mapped_column(TIMESTAMPTZ, server_default=func.now())


class AuthorEvent(Base):
    __tablename__ = "author_events"

    id:         Mapped[int]           = mapped_column(Integer, primary_key=True)
    author_id:  Mapped[int]           = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
    year:       Mapped[int]           = mapped_column(SmallInteger, nullable=False)
    month:      Mapped[Optional[int]] = mapped_column(SmallInteger)
    event_zh:   Mapped[str]           = mapped_column(Text, nullable=False)
    event_en:   Mapped[Optional[str]] = mapped_column(Text)
    event_type: Mapped[str]           = mapped_column(Text, server_default="life")
    source:     Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime]      = mapped_column(TIMESTAMPTZ, server_default=func.now())

    author: Mapped["Author"] = relationship(back_populates="events")


class AuthorWorldEventLink(Base):
    __tablename__ = "author_world_event_links"
    __table_args__ = (UniqueConstraint("author_id", "world_event_id", "relation_type"),)

    id:             Mapped[int]           = mapped_column(Integer, primary_key=True)
    author_id:      Mapped[int]           = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
    world_event_id: Mapped[int]           = mapped_column(ForeignKey("world_events.id", ondelete="CASCADE"))
    relation_zh:    Mapped[str]           = mapped_column(Text, nullable=False)
    relation_en:    Mapped[Optional[str]] = mapped_column(Text)
    relation_type:  Mapped[str]           = mapped_column(Text, server_default="influence")
    confidence:     Mapped[float]         = mapped_column(Numeric(3, 2), server_default="0.80")
    ai_model:       Mapped[Optional[str]] = mapped_column(Text)
    created_at:     Mapped[datetime]      = mapped_column(TIMESTAMPTZ, server_default=func.now())

    annotation: Mapped[Optional["AiAnnotation"]] = relationship(back_populates="link", cascade="all, delete")


class AiAnnotation(Base):
    __tablename__ = "ai_annotations"

    id:             Mapped[int]           = mapped_column(Integer, primary_key=True)
    link_id:        Mapped[int]           = mapped_column(ForeignKey("author_world_event_links.id", ondelete="CASCADE"))
    annotation_zh:  Mapped[str]           = mapped_column(Text, nullable=False)
    annotation_en:  Mapped[Optional[str]] = mapped_column(Text)
    prompt_used:    Mapped[Optional[str]] = mapped_column(Text)
    model:          Mapped[str]           = mapped_column(Text, nullable=False)
    tokens_used:    Mapped[Optional[int]] = mapped_column(Integer)
    created_at:     Mapped[datetime]      = mapped_column(TIMESTAMPTZ, server_default=func.now())

    link: Mapped["AuthorWorldEventLink"] = relationship(back_populates="annotation")
