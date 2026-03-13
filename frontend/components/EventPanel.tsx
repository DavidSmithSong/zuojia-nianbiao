"use client";

import { useState, useEffect } from "react";
import AuthorCard from "./AuthorCard";
import { generateAiLink, fetchAuthors, type ApiAuthor, type ApiTimelineEvent } from "../lib/api";

interface Props {
  event: ApiTimelineEvent;
  onClose: () => void;
}

const TYPE_LABEL: Record<string, string> = {
  birth: "出生",
  death: "逝世",
  work:  "作品出版",
  life:  "生平事件",
  world: "世界大事",
};

const RELATION_OPTIONS = [
  { value: "influence", label: "影响" },
  { value: "response",  label: "回应" },
  { value: "parallel",  label: "平行" },
  { value: "contrast",  label: "对照" },
] as const;

export default function EventPanel({ event, onClose }: Props) {
  const [aiText, setAiText]         = useState("");
  const [loading, setLoading]       = useState(false);
  const [authors, setAuthors]       = useState<ApiAuthor[]>([]);
  const [selectedAuthorId, setSelectedAuthorId] = useState<number>(
    event.author_id ?? 0
  );
  const [relationType, setRelationType] = useState<"influence" | "response" | "parallel" | "contrast">("influence");

  // 当面板展示世界大事时，拉取作家列表供选择
  useEffect(() => {
    if (event.type === "world") {
      fetchAuthors().then(setAuthors).catch(() => {});
    }
  }, [event.type]);

  async function handleGenerateLink() {
    const authorId      = event.type === "world" ? selectedAuthorId : (event.author_id ?? 0);
    const worldEventId  = event.type === "world" ? (event.event_id ?? 0) : 0;

    if (!authorId || !worldEventId) return;

    setLoading(true);
    setAiText("");
    try {
      const data = await generateAiLink(authorId, worldEventId, relationType);
      setAiText(data.annotation_zh ?? data.relation_zh ?? "暂无关联数据");
    } catch {
      setAiText("生成失败，请稍后重试。");
    } finally {
      setLoading(false);
    }
  }

  const canGenerateAi =
    event.type === "world" &&
    event.event_id != null &&
    (event.type === "world" ? selectedAuthorId > 0 : (event.author_id ?? 0) > 0);

  return (
    <div className="fixed bottom-0 right-0 w-full md:w-96 bg-gray-900 border-t md:border-l border-gray-700 shadow-2xl p-5 z-50 max-h-[80vh] overflow-y-auto">
      {/* 标题行 */}
      <div className="flex justify-between items-start mb-3">
        <div>
          <span className="text-xs bg-gray-700 text-gray-300 px-2 py-0.5 rounded mr-2">
            {TYPE_LABEL[event.type] ?? event.type}
          </span>
          <span className="text-xs text-gray-500">{event.year} 年</span>
        </div>
        <button
          onClick={onClose}
          className="text-gray-500 hover:text-gray-200 text-lg leading-none"
        >×</button>
      </div>

      <h3 className="text-base font-semibold text-gray-100 mb-3">{event.label}</h3>

      {/* 作家卡片（非世界大事） */}
      {event.author_id && event.author_name_zh && event.type !== "world" && (
        <div className="mb-4">
          <AuthorCard authorId={event.author_id} authorName={event.author_name_zh} />
        </div>
      )}

      {/* 世界大事：AI 关联生成区 */}
      {event.type === "world" && (
        <div className="space-y-3">
          {/* 选择作家 */}
          <div>
            <label className="text-xs text-gray-400 block mb-1">选择作家</label>
            <select
              value={selectedAuthorId}
              onChange={e => setSelectedAuthorId(Number(e.target.value))}
              className="w-full bg-gray-800 border border-gray-700 rounded px-2 py-1.5 text-sm text-gray-100"
            >
              <option value={0}>— 请选择作家 —</option>
              {authors.map(a => (
                <option key={a.id} value={a.id}>
                  {a.name_zh}（{a.birth}–{a.death ?? "今"}）
                </option>
              ))}
            </select>
          </div>

          {/* 选择关联类型 */}
          <div>
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
            onClick={handleGenerateLink}
            disabled={loading || !canGenerateAi}
            className="w-full text-sm bg-blue-700 hover:bg-blue-600 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-lg px-4 py-2 transition-colors"
          >
            {loading ? "AI 生成中…" : "✦ 生成 AI 关联阐释"}
          </button>
        </div>
      )}

      {/* AI 阐释文本 */}
      {aiText && (
        <div className="mt-3 bg-gray-800 rounded-lg p-3 text-sm text-gray-300 leading-relaxed">
          {aiText}
        </div>
      )}
    </div>
  );
}
