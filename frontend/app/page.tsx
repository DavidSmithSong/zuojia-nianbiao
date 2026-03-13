"use client";

import Timeline from "@/components/Timeline";
import SearchBar from "@/components/SearchBar";
import { type ApiAuthor } from "@/lib/api";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-950 text-gray-100">
      <header className="px-8 py-6 border-b border-gray-800 flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold tracking-wide">作家年表</h1>
          <p className="text-gray-400 text-sm mt-1">将世界文学史变成一张可以探索的地图</p>
        </div>
        <SearchBar
          onSelect={(author: ApiAuthor) => {
            // 在控制台输出，后续可跳转到作家详情页
            console.info("selected author:", author);
          }}
        />
      </header>
      <Timeline />
    </main>
  );
}
