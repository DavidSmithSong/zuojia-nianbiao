"""
作家年表 · 批量预生成 AI 关联

功能：为指定作家 × 重大历史事件（significance >= 4）批量调用后端 AI 接口，
      将结果持久化到 author_world_event_links + ai_annotations 表。

用法：
    pip install httpx asyncpg
    DATABASE_URL=postgresql://... BACKEND_URL=http://localhost:8000 python scripts/batch_ai_generate.py

可选参数（命令行）：
    --min-sig 4          最低重要性级别（默认 4）
    --relation influence  关联类型（默认 influence）
    --delay 2            每次请求之间的间隔秒数（默认 2，避免触发 API 限速）
    --authors 鲁迅,余华  仅处理指定作家（逗号分隔，默认全部）
"""
import argparse
import asyncio
import os
import sys
import time

import httpx


BACKEND = os.environ.get("BACKEND_URL", "http://localhost:8000")


async def get_authors(client: httpx.AsyncClient) -> list[dict]:
    r = await client.get(f"{BACKEND}/api/authors")
    r.raise_for_status()
    return r.json()


async def get_world_events(client: httpx.AsyncClient, min_sig: int) -> list[dict]:
    r = await client.get(f"{BACKEND}/api/events")
    r.raise_for_status()
    return [e for e in r.json() if e["significance"] >= min_sig]


async def generate_link(
    client: httpx.AsyncClient,
    author_id: int,
    event_id: int,
    relation_type: str,
) -> dict | None:
    try:
        r = await client.post(
            f"{BACKEND}/api/ai/generate-link",
            json={
                "author_id": author_id,
                "world_event_id": event_id,
                "relation_type": relation_type,
            },
            timeout=60.0,
        )
        if r.status_code == 201:
            return r.json()
        if r.status_code == 200:
            return r.json()   # already exists
        print(f"    ⚠ 跳过 ({r.status_code}): {r.text[:80]}")
    except httpx.ReadTimeout:
        print("    ⚠ 超时，跳过")
    return None


async def main(args: argparse.Namespace) -> None:
    async with httpx.AsyncClient() as client:
        print("获取作家列表…")
        authors = await get_authors(client)

        if args.authors:
            names = set(args.authors.split(","))
            authors = [a for a in authors if a["name_zh"] in names]
        print(f"  作家数：{len(authors)}")

        print(f"获取世界大事（significance >= {args.min_sig}）…")
        events = await get_world_events(client, args.min_sig)
        print(f"  事件数：{len(events)}")

        total   = len(authors) * len(events)
        done    = 0
        success = 0
        start   = time.monotonic()

        for author in authors:
            for event in events:
                done += 1
                label = f"[{done}/{total}] {author['name_zh']} × {event['year']} {event['event_zh'][:20]}"
                print(f"  {label}…", end=" ", flush=True)

                result = await generate_link(
                    client, author["id"], event["id"], args.relation
                )
                if result:
                    success += 1
                    conf = result.get("confidence", "?")
                    print(f"✓ (置信度 {conf})")
                else:
                    print("✗")

                await asyncio.sleep(args.delay)

        elapsed = time.monotonic() - start
        print(f"\n完成：{success}/{total} 成功，耗时 {elapsed:.0f}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量预生成 AI 关联")
    parser.add_argument("--min-sig",  type=int,   default=4,          dest="min_sig")
    parser.add_argument("--relation", type=str,   default="influence")
    parser.add_argument("--delay",    type=float, default=2.0)
    parser.add_argument("--authors",  type=str,   default="",         help="逗号分隔的作家名（中文），留空表示全部")
    args = parser.parse_args()

    if not BACKEND:
        print("请设置 BACKEND_URL 环境变量", file=sys.stderr)
        sys.exit(1)

    asyncio.run(main(args))
