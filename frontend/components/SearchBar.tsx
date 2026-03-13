"use client";

import { useState, useEffect, useRef } from "react";
import { fetchAuthors, type ApiAuthor } from "../lib/api";

interface Props {
  onSelect?: (author: ApiAuthor) => void;
}

export default function SearchBar({ onSelect }: Props) {
  const [query, setQuery]       = useState("");
  const [results, setResults]   = useState<ApiAuthor[]>([]);
  const [allAuthors, setAllAuthors] = useState<ApiAuthor[]>([]);
  const [open, setOpen]         = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  // 初始加载全部作家（用于本地模糊匹配）
  useEffect(() => {
    fetchAuthors().then(setAllAuthors).catch(() => {});
  }, []);

  // 关闭下拉
  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  // 本地过滤
  useEffect(() => {
    const q = query.trim().toLowerCase();
    if (!q) {
      setResults([]);
      setOpen(false);
      return;
    }
    const matched = allAuthors.filter(
      a =>
        a.name_zh.toLowerCase().includes(q) ||
        a.name.toLowerCase().includes(q) ||
        a.nationality.toLowerCase().includes(q) ||
        a.tags.some(t => t.toLowerCase().includes(q))
    );
    setResults(matched.slice(0, 8));
    setOpen(matched.length > 0);
  }, [query, allAuthors]);

  return (
    <div ref={ref} className="relative w-full max-w-sm">
      <div className="relative">
        <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 text-sm">⌕</span>
        <input
          type="text"
          placeholder="搜索作家…"
          value={query}
          onChange={e => setQuery(e.target.value)}
          onFocus={() => results.length > 0 && setOpen(true)}
          className="w-full bg-gray-800 border border-gray-700 rounded-lg pl-8 pr-3 py-1.5 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-gray-500"
        />
        {query && (
          <button
            onClick={() => { setQuery(""); setOpen(false); }}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300 text-xs"
          >✕</button>
        )}
      </div>

      {open && (
        <ul className="absolute top-full mt-1 w-full bg-gray-900 border border-gray-700 rounded-lg shadow-xl z-50 overflow-hidden">
          {results.map(a => (
            <li key={a.id}>
              <button
                className="w-full text-left px-4 py-2 hover:bg-gray-800 transition-colors flex items-center gap-3"
                onClick={() => {
                  setQuery(a.name_zh);
                  setOpen(false);
                  onSelect?.(a);
                }}
              >
                <span className="w-7 h-7 rounded-full bg-blue-700 flex items-center justify-center text-white text-xs font-bold shrink-0">
                  {a.name_zh[0]}
                </span>
                <span className="flex flex-col min-w-0">
                  <span className="text-sm text-gray-100 truncate">{a.name_zh}</span>
                  <span className="text-xs text-gray-500 truncate">
                    {a.nationality} · {a.birth}–{a.death ?? "今"}
                  </span>
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
