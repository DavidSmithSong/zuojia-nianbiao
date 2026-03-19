"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import ThemeToggle from "@/components/ThemeToggle";
import { PORTRAITS } from "@/components/portraits";
import { fetchAuthor, fetchWorldEvents, generateAiLink, type ApiAuthorDetail, type ApiWorldEvent } from "@/lib/api";

function fmtYear(y: number | null | undefined): string {
  if (y == null) return "至今";
  if (y < 0) return `前${Math.abs(y)}`;
  return String(y);
}

const RELATION_OPTIONS = [
  { value: "influence", label: "影响" },
  { value: "response",  label: "回应" },
  { value: "parallel",  label: "平行" },
  { value: "contrast",  label: "对照" },
] as const;

export default function AuthorDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router  = useRouter();

  const [author, setAuthor]   = useState<ApiAuthorDetail | null>(null);
  const [events, setEvents]   = useState<ApiWorldEvent[]>([]);
  const [loading, setLoading] = useState(true);

  const [selectedEvent, setSelectedEvent]   = useState<ApiWorldEvent | null>(null);
  const [relationType, setRelationType]     = useState<"influence" | "response" | "parallel" | "contrast">("influence");
  const [aiText, setAiText]                 = useState("");
  const [aiLoading, setAiLoading]           = useState(false);

  useEffect(() => {
    Promise.all([
      fetchAuthor(Number(id)),
      fetchWorldEvents(),
    ]).then(([a, e]) => {
      setAuthor(a);
      setEvents(e.filter(ev => ev.significance >= 4));
    }).catch(() => {}).finally(() => setLoading(false));
  }, [id]);

  async function handleGenerateAi() {
    if (!author || !selectedEvent) return;
    setAiLoading(true);
    setAiText("");
    try {
      const data = await generateAiLink(author.id, selectedEvent.id, relationType);
      setAiText(data.annotation_zh ?? data.relation_zh ?? "暂无数据");
    } catch {
      setAiText("生成失败，请稍后重试。");
    } finally {
      setAiLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center t-bg t-text-m">
        加载中…
      </div>
    );
  }

  if (!author) {
    return (
      <div className="min-h-screen flex items-center justify-center t-bg t-text-m">
        作家不存在
      </div>
    );
  }

  const portraitUrl = PORTRAITS[author.name_zh];

  return (
    <div className="min-h-screen t-bg t-text">
      {/* 顶栏 */}
      <header
        className="px-8 py-4 flex items-center justify-between"
        style={{ borderBottom: "1px solid var(--border)" }}
      >
        <button
          onClick={() => router.push("/")}
          className="text-sm t-text-m"
          style={{ display: "flex", alignItems: "center", gap: 4 }}
        >
          ← 返回年表
        </button>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <button
            onClick={() => router.push("/graph")}
            className="text-sm t-text-m"
            style={{ display: "flex", alignItems: "center", gap: 4, background: "none", border: "none", cursor: "pointer" }}
          >
            🕸 关系图
          </button>
          <button
            onClick={() => router.push("/map")}
            className="text-sm t-text-m"
            style={{ display: "flex", alignItems: "center", gap: 4, background: "none", border: "none", cursor: "pointer" }}
          >
            🌍 地图
          </button>
          <ThemeToggle />
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-6 py-10 space-y-10">

        {/* 作家基本信息 */}
        <section className="flex gap-6 items-start">
          {portraitUrl ? (
            <img
              src={portraitUrl}
              alt={author.name_zh}
              style={{
                width: 80, height: 80, borderRadius: "50%",
                objectFit: "cover", flexShrink: 0,
                border: "2px solid var(--border)",
              }}
            />
          ) : (
            <div style={{
              width: 80, height: 80, borderRadius: "50%",
              background: "#1d4ed8", flexShrink: 0,
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: 28, fontWeight: 700, color: "#fff",
            }}>
              {author.name_zh[0]}
            </div>
          )}
          <div className="flex-1">
            <div className="flex items-baseline gap-3 flex-wrap">
              <h1 className="text-3xl font-bold">{author.name_zh}</h1>
              <span className="text-lg t-text-m">{author.name}</span>
            </div>
            <div className="mt-1 flex gap-3 text-sm t-text-m flex-wrap">
              <span>{author.nationality}</span>
              <span>·</span>
              <span>{fmtYear(author.birth)} – {fmtYear(author.death)}</span>
              {author.tags.map(t => (
                <span
                  key={t}
                  className="text-xs px-2 py-0.5 rounded"
                  style={{ background: "var(--surface2)", color: "var(--text-m)" }}
                >
                  {t}
                </span>
              ))}
            </div>
            {author.bio_zh && (
              <p className="mt-4 text-sm leading-relaxed max-w-2xl t-text-m">
                {author.bio_zh}
              </p>
            )}
          </div>
        </section>

        {/* 主要作品 */}
        {author.works.length > 0 && (
          <section>
            <h2
              className="text-lg font-semibold mb-4 pb-2"
              style={{ borderBottom: "1px solid var(--border)" }}
            >
              主要作品
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {author.works.sort((a, b) => a.year - b.year).map(w => (
                <div
                  key={w.id}
                  className="rounded-lg p-4 flex justify-between items-start gap-2"
                  style={{ background: "var(--surface)", border: "1px solid var(--border)" }}
                >
                  <div>
                    <div className="font-medium">《{w.title_zh}》</div>
                    <div className="text-xs mt-0.5 t-text-m">{w.title}</div>
                  </div>
                  <div className="flex flex-col items-end gap-1 shrink-0">
                    <span className="text-sm t-text-m">{fmtYear(w.year)}</span>
                    {w.genre && (
                      <span
                        className="text-xs px-2 py-0.5 rounded"
                        style={{ background: "var(--surface2)", color: "var(--text-m)" }}
                      >
                        {w.genre}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* 生平事件 */}
        {author.events.length > 0 && (
          <section>
            <h2
              className="text-lg font-semibold mb-4 pb-2"
              style={{ borderBottom: "1px solid var(--border)" }}
            >
              生平大事
            </h2>
            <div
              className="relative pl-4 space-y-4"
              style={{ borderLeft: "1px solid var(--border)" }}
            >
              {author.events.sort((a, b) => a.year - b.year).map(e => (
                <div key={e.id} className="relative">
                  <div
                    className="absolute w-2.5 h-2.5 rounded-full"
                    style={{
                      left: "-1.35rem", top: 4,
                      background: "var(--surface2)",
                      border: "2px solid var(--border)",
                    }}
                  />
                  <div className="flex gap-3 items-start">
                    <span className="text-xs t-text-m w-14 shrink-0 pt-0.5">{fmtYear(e.year)}</span>
                    <span className="text-sm leading-relaxed">{e.event_zh}</span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* AI 关联生成 */}
        <section
          className="rounded-xl p-6"
          style={{ background: "var(--surface)", border: "1px solid var(--border)" }}
        >
          <h2 className="text-lg font-semibold mb-4">✦ AI 关联阐释</h2>
          <p className="text-xs t-text-m mb-4">
            选择一个历史事件，让 AI 分析 {author.name_zh} 与它之间的深层关联。
          </p>

          <div className="mb-3">
            <label className="text-xs t-text-m block mb-1">选择历史事件</label>
            <select
              value={selectedEvent?.id ?? ""}
              onChange={e => {
                const ev = events.find(x => x.id === Number(e.target.value));
                setSelectedEvent(ev ?? null);
                setAiText("");
              }}
              className="w-full rounded px-3 py-2 text-sm"
              style={{
                background: "var(--surface2)",
                border: "1px solid var(--border)",
                color: "var(--text)",
              }}
            >
              <option value="">— 请选择 —</option>
              {events.map(e => (
                <option key={e.id} value={e.id}>
                  {e.year}年 · {e.event_zh}
                </option>
              ))}
            </select>
          </div>

          <div className="mb-4">
            <label className="text-xs t-text-m block mb-1">关联类型</label>
            <div className="flex gap-2 flex-wrap">
              {RELATION_OPTIONS.map(opt => (
                <button
                  key={opt.value}
                  onClick={() => setRelationType(opt.value)}
                  className="text-xs px-3 py-1 rounded-full border transition-colors"
                  style={relationType === opt.value
                    ? { background: "#1d4ed8", borderColor: "#1d4ed8", color: "#fff" }
                    : { background: "var(--surface2)", borderColor: "var(--border)", color: "var(--text-m)" }
                  }
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={handleGenerateAi}
            disabled={aiLoading || !selectedEvent}
            className="w-full rounded-lg px-4 py-2.5 text-sm transition-colors"
            style={{
              background: aiLoading || !selectedEvent ? "var(--surface2)" : "#1d4ed8",
              color:      aiLoading || !selectedEvent ? "var(--text-m)"   : "#fff",
              cursor:     aiLoading || !selectedEvent ? "not-allowed"     : "pointer",
            }}
          >
            {aiLoading ? "AI 生成中…" : "生成关联阐释"}
          </button>

          {aiText && (
            <div
              className="mt-4 rounded-lg p-4 text-sm leading-relaxed"
              style={{
                background:   "var(--surface2)",
                borderLeft:   "2px solid #1d4ed8",
                color:        "var(--text)",
              }}
            >
              {aiText}
            </div>
          )}
        </section>

      </div>
    </div>
  );
}
