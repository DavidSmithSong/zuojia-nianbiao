/**
 * 作家年表 · 前端 API 客户端
 * 所有请求经 next.config.ts rewrites 代理到 FastAPI 后端
 */

// ── 类型定义 ─────────────────────────────────────────────────────────────────

export interface ApiAuthor {
  id: number;
  name: string;
  name_zh: string;
  birth: number;
  death?: number;
  nationality: string;
  bio_zh?: string;
  portrait_url?: string;
  tags: string[];
}

export interface ApiAuthorDetail extends ApiAuthor {
  works: ApiWork[];
  events: ApiAuthorEvent[];
}

export interface ApiWork {
  id: number;
  title: string;
  title_zh: string;
  year: number;
  genre?: string;
}

export interface ApiAuthorEvent {
  id: number;
  year: number;
  event_zh: string;
  event_type: string;
}

export interface ApiWorldEvent {
  id: number;
  year: number;
  month?: number;
  event_zh: string;
  event_en?: string;
  category: string;
  region?: string;
  significance: number;
}

export interface ApiTimelineEvent {
  year: number;
  type: string;        // "birth" | "death" | "work" | "life" | "world"
  label: string;
  author_id?: number;
  author_name_zh?: string;
  event_id?: number;
  category?: string;
}

export interface ApiTimelineResponse {
  from_year: number;
  to_year: number;
  events: ApiTimelineEvent[];
}

export interface ApiAiLinkOut {
  id: number;
  author_id: number;
  world_event_id: number;
  relation_zh: string;
  relation_type: string;
  confidence: number;
  ai_model: string;
  annotation_zh?: string;
}

// ── 工具函数 ─────────────────────────────────────────────────────────────────

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, init);
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`API ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

// ── 作家 ──────────────────────────────────────────────────────────────────────

export async function fetchAuthors(nationality?: string): Promise<ApiAuthor[]> {
  const url = nationality
    ? `/api/authors?nationality=${encodeURIComponent(nationality)}`
    : `/api/authors`;
  return apiFetch<ApiAuthor[]>(url);
}

export async function fetchAuthor(id: number): Promise<ApiAuthorDetail> {
  return apiFetch<ApiAuthorDetail>(`/api/authors/${id}`);
}

// ── 世界大事 ──────────────────────────────────────────────────────────────────

export async function fetchWorldEvents(params?: {
  category?: string;
  from_year?: number;
  to_year?: number;
}): Promise<ApiWorldEvent[]> {
  const q = new URLSearchParams();
  if (params?.category) q.set("category", params.category);
  if (params?.from_year) q.set("from_year", String(params.from_year));
  if (params?.to_year)   q.set("to_year",   String(params.to_year));
  return apiFetch<ApiWorldEvent[]>(`/api/events?${q}`);
}

// ── 时间线 ────────────────────────────────────────────────────────────────────

export async function fetchTimeline(
  fromYear: number,
  toYear: number
): Promise<ApiTimelineResponse> {
  return apiFetch<ApiTimelineResponse>(
    `/api/timeline?from=${fromYear}&to=${toYear}`
  );
}

// ── AI 关联 ───────────────────────────────────────────────────────────────────

export async function generateAiLink(
  author_id: number,
  world_event_id: number,
  relation_type: "influence" | "response" | "parallel" | "contrast" = "influence"
): Promise<ApiAiLinkOut> {
  return apiFetch<ApiAiLinkOut>("/api/ai/generate-link", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ author_id, world_event_id, relation_type }),
  });
}
