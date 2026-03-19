"""
数据库连接与 ORM 基类
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

import re

_raw = os.environ["DATABASE_URL"]
# 统一转为 asyncpg scheme
_raw = re.sub(r"^postgresql(\+asyncpg)?://", "postgresql+asyncpg://", _raw)
# asyncpg 不支持 sslmode/channel_binding，转为 ssl=require
_raw = re.sub(r"[?&]sslmode=[^&]*", "", _raw)
_raw = re.sub(r"[?&]channel_binding=[^&]*", "", _raw)
DATABASE_URL = _raw

engine = create_async_engine(DATABASE_URL, echo=False, connect_args={"ssl": "require"})
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
