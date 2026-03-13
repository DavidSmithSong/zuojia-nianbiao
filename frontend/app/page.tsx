"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Timeline from "@/components/Timeline";
import SearchBar from "@/components/SearchBar";
import { fetchAuthors, type ApiAuthor } from "@/lib/api";

const NAT_FILTERS = [
  { label: "全部", value: "" },
  { label: "中国", value: "中国" },
  { label: "西方", value: "西方" },
];

export default function Home() {
  const router  = useRouter();
  const [authors, setAuthors]     = useState<ApiAuthor[]>([]);
  const [natFilter, setNatFilter] = useState("");
  const [sideOpen, setSideOpen]   = useState(false);

  useEffect(() => {
    fetchAuthors().then(setAuthors).catch(() => {});
  }, []);

  const displayAuthors = natFilter
    ? authors.filter(a => a.nationality.includes(natFilter))
    : authors;

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 flex flex-col">
      {/* 顶部导航栏 */}
      <header className="px-6 py-4 border-b border-gray-800 flex items-center justify-between gap-4 flex-wrap shrink-0">
        <div className="flex items-center gap-4">
          <button
            onClick={() => setSideOpen(v => !v)}
            className="text-gray-500 hover:text-gray-200 text-lg leading-none"
            title="作家列表"
          >☰</button>
          <div>
            <h1 className="text-xl font-bold tracking-wide leading-tight">作家年表</h1>
            <p className="text-gray-500 text-xs">将世界文学史变成一张可以探索的地图</p>
          </div>
        </div>
        <SearchBar />
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* 作家侧栏 */}
        {sideOpen && (
          <aside className="w-56 border-r border-gray-800 bg-gray-950 flex flex-col shrink-0 overflow-hidden">
            {/* 国籍筛选 */}
            <div className="px-3 py-3 border-b border-gray-800 flex gap-1">
              {NAT_FILTERS.map(f => (
                <button
                  key={f.value}
                  onClick={() => setNatFilter(f.value)}
                  className={`flex-1 text-xs py-1 rounded transition-colors ${
                    natFilter === f.value
                      ? "bg-blue-700 text-white"
                      : "bg-gray-800 text-gray-400 hover:bg-gray-700"
                  }`}
                >
                  {f.label}
                </button>
              ))}
            </div>

            {/* 作家列表 */}
            <ul className="overflow-y-auto flex-1">
              {displayAuthors.map(a => (
                <li key={a.id}>
                  <button
                    className="w-full text-left px-3 py-2.5 hover:bg-gray-800 transition-colors flex items-center gap-2.5 border-b border-gray-900"
                    onClick={() => router.push(`/authors/${a.id}`)}
                  >
                    <span className="w-7 h-7 rounded-full bg-blue-700 flex items-center justify-center text-white text-xs font-bold shrink-0">
                      {a.name_zh[0]}
                    </span>
                    <span className="flex flex-col min-w-0">
                      <span className="text-sm text-gray-100 truncate">{a.name_zh}</span>
                      <span className="text-xs text-gray-600">{a.birth}–{a.death ?? "今"}</span>
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          </aside>
        )}

        {/* 主内容：时间线 */}
        <main className="flex-1 overflow-auto">
          <Timeline />
        </main>
      </div>
    </div>
  );
}
