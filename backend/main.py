"""
作家年表 · FastAPI 入口
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import authors, works, events, timeline, ai_links


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="作家年表 API",
    description="交互式作家时间线网站后端接口",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authors.router,  prefix="/api/authors",  tags=["authors"])
app.include_router(works.router,    prefix="/api/works",    tags=["works"])
app.include_router(events.router,   prefix="/api/events",   tags=["events"])
app.include_router(timeline.router, prefix="/api/timeline", tags=["timeline"])
app.include_router(ai_links.router, prefix="/api/ai",       tags=["ai"])


@app.get("/")
async def root():
    return {"status": "ok", "project": "作家年表"}
