# 作家年表 · 项目说明

> **宋化富 · 交互式作家时间线网站**
> 创建日期：2026-03-03

---

## 项目愿景

将世界文学史变成一张可以探索的地图。

每位作家的生命、作品、所处时代以三条平行轨道并列展示，读者可以直观看到：
《百年孤独》诞生时，世界正在发生什么？鲁迅弃医从文那一年，卡夫卡在写什么？
AI 引擎自动挖掘这些跨越时空的深层关联，让文学阅读从孤立的文本体验升维为历史的立体感知。

---

## 目录结构

```
作家年表/
├── seed_authors.py         # Python 数据初始化脚本（20位作家 · 本文件）
├── data_schema.sql         # PostgreSQL 建表语句
├── README_作家年表.md       # 本文件
│
├── frontend/               # 前端（待创建）
│   ├── components/
│   │   ├── Timeline.tsx    # D3.js 三轨时间线主组件
│   │   ├── AuthorCard.tsx  # 作家悬浮卡片
│   │   └── EventPanel.tsx  # 事件详情面板（含 AI 关联）
│   └── pages/
│       ├── index.tsx       # 首页 · 时间线入口
│       └── author/[id].tsx # 作家个人页
│
├── backend/                # 后端（待创建）
│   ├── main.py             # FastAPI 入口
│   ├── routers/
│   │   ├── authors.py      # /api/authors CRUD
│   │   ├── events.py       # /api/events
│   │   └── ai_links.py     # /api/ai/generate-link
│   └── services/
│       └── ai_engine.py    # Claude / Gemini API 调用
│
└── scripts/                # 工具脚本（待创建）
    ├── fetch_random_house.py  # 爬取兰登书屋100部数据
    └── bulk_ai_annotate.py    # 批量生成 AI 关联
```

---

## 技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| 前端框架 | Next.js 14 (App Router) | React 服务端渲染，SEO 友好 |
| 可视化 | D3.js v7 | 三轨时间线 SVG 渲染 |
| 样式 | Tailwind CSS | 快速布局 |
| 后端 | FastAPI (Python 3.12) | 高性能 REST API |
| 数据库 | PostgreSQL 16 | 结构化存储 + 全文检索 |
| ORM | SQLAlchemy 2.0 | 异步查询 |
| AI 引擎 | Claude API (claude-opus-4) | 作家-事件深层关联生成 |
| AI 备用 | Gemini 2.0 API | 多模型交叉验证 |
| 部署 | Vercel（前端）+ Railway/Fly.io（后端）| |

---

## 数据库表结构

```
authors                     -- 作家基本信息
  └── works                 -- 作品（一对多）
  └── author_events         -- 作家生平事件（一对多）
  └── author_world_event_links  -- 作家与世界事件关联（多对多中间表）
        └── ai_annotations  -- AI 生成的深度阐释（一对一）

world_events                -- 世界历史事件（独立表）

视图：
  v_author_search           -- 全文搜索视图
  v_timeline_overview       -- 时间线年度统计视图
```

---

## 快速开始

### 1. 初始化数据库

```bash
# 创建数据库
createdb zuojia_nianbiao

# 建表
psql -U postgres -d zuojia_nianbiao -f data_schema.sql
```

### 2. 初始化作家数据

```bash
# 安装依赖
pip install psycopg2-binary

# 查看数据摘要（无需数据库）
python seed_authors.py --action summary

# 导出为 JSON（无需数据库）
python seed_authors.py --action json --output authors_seed.json

# 写入 PostgreSQL
export DATABASE_URL="postgresql://postgres:password@localhost:5432/zuojia_nianbiao"
python seed_authors.py --action seed
```

### 3. 启动后端（后续步骤）

```bash
cd backend
pip install fastapi uvicorn sqlalchemy asyncpg
uvicorn main:app --reload --port 8000
```

### 4. 启动前端（后续步骤）

```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:3000
```

---

## 初始数据：20位作家

### 中国作家（10位）

| 作家 | 生卒年 | 代表作 |
|------|--------|--------|
| 鲁迅 | 1881-1936 | 《狂人日记》《阿Q正传》《呐喊》 |
| 张爱玲 | 1920-1995 | 《倾城之恋》《金锁记》 |
| 沈从文 | 1902-1988 | 《边城》《长河》 |
| 余华 | 1960- | 《活着》《许三观卖血记》《兄弟》 |
| 莫言 | 1955- | 《红高粱家族》《蛙》（2012诺贝尔奖） |
| 巴金 | 1904-2005 | 《家》《春》《秋》《随想录》 |
| 老舍 | 1899-1966 | 《骆驼祥子》《茶馆》 |
| 冰心 | 1900-1999 | 《繁星》《春水》《寄小读者》 |
| 汪曾祺 | 1920-1997 | 《受戒》《大淖记事》 |
| 残雪 | 1953- | 《黄泥街》《最后的情人》 |

### 西方作家（10位）

| 作家 | 生卒年 | 代表作 |
|------|--------|--------|
| 卡夫卡 | 1883-1924 | 《变形记》《审判》《城堡》 |
| 博尔赫斯 | 1899-1986 | 《虚构集》《阿莱夫》 |
| 加缪 | 1913-1960 | 《局外人》《鼠疫》（1957诺贝尔奖） |
| 陀思妥耶夫斯基 | 1821-1881 | 《罪与罚》《卡拉马佐夫兄弟》 |
| 福克纳 | 1897-1962 | 《喧哗与骚动》（1949诺贝尔奖） |
| 海明威 | 1899-1961 | 《老人与海》（1954诺贝尔奖） |
| 伍尔夫 | 1882-1941 | 《达洛维夫人》《到灯塔去》 |
| 加西亚·马尔克斯 | 1927-2014 | 《百年孤独》（1982诺贝尔奖） |
| 卡尔维诺 | 1923-1985 | 《看不见的城市》《如果在冬夜，一个旅人》 |
| 托卡尔丘克 | 1962- | 《航班》《雅各书》（2018诺贝尔奖） |

---

## 下一步计划

### 阶段一：数据层（当前）
- [x] 设计 PostgreSQL 数据库 Schema
- [x] 编写 20 位核心作家种子数据
- [ ] 爬取兰登书屋百部书单，扩展至 100 位作家
- [ ] 整理 1800-2026 年世界历史大事（约 500 条）

### 阶段二：API 层
- [ ] 搭建 FastAPI 项目框架
- [ ] 实现 `/api/authors`、`/api/works`、`/api/events` 基础 CRUD
- [ ] 实现 `/api/timeline?from=1900&to=1950` 时间段查询接口
- [ ] 集成 Claude API，实现 `/api/ai/generate-link` 端点

### 阶段三：前端层
- [ ] Next.js 项目初始化（App Router + TypeScript）
- [ ] D3.js 三轨时间线原型（仅静态数据）
- [ ] 作家卡片悬浮详情组件
- [ ] AI 关联展示面板（流式输出）
- [ ] 全局搜索（作家 / 作品 / 事件）

### 阶段四：AI 关联引擎
- [ ] 设计 Prompt 模板：给定作家 + 世界事件 → 生成关联阐释
- [ ] 批量预生成高优先级关联（诺贝尔奖得主 × 重大历史事件）
- [ ] 实现用户触发的实时生成（首次点击时调用 API）
- [ ] Gemini / Claude 双模型交叉验证机制

### 阶段五：发布
- [ ] 部署前端至 Vercel
- [ ] 部署后端至 Railway
- [ ] 配置自定义域名
- [ ] SEO 优化（作家个人页静态生成）

---

## AI 关联引擎设计思路

**核心 Prompt 结构：**

```
你是一位精通文学史与世界历史的学者。

作家：{name_zh}（{birth}-{death}，{nationality}）
历史事件：{year}年，{event_zh}

请用200字以内的中文，阐述这位作家与这一历史事件之间的深层关联。
要求：
1. 分析事件对作家创作的具体影响（或作家对事件的回应）
2. 引用作家具体作品或言论作为佐证
3. 语言生动，避免泛泛而谈
4. 若两者之间无显著关联，请如实说明
```

**关联类型分类：**
- `influence`：历史事件直接影响了作家的创作题材、风格或人生轨迹
- `response`：作家通过作品或言论直接回应了该事件
- `parallel`：事件与作家的某部作品在主题或时间上形成平行共鸣
- `contrast`：事件与作家的世界形成鲜明对照，产生张力

---

## 参考资源

- [兰登书屋现代文库100部最佳英语小说](https://www.modernlibrary.com/top-100/100-best-novels/)
- [诺贝尔文学奖历届得主](https://www.nobelprize.org/prizes/literature/)
- [古腾堡计划（免费电子书）](https://www.gutenberg.org/)
- [Open Library API](https://openlibrary.org/developers/api)
- [Wikidata 作家数据](https://www.wikidata.org/)
- Claude API 文档：https://docs.anthropic.com/
- D3.js 时间线教程：https://observablehq.com/@d3/timeline

---

*由宋化富发起 · Claude Code 协助搭建 · 2026年3月*
