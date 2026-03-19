"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Timeline from "@/components/Timeline";
import SearchBar from "@/components/SearchBar";
import ThemeToggle from "@/components/ThemeToggle";
import { PORTRAITS } from "@/components/portraits";
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
    <div className="min-h-screen flex flex-col t-bg t-text">
      {/* 顶部导航栏 */}
      <header
        className="px-6 py-4 flex items-center justify-between gap-4 flex-wrap shrink-0 t-border"
        style={{ borderBottom: "1px solid var(--border)" }}
      >
        <div className="flex items-center gap-4">
          <button
            onClick={() => setSideOpen(v => !v)}
            className="text-lg leading-none t-text-m"
            title="作家列表"
          >☰</button>
          <div>
            <h1 className="text-xl font-bold tracking-wide leading-tight">作家年表</h1>
            <p className="text-xs t-text-m">将世界文学史变成一张可以探索的地图</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <SearchBar />
          <a
            href="https://davidsmithsong.github.io/green-light/"
            className="text-xs t-text-m"
            style={{ textDecoration: "none" }}
            title="绿光考研"
          >📚 考研</a>
          <button
            onClick={() => router.push("/map")}
            className="text-xs t-text-m"
            style={{ background: "none", border: "none", cursor: "pointer" }}
            title="文学地图"
          >🌍 地图</button>
          <button
            onClick={() => router.push("/graph")}
            className="text-xs t-text-m"
            style={{ background: "none", border: "none", cursor: "pointer" }}
            title="文学关系图"
          >🕸 关系图</button>
          <ThemeToggle />
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* 作家侧栏 */}
        {sideOpen && (
          <aside
            className="w-56 flex flex-col shrink-0 overflow-hidden t-surface"
            style={{ borderRight: "1px solid var(--border)" }}
          >
            {/* 国籍筛选 */}
            <div
              className="px-3 py-3 flex gap-1"
              style={{ borderBottom: "1px solid var(--border)" }}
            >
              {NAT_FILTERS.map(f => (
                <button
                  key={f.value}
                  onClick={() => setNatFilter(f.value)}
                  className="flex-1 text-xs py-1 rounded transition-colors"
                  style={natFilter === f.value
                    ? { background: "#1d4ed8", color: "#fff" }
                    : { background: "var(--surface2)", color: "var(--text-m)" }
                  }
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
                    className="w-full text-left px-3 py-2.5 transition-colors flex items-center gap-2.5"
                    style={{ borderBottom: "1px solid var(--border)" }}
                    onClick={() => router.push(`/authors/${a.id}`)}
                    onMouseEnter={e => (e.currentTarget.style.background = "var(--surface2)")}
                    onMouseLeave={e => (e.currentTarget.style.background = "")}
                  >
                    {PORTRAITS[a.name_zh] ? (
                      <img
                        src={PORTRAITS[a.name_zh]}
                        alt={a.name_zh}
                        className="w-7 h-7 rounded-full object-cover shrink-0"
                      />
                    ) : (
                      <span className="w-7 h-7 rounded-full bg-blue-700 flex items-center justify-center text-white text-xs font-bold shrink-0">
                        {a.name_zh[0]}
                      </span>
                    )}
                    <span className="flex flex-col min-w-0">
                      <span className="text-sm truncate t-text">{a.name_zh}</span>
                      <span className="text-xs t-text-m">{a.birth}–{a.death ?? "今"}</span>
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
