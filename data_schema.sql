-- =============================================================================
-- 作家年表 · PostgreSQL 数据库建表语句
-- Project : 交互式作家时间线网站
-- Author  : 宋化富
-- Created : 2026-03-03
-- Version : 1.0
-- =============================================================================
-- 运行方式：
--   psql -U <user> -d <dbname> -f data_schema.sql
-- =============================================================================


-- ---------------------------------------------------------------------------
-- 0. 扩展
-- ---------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "pgcrypto";   -- 用于 gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "unaccent";   -- 用于全文检索去重音


-- ---------------------------------------------------------------------------
-- 1. authors —— 作家基本信息
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS authors (
    id             SERIAL          PRIMARY KEY,
    name           TEXT            NOT NULL,                       -- 英文/拼音名
    name_zh        TEXT            NOT NULL UNIQUE,                -- 中文名（唯一键）
    birth          SMALLINT        NOT NULL,                       -- 出生年份
    death          SMALLINT,                                       -- 逝世年份（在世则为 NULL）
    nationality    TEXT            NOT NULL,                       -- 国籍（中文）
    bio_zh         TEXT,                                           -- 中文简介（约100字）
    portrait_url   TEXT,                                           -- 头像图片 URL
    wikipedia_url  TEXT,                                           -- 维基百科链接
    tags           TEXT[]          DEFAULT '{}',                   -- 标签，如 {现代主义, 魔幻现实主义}
    created_at     TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE  authors              IS '作家基本信息表';
COMMENT ON COLUMN authors.name         IS '作家英文名或罗马化拼音名';
COMMENT ON COLUMN authors.name_zh      IS '作家中文名（主键唯一约束）';
COMMENT ON COLUMN authors.birth        IS '出生年份（公元，负数为公元前）';
COMMENT ON COLUMN authors.death        IS '逝世年份，NULL 表示在世';
COMMENT ON COLUMN authors.tags         IS 'PostgreSQL 数组：文学流派标签';

-- 自动更新 updated_at
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_authors_updated_at
BEFORE UPDATE ON authors
FOR EACH ROW EXECUTE FUNCTION set_updated_at();


-- ---------------------------------------------------------------------------
-- 2. works —— 作品信息
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS works (
    id             SERIAL          PRIMARY KEY,
    author_id      INTEGER         NOT NULL
                       REFERENCES authors(id) ON DELETE CASCADE,
    title          TEXT            NOT NULL,                       -- 原文或英文标题
    title_zh       TEXT            NOT NULL,                       -- 中文标题
    year           SMALLINT        NOT NULL,                       -- 首次出版年份
    genre          TEXT,                                           -- 体裁：小说/诗歌/戏剧/随笔
    language       TEXT,                                           -- 创作语言
    description_zh TEXT,                                           -- 中文简介
    cover_url      TEXT,                                           -- 封面图 URL
    goodreads_id   TEXT,                                           -- Goodreads ID（供API调用）
    isbn           TEXT,                                           -- ISBN-13
    created_at     TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    UNIQUE (author_id, title_zh)                                   -- 同一作家不重复同名中译作品
);

COMMENT ON TABLE  works              IS '作品信息表，与作家一对多关联';
COMMENT ON COLUMN works.year         IS '首次出版年份，连载则取首次发表年';
COMMENT ON COLUMN works.genre        IS '体裁类型，建议使用受控词汇';

CREATE INDEX idx_works_author_id ON works(author_id);
CREATE INDEX idx_works_year      ON works(year);


-- ---------------------------------------------------------------------------
-- 3. world_events —— 世界历史事件
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS world_events (
    id             SERIAL          PRIMARY KEY,
    year           SMALLINT        NOT NULL,                       -- 事件年份
    month          SMALLINT        CHECK (month BETWEEN 1 AND 12),
    day            SMALLINT        CHECK (day   BETWEEN 1 AND 31),
    event_zh       TEXT            NOT NULL,                       -- 事件中文描述
    event_en       TEXT,                                           -- 事件英文描述
    category       TEXT            NOT NULL DEFAULT 'general',     -- 分类：war/politics/culture/science/economy
    region         TEXT,                                           -- 地区：中国/欧洲/美洲/全球…
    significance   SMALLINT        DEFAULT 3
                       CHECK (significance BETWEEN 1 AND 5),      -- 重要程度 1-5
    source_url     TEXT,                                           -- 参考来源 URL
    created_at     TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE  world_events               IS '世界历史事件表（时间线第三轨）';
COMMENT ON COLUMN world_events.category      IS '事件分类：war | politics | culture | science | economy | disaster';
COMMENT ON COLUMN world_events.significance  IS '重要程度：1=次要 … 5=世纪大事';

CREATE INDEX idx_world_events_year     ON world_events(year);
CREATE INDEX idx_world_events_category ON world_events(category);

-- 预置若干世界大事（供演示）
INSERT INTO world_events (year, event_zh, event_en, category, region, significance) VALUES
    (1914, '第一次世界大战爆发',                  'World War I begins',                           'war',      '欧洲', 5),
    (1917, '俄国十月革命',                        'Russian October Revolution',                   'politics', '欧洲', 5),
    (1918, '第一次世界大战结束',                  'World War I ends',                             'war',      '全球', 5),
    (1919, '五四运动（中国）',                    'May Fourth Movement, China',                   'politics', '中国', 5),
    (1929, '全球经济大萧条开始',                  'Great Depression begins',                       'economy',  '全球', 5),
    (1933, '希特勒就任德国总理',                  'Hitler becomes Chancellor of Germany',          'politics', '欧洲', 5),
    (1937, '中国全面抗战爆发（七七事变）',         'Second Sino-Japanese War begins',               'war',      '中国', 5),
    (1939, '第二次世界大战爆发',                  'World War II begins',                           'war',      '全球', 5),
    (1945, '第二次世界大战结束，联合国成立',       'World War II ends; United Nations founded',    'war',      '全球', 5),
    (1949, '中华人民共和国成立',                  'People''s Republic of China founded',           'politics', '中国', 5),
    (1950, '朝鲜战争爆发',                        'Korean War begins',                             'war',      '亚洲', 4),
    (1955, '万隆会议召开',                        'Bandung Conference',                            'politics', '全球', 4),
    (1957, '苏联发射人类首颗人造卫星',             'Sputnik launched',                             'science',  '全球', 5),
    (1966, '中国文化大革命开始',                  'Cultural Revolution begins in China',           'politics', '中国', 5),
    (1969, '人类首次登月',                        'Moon landing (Apollo 11)',                      'science',  '全球', 5),
    (1976, '文化大革命结束，四人帮被捕',           'Cultural Revolution ends; Gang of Four arrested','politics','中国', 5),
    (1989, '柏林墙倒塌',                          'Fall of the Berlin Wall',                       'politics', '欧洲', 5),
    (1991, '苏联解体',                            'Dissolution of the Soviet Union',               'politics', '欧洲', 5),
    (2001, '9·11恐怖袭击',                        'September 11 attacks',                          'war',      '美洲', 5),
    (2008, '全球金融危机',                        'Global Financial Crisis',                       'economy',  '全球', 5),
    (2020, '新冠疫情全球大流行',                  'COVID-19 global pandemic',                      'disaster', '全球', 5)
ON CONFLICT DO NOTHING;


-- ---------------------------------------------------------------------------
-- 4. author_events —— 作家个人年表事件（生平轨）
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS author_events (
    id             SERIAL          PRIMARY KEY,
    author_id      INTEGER         NOT NULL
                       REFERENCES authors(id) ON DELETE CASCADE,
    year           SMALLINT        NOT NULL,                       -- 事件年份
    month          SMALLINT        CHECK (month BETWEEN 1 AND 12),
    event_zh       TEXT            NOT NULL,                       -- 事件描述（中文）
    event_en       TEXT,                                           -- 事件描述（英文，可选）
    event_type     TEXT            DEFAULT 'life',                 -- life/publication/award/travel/death
    source         TEXT,                                           -- 资料来源
    created_at     TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE  author_events            IS '作家个人年表事件（生平轨数据）';
COMMENT ON COLUMN author_events.event_type IS '事件类型：life | publication | award | travel | death';

CREATE INDEX idx_author_events_author_id ON author_events(author_id);
CREATE INDEX idx_author_events_year      ON author_events(year);


-- ---------------------------------------------------------------------------
-- 5. author_world_event_links —— 作家与世界事件的关联（AI引擎产出）
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS author_world_event_links (
    id              SERIAL          PRIMARY KEY,
    author_id       INTEGER         NOT NULL
                        REFERENCES authors(id)       ON DELETE CASCADE,
    world_event_id  INTEGER         NOT NULL
                        REFERENCES world_events(id)  ON DELETE CASCADE,
    relation_zh     TEXT            NOT NULL,                      -- AI生成的关联描述（中文）
    relation_en     TEXT,                                          -- AI生成的关联描述（英文）
    relation_type   TEXT            DEFAULT 'influence',           -- influence/response/parallel/contrast
    confidence      NUMERIC(3,2)    DEFAULT 0.80
                        CHECK (confidence BETWEEN 0 AND 1),       -- AI置信度 0.00-1.00
    ai_model        TEXT,                                          -- 生成该关联使用的AI模型
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    UNIQUE (author_id, world_event_id, relation_type)
);

COMMENT ON TABLE  author_world_event_links             IS '作家与世界事件关联表（AI引擎输出）';
COMMENT ON COLUMN author_world_event_links.relation_type IS 'influence=事件影响作家 | response=作家回应事件 | parallel=平行发生 | contrast=形成对照';
COMMENT ON COLUMN author_world_event_links.confidence  IS 'AI生成置信度，范围0.00~1.00';

CREATE INDEX idx_awel_author_id      ON author_world_event_links(author_id);
CREATE INDEX idx_awel_world_event_id ON author_world_event_links(world_event_id);


-- ---------------------------------------------------------------------------
-- 6. ai_annotations —— AI深层关联批注（长文本，供详情面板展示）
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ai_annotations (
    id              SERIAL          PRIMARY KEY,
    link_id         INTEGER         NOT NULL
                        REFERENCES author_world_event_links(id) ON DELETE CASCADE,
    annotation_zh   TEXT            NOT NULL,                      -- 中文详细阐释（500字以内）
    annotation_en   TEXT,
    prompt_used     TEXT,                                          -- 生成时使用的 prompt（调试用）
    model           TEXT            NOT NULL,                      -- 模型名称（claude-opus-4/gemini-2.0...）
    tokens_used     INTEGER,                                       -- 消耗 token 数
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE ai_annotations IS 'AI生成的作家-事件深度关联批注，与 author_world_event_links 一对一';


-- ---------------------------------------------------------------------------
-- 7. 全文检索视图（供搜索功能使用）
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_author_search AS
SELECT
    a.id,
    a.name_zh,
    a.name,
    a.birth,
    a.death,
    a.nationality,
    a.bio_zh,
    a.tags,
    to_tsvector('simple', coalesce(a.name_zh, '') || ' ' ||
                           coalesce(a.name, '')    || ' ' ||
                           coalesce(a.bio_zh, ''))  AS search_vector,
    ARRAY_AGG(DISTINCT w.title_zh) FILTER (WHERE w.title_zh IS NOT NULL) AS work_titles_zh
FROM authors a
LEFT JOIN works w ON w.author_id = a.id
GROUP BY a.id;

COMMENT ON VIEW v_author_search IS '作家全文搜索视图，汇总作品列表';


-- ---------------------------------------------------------------------------
-- 8. 统计视图
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_timeline_overview AS
SELECT
    generate_series AS year,
    (SELECT COUNT(*) FROM authors    WHERE birth  = generate_series) AS authors_born,
    (SELECT COUNT(*) FROM authors    WHERE death  = generate_series) AS authors_died,
    (SELECT COUNT(*) FROM works      WHERE year   = generate_series) AS works_published,
    (SELECT COUNT(*) FROM world_events WHERE year = generate_series) AS world_events_count
FROM generate_series(1800, 2030);

COMMENT ON VIEW v_timeline_overview IS '时间线总览视图，按年份聚合各类数据量';


-- ---------------------------------------------------------------------------
-- 完成
-- ---------------------------------------------------------------------------
-- 下一步：
--   1. 运行 seed_authors.py --action seed 写入作家数据
--   2. 调用 AI 关联引擎，填充 author_world_event_links 与 ai_annotations
--   3. 接入前端 D3.js 时间线渲染
-- ---------------------------------------------------------------------------
