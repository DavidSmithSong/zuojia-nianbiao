"""
作家年表 · 世界历史大事种子数据（古代与中世纪，约 -800 至 1803）
运行：
    DATABASE_URL=postgresql+asyncpg://joker@localhost:5432/zuojia_nianbiao \
    .venv/bin/python -m backend.seed_world_events2
需要环境变量 DATABASE_URL
"""
import asyncio
import os
import sys

# ── 数据定义 ────────────────────────────────────────────────────────────────────
# (year, event_zh, category, significance)
WORLD_EVENTS = [
    # 古希腊/罗马时期 (-800 to 500)
    (-776, "第一届奥林匹克运动会举办", "culture", 4),
    (-490, "马拉松战役，希腊击退波斯", "war", 4),
    (-480, "温泉关战役与萨拉米斯海战", "war", 4),
    (-447, "雅典帕特农神庙开始建造", "culture", 3),
    (-431, "伯罗奔尼撒战争爆发，雅典对抗斯巴达", "war", 4),
    (-399, "苏格拉底被处死", "culture", 5),
    (-334, "亚历山大大帝开始东征", "war", 5),
    (-221, "秦始皇统一六国，建立中国第一个大一统帝国", "politics", 5),
    (-206, "汉朝建立", "politics", 4),
    (-44,  "凯撒遇刺，罗马共和国终结", "politics", 5),
    (-27,  "屋大维建立罗马帝国", "politics", 5),
    (79,   "维苏威火山爆发，庞贝城毁灭", "disaster", 4),
    (105,  "蔡伦改进造纸术（东汉）", "science", 4),
    (220,  "汉朝灭亡，三国时代开始", "politics", 4),
    (313,  "米兰敕令，基督教在罗马合法化", "culture", 4),
    (395,  "罗马帝国东西分裂", "politics", 5),
    (476,  "西罗马帝国灭亡", "politics", 5),
    # 中世纪 (500-1400)
    (618,  "唐朝建立，中国进入盛世", "politics", 5),
    (622,  "穆罕默德迁徙麦地那，伊斯兰历元年", "culture", 5),
    (755,  "安史之乱爆发，唐朝由盛转衰", "war", 5),
    (800,  "查理曼大帝加冕，西方帝国复兴", "politics", 4),
    (960,  "宋朝建立", "politics", 4),
    (1054, "基督教东西方教会大分裂", "culture", 4),
    (1066, "诺曼征服英国，英国语言文化剧变", "war", 4),
    (1096, "第一次十字军东征开始", "war", 4),
    (1206, "成吉思汗统一蒙古，建立蒙古帝国", "politics", 5),
    (1215, "英国《大宪章》签订，限制王权", "politics", 5),
    (1271, "元朝建立，马可·波罗东行", "politics", 4),
    (1347, "黑死病席卷欧洲，欧洲人口锐减三分之一", "disaster", 5),
    (1368, "明朝建立，驱逐蒙元", "politics", 4),
    (1397, "李氏朝鲜建立", "politics", 3),
    # 近代早期 (1400-1803)
    (1453, "拜占庭帝国灭亡，奥斯曼土耳其占领君士坦丁堡", "war", 5),
    (1455, "谷登堡活字印刷《圣经》，印刷术在欧洲普及", "science", 5),
    (1492, "哥伦布抵达美洲，新旧世界相遇", "science", 5),
    (1517, "马丁·路德发表《九十五条论纲》，宗教改革开始", "culture", 5),
    (1543, "哥白尼发表《天体运行论》，日心说确立", "science", 5),
    (1588, "西班牙无敌舰队覆灭，英国称霸海洋", "war", 4),
    (1618, "三十年战争爆发", "war", 4),
    (1644, "清朝建立，明朝灭亡", "politics", 4),
    (1648, "威斯特伐利亚和约，现代国家体系形成", "politics", 4),
    (1687, "牛顿发表《自然哲学的数学原理》", "science", 5),
    (1689, "英国《权利法案》通过，君主立宪制确立", "politics", 4),
    (1762, "卢梭发表《社会契约论》", "culture", 5),
    (1776, "美国《独立宣言》发表", "politics", 5),
    (1789, "法国大革命爆发，人权宣言发表", "politics", 5),
    (1799, "拿破仑政变，执政府成立", "politics", 4),
]


async def seed():
    import asyncpg

    raw_url = os.environ["DATABASE_URL"]
    # asyncpg does not accept the +asyncpg driver prefix used by SQLAlchemy
    url = raw_url.replace("postgresql+asyncpg://", "postgresql://")
    conn = await asyncpg.connect(url)

    inserted = 0
    skipped  = 0
    for row in WORLD_EVENTS:
        year, event_zh, category, significance = row
        existing = await conn.fetchval(
            "SELECT id FROM world_events WHERE year=$1 AND event_zh=$2",
            year, event_zh,
        )
        if existing:
            skipped += 1
            continue
        await conn.execute(
            """INSERT INTO world_events (year, event_zh, category, significance)
               VALUES ($1, $2, $3, $4)""",
            year, event_zh, category, significance,
        )
        inserted += 1

    await conn.close()
    print(f"完成：插入 {inserted} 条，跳过 {skipped} 条（已存在）")


if __name__ == "__main__":
    if "DATABASE_URL" not in os.environ:
        print("请设置 DATABASE_URL 环境变量", file=sys.stderr)
        sys.exit(1)
    asyncio.run(seed())
