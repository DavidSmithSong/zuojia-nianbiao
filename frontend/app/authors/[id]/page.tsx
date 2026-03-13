"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { fetchAuthor, fetchWorldEvents, generateAiLink, type ApiAuthorDetail, type ApiWorldEvent } from "@/lib/api";

const RELATION_OPTIONS = [
  { value: "influence", label: "影响" },
  { value: "response",  label: "回应" },
  { value: "parallel",  label: "平行" },
  { value: "contrast",  label: "对照" },
] as const;

const GENRE_COLOR: Record<string, string> = {
  "小说":   "bg-blue-900 text-blue-200",
  "短篇小说": "bg-indigo-900 text-indigo-200",
  "散文":   "bg-green-900 text-green-200",
  "诗歌":   "bg-purple-900 text-purple-200",
  "杂文":   "bg-yellow-900 text-yellow-200",
  "戏剧":   "bg-red-900 text-red-200",
};

export default function AuthorDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router  = useRouter();

  const [author, setAuthor]     = useState<ApiAuthorDetail | null>(null);
  const [events, setEvents]     = useState<ApiWorldEvent[]>([]);
  const [loading, setLoading]   = useState(true);

  // AI 关联面板状态
  const [selectedEvent, setSelectedEvent]     = useState<ApiWorldEvent | null>(null);
  const [relationType, setRelationType]       = useState<"influence" | "response" | "parallel" | "contrast">("influence");
  const [aiText, setAiText]                   = useState("");
  const [aiLoading, setAiLoading]             = useState(false);

  useEffect(() => {
    Promise.all([
      fetchAuthor(Number(id)),
      fetchWorldEvents(),
    ]).then(([a, e]) => {
      setAuthor(a);
      // 只展示重要性 >= 4 的事件
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
      <div className="min-h-screen bg-gray-950 text-gray-400 flex items-center justify-center">
        加载中…
      </div>
    );
  }

  if (!author) {
    return (
      <div className="min-h-screen bg-gray-950 text-gray-400 flex items-center justify-center">
        作家不存在
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      {/* 顶栏 */}
      <header className="px-8 py-4 border-b border-gray-800 flex items-center gap-4">
        <button
          onClick={() => router.push("/")}
          className="text-gray-500 hover:text-gray-200 text-sm flex items-center gap-1"
        >
          ← 返回年表
        </button>
      </header>

      <div className="max-w-4xl mx-auto px-6 py-10 space-y-10">

        {/* 作家基本信息 */}
        <section className="flex gap-6 items-start">
          <div className="w-16 h-16 rounded-full bg-blue-700 flex items-center justify-center text-2xl font-bold shrink-0">
            {author.name_zh[0]}
          </div>
          <div className="flex-1">
            <div className="flex items-baseline gap-3 flex-wrap">
              <h1 className="text-3xl font-bold">{author.name_zh}</h1>
              <span className="text-gray-400 text-lg">{author.name}</span>
            </div>
            <div className="mt-1 flex gap-3 text-sm text-gray-500 flex-wrap">
              <span>{author.nationality}</span>
              <span>·</span>
              <span>{author.birth} – {author.death ?? "至今"}</span>
              {author.tags.map(t => (
                <span key={t} className="bg-gray-800 px-2 py-0.5 rounded text-xs text-gray-400">{t}</span>
              ))}
            </div>
            {author.bio_zh && (
              <p className="mt-4 text-gray-300 leading-relaxed text-sm max-w-2xl">
                {author.bio_zh}
              </p>
            )}
          </div>
        </section>

        {/* 主要作品 */}
        {author.works.length > 0 && (
          <section>
            <h2 className="text-lg font-semibold text-gray-200 mb-4 border-b border-gray-800 pb-2">
              主要作品
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {author.works.sort((a, b) => a.year - b.year).map(w => (
                <div key={w.id} className="bg-gray-900 rounded-lg p-4 flex justify-between items-start gap-2">
                  <div>
                    <div className="font-medium text-gray-100">《{w.title_zh}》</div>
                    <div className="text-xs text-gray-500 mt-0.5">{w.title}</div>
                  </div>
                  <div className="flex flex-col items-end gap-1 shrink-0">
                    <span className="text-sm text-gray-500">{w.year}</span>
                    {w.genre && (
                      <span className={`text-xs px-2 py-0.5 rounded ${GENRE_COLOR[w.genre] ?? "bg-gray-800 text-gray-400"}`}>
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
            <h2 className="text-lg font-semibold text-gray-200 mb-4 border-b border-gray-800 pb-2">
              生平大事
            </h2>
            <div className="relative pl-4 border-l border-gray-800 space-y-4">
              {author.events.sort((a, b) => a.year - b.year).map(e => (
                <div key={e.id} className="relative">
                  <div className="absolute -left-[1.35rem] top-1 w-2.5 h-2.5 rounded-full bg-gray-600 border-2 border-gray-950" />
                  <div className="flex gap-3 items-start">
                    <span className="text-xs text-gray-600 w-10 shrink-0 pt-0.5">{e.year}</span>
                    <span className="text-sm text-gray-300 leading-relaxed">{e.event_zh}</span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* AI 关联生成 */}
        <section className="bg-gray-900 rounded-xl p-6">
          <h2 className="text-lg font-semibold text-gray-200 mb-4">
            ✦ AI 关联阐释
          </h2>
          <p className="text-xs text-gray-500 mb-4">
            选择一个历史事件，让 AI 分析 {author.name_zh} 与它之间的深层关联。
          </p>

          {/* 选择历史事件 */}
          <div className="mb-3">
            <label className="text-xs text-gray-400 block mb-1">选择历史事件</label>
            <select
              value={selectedEvent?.id ?? ""}
              onChange={e => {
                const ev = events.find(x => x.id === Number(e.target.value));
                setSelectedEvent(ev ?? null);
                setAiText("");
              }}
              className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-sm text-gray-100"
            >
              <option value="">— 请选择 —</option>
              {events.map(e => (
                <option key={e.id} value={e.id}>
                  {e.year}年 · {e.event_zh}
                </option>
              ))}
            </select>
          </div>

          {/* 关联类型 */}
          <div className="mb-4">
            <label className="text-xs text-gray-400 block mb-1">关联类型</label>
            <div className="flex gap-2 flex-wrap">
              {RELATION_OPTIONS.map(opt => (
                <button
                  key={opt.value}
                  onClick={() => setRelationType(opt.value)}
                  className={`text-xs px-3 py-1 rounded-full border transition-colors ${
                    relationType === opt.value
                      ? "bg-blue-700 border-blue-600 text-white"
                      : "bg-gray-800 border-gray-700 text-gray-400 hover:border-gray-500"
                  }`}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={handleGenerateAi}
            disabled={aiLoading || !selectedEvent}
            className="w-full bg-blue-700 hover:bg-blue-600 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-lg px-4 py-2.5 text-sm transition-colors"
          >
            {aiLoading ? "AI 生成中…" : "生成关联阐释"}
          </button>

          {aiText && (
            <div className="mt-4 bg-gray-800 rounded-lg p-4 text-sm text-gray-300 leading-relaxed border-l-2 border-blue-700">
              {aiText}
            </div>
          )}
        </section>

      </div>
    </div>
  );
}
