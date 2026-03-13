"use client";

import { useState } from "react";
import AuthorCard from "./AuthorCard";

interface TimelineEvent {
  year: number;
  type: string;
  label: string;
  authorId?: number;
  authorName?: string;
  category?: string;
}

interface Props {
  event: TimelineEvent;
  onClose: () => void;
}

const TYPE_LABEL: Record<string, string> = {
  birth: "出生",
  death: "逝世",
  work:  "作品出版",
  life:  "生平事件",
  world: "世界大事",
};

export default function EventPanel({ event, onClose }: Props) {
  const [aiText, setAiText] = useState("");
  const [loading, setLoading] = useState(false);

  async function generateLink() {
    if (!event.authorId) return;
    setLoading(true);
    setAiText("");
    try {
      const res = await fetch("/api/ai/generate-link", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          author_id: event.authorId,
          world_event_id: 1,
          relation_type: "influence",
        }),
      });
      const data = await res.json();
      setAiText(data.annotation_zh ?? data.relation_zh ?? "暂无关联数据");
    } catch {
      setAiText("生成失败，请稍后重试。");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="fixed bottom-0 right-0 w-full md:w-96 bg-gray-900 border-t md:border-l border-gray-700 shadow-2xl p-5 z-50">
      <div className="flex justify-between items-start mb-3">
        <div>
          <span className="text-xs bg-gray-700 text-gray-300 px-2 py-0.5 rounded mr-2">
            {TYPE_LABEL[event.type] ?? event.type}
          </span>
          <span className="text-xs text-gray-500">{event.year} 年</span>
        </div>
        <button onClick={onClose} className="text-gray-500 hover:text-gray-200 text-lg leading-none">×</button>
      </div>

      <h3 className="text-base font-semibold text-gray-100 mb-3">{event.label}</h3>

      {event.authorId && event.authorName && (
        <div className="mb-4">
          <AuthorCard authorId={event.authorId} authorName={event.authorName} />
        </div>
      )}

      {event.type === "world" && event.authorId && (
        <button
          onClick={generateLink}
          disabled={loading}
          className="w-full text-sm bg-blue-700 hover:bg-blue-600 disabled:bg-gray-700 text-white rounded-lg px-4 py-2 mb-3 transition-colors"
        >
          {loading ? "AI 生成中…" : "✦ 生成 AI 关联阐释"}
        </button>
      )}

      {aiText && (
        <div className="bg-gray-800 rounded-lg p-3 text-sm text-gray-300 leading-relaxed">
          {aiText}
        </div>
      )}
    </div>
  );
}
