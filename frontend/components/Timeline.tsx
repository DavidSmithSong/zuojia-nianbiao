"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import * as d3 from "d3";
import EventPanel from "./EventPanel";
import { fetchTimeline, type ApiTimelineEvent } from "../lib/api";

// ── 静态兜底数据（后端不可用时展示）────────────────────────────────────────

const FALLBACK_EVENTS: ApiTimelineEvent[] = [
  { year: 1821, type: "birth",  label: "陀思妥耶夫斯基 出生", author_id: 4,  author_name_zh: "陀思妥耶夫斯基" },
  { year: 1881, type: "death",  label: "陀思妥耶夫斯基 逝世", author_id: 4,  author_name_zh: "陀思妥耶夫斯基" },
  { year: 1881, type: "birth",  label: "鲁迅 出生",           author_id: 1,  author_name_zh: "鲁迅" },
  { year: 1882, type: "birth",  label: "伍尔夫 出生",         author_id: 7,  author_name_zh: "伍尔夫" },
  { year: 1883, type: "birth",  label: "卡夫卡 出生",         author_id: 11, author_name_zh: "卡夫卡" },
  { year: 1899, type: "birth",  label: "博尔赫斯 出生",       author_id: 12, author_name_zh: "博尔赫斯" },
  { year: 1899, type: "birth",  label: "老舍 出生",           author_id: 6,  author_name_zh: "老舍" },
  { year: 1913, type: "birth",  label: "加缪 出生",           author_id: 13, author_name_zh: "加缪" },
  { year: 1918, type: "work",   label: "《狂人日记》出版",    author_id: 1,  author_name_zh: "鲁迅" },
  { year: 1924, type: "death",  label: "卡夫卡 逝世",         author_id: 11, author_name_zh: "卡夫卡" },
  { year: 1925, type: "work",   label: "《达洛维夫人》出版",  author_id: 7,  author_name_zh: "伍尔夫" },
  { year: 1927, type: "birth",  label: "加西亚·马尔克斯 出生", author_id: 18, author_name_zh: "加西亚·马尔克斯" },
  { year: 1929, type: "work",   label: "《喧哗与骚动》出版",  author_id: 15, author_name_zh: "福克纳" },
  { year: 1934, type: "work",   label: "《边城》出版",        author_id: 3,  author_name_zh: "沈从文" },
  { year: 1936, type: "death",  label: "鲁迅 逝世",           author_id: 1,  author_name_zh: "鲁迅" },
  { year: 1941, type: "death",  label: "伍尔夫 逝世",         author_id: 7,  author_name_zh: "伍尔夫" },
  { year: 1942, type: "work",   label: "《局外人》出版",      author_id: 13, author_name_zh: "加缪" },
  { year: 1944, type: "work",   label: "《虚构集》出版",      author_id: 12, author_name_zh: "博尔赫斯" },
  { year: 1960, type: "death",  label: "加缪 逝世",           author_id: 13, author_name_zh: "加缪" },
  { year: 1967, type: "work",   label: "《百年孤独》出版",    author_id: 18, author_name_zh: "加西亚·马尔克斯" },
  { year: 1972, type: "work",   label: "《看不见的城市》出版", author_id: 19, author_name_zh: "卡尔维诺" },
  { year: 1986, type: "death",  label: "博尔赫斯 逝世",       author_id: 12, author_name_zh: "博尔赫斯" },
  { year: 1992, type: "work",   label: "《活着》出版",        author_id: 4,  author_name_zh: "余华" },
  { year: 1914, type: "world",  label: "第一次世界大战爆发",   event_id: 1,  category: "war" },
  { year: 1917, type: "world",  label: "俄国十月革命",         event_id: 2,  category: "politics" },
  { year: 1919, type: "world",  label: "五四运动",             event_id: 4,  category: "politics" },
  { year: 1929, type: "world",  label: "全球经济大萧条",       event_id: 5,  category: "economy" },
  { year: 1937, type: "world",  label: "中国全面抗战爆发",     event_id: 7,  category: "war" },
  { year: 1939, type: "world",  label: "第二次世界大战爆发",   event_id: 8,  category: "war" },
  { year: 1945, type: "world",  label: "二战结束·联合国成立",  event_id: 9,  category: "war" },
  { year: 1949, type: "world",  label: "中华人民共和国成立",   event_id: 10, category: "politics" },
  { year: 1966, type: "world",  label: "文化大革命开始",       event_id: 14, category: "politics" },
  { year: 1969, type: "world",  label: "人类首次登月",         event_id: 15, category: "science" },
  { year: 1989, type: "world",  label: "柏林墙倒塌",           event_id: 17, category: "politics" },
  { year: 1991, type: "world",  label: "苏联解体",             event_id: 18, category: "politics" },
];

// ── 颜色映射 ──────────────────────────────────────────────────────────────────

const COLOR: Record<string, string> = {
  birth: "#60a5fa",
  death: "#94a3b8",
  work:  "#34d399",
  life:  "#a78bfa",
  world: "#f87171",
};

const WORLD_CAT_COLOR: Record<string, string> = {
  war:      "#ef4444",
  politics: "#f97316",
  economy:  "#eab308",
  science:  "#22d3ee",
  culture:  "#a78bfa",
  disaster: "#f43f5e",
  general:  "#f87171",
};

// ── 主组件 ────────────────────────────────────────────────────────────────────

export default function Timeline() {
  const svgRef = useRef<SVGSVGElement>(null);

  const [events, setEvents]     = useState<ApiTimelineEvent[]>(FALLBACK_EVENTS);
  const [loading, setLoading]   = useState(false);
  const [apiError, setApiError] = useState(false);
  const [selected, setSelected] = useState<ApiTimelineEvent | null>(null);
  const [fromYear, setFromYear] = useState(1880);
  const [toYear,   setToYear]   = useState(2000);

  // 从后端拉取时间线数据
  const loadTimeline = useCallback(async (from: number, to: number) => {
    setLoading(true);
    try {
      const data = await fetchTimeline(from, to);
      setEvents(data.events);
      setApiError(false);
    } catch {
      setApiError(true);
      // 维持兜底数据不变
    } finally {
      setLoading(false);
    }
  }, []);

  // 防抖加载：年份变化 300ms 后触发
  useEffect(() => {
    const timer = setTimeout(() => loadTimeline(fromYear, toYear), 300);
    return () => clearTimeout(timer);
  }, [fromYear, toYear, loadTimeline]);

  // D3 绘制（events 或年份变化时重绘）
  useEffect(() => {
    if (!svgRef.current) return;

    const svg    = d3.select(svgRef.current);
    const width  = svgRef.current.clientWidth || 800;
    const height = 420;
    const margin = { top: 40, right: 30, bottom: 50, left: 30 };

    svg.selectAll("*").remove();
    svg.attr("height", height);

    const x = d3.scaleLinear()
      .domain([fromYear, toYear])
      .range([margin.left, width - margin.right]);

    const TRACKS = [
      { label: "生平",     y: height * 0.22, types: new Set(["birth", "death", "life"]) },
      { label: "作品",     y: height * 0.50, types: new Set(["work"]) },
      { label: "世界大事", y: height * 0.78, types: new Set(["world"]) },
    ];

    // 背景条纹
    TRACKS.forEach(t => {
      svg.append("rect")
        .attr("x", margin.left)
        .attr("y", t.y - 28)
        .attr("width", width - margin.left - margin.right)
        .attr("height", 56)
        .attr("fill", "#1e293b")
        .attr("rx", 6);

      svg.append("text")
        .attr("x", margin.left + 8)
        .attr("y", t.y + 5)
        .attr("fill", "#64748b")
        .attr("font-size", 11)
        .text(t.label);
    });

    // 时间轴
    const xAxis = d3.axisBottom(x)
      .ticks(Math.min(Math.round((toYear - fromYear) / 10), 20))
      .tickFormat(d => `${d}`);

    svg.append("g")
      .attr("transform", `translate(0, ${height - margin.bottom})`)
      .call(xAxis)
      .call(g => g.select(".domain").attr("stroke", "#475569"))
      .call(g => g.selectAll("text").attr("fill", "#94a3b8").attr("font-size", 11))
      .call(g => g.selectAll("line").attr("stroke", "#475569"));

    const visible = events.filter(e => e.year >= fromYear && e.year <= toYear);

    // Tooltip
    const container = svgRef.current.parentElement!;
    let tooltip = d3.select(container).select<HTMLDivElement>(".tl-tooltip");
    if (tooltip.empty()) {
      tooltip = d3.select(container)
        .append("div")
        .attr("class", "tl-tooltip")
        .style("position",       "absolute")
        .style("background",     "#1e293b")
        .style("color",          "#f1f5f9")
        .style("padding",        "4px 10px")
        .style("border-radius",  "6px")
        .style("font-size",      "12px")
        .style("pointer-events", "none")
        .style("opacity",        "0")
        .style("white-space",    "nowrap");
    }

    // 绘制节点
    TRACKS.forEach(track => {
      const trackEvents = visible.filter(e => track.types.has(e.type));

      svg.selectAll(`.dot-${track.label}`)
        .data(trackEvents)
        .enter()
        .append("circle")
        .attr("cx",   d => x(d.year))
        .attr("cy",   track.y)
        .attr("r",    6)
        .attr("fill", d => d.type === "world"
          ? (WORLD_CAT_COLOR[d.category ?? ""] ?? COLOR.world)
          : COLOR[d.type] ?? "#fff")
        .attr("stroke",       "#0f172a")
        .attr("stroke-width", 1.5)
        .attr("cursor",       "pointer")
        .on("mouseover", function(ev, d) {
          d3.select(this).attr("r", 9);
          tooltip
            .style("opacity", 1)
            .html(d.label)
            .style("left", `${(ev as MouseEvent).offsetX + 12}px`)
            .style("top",  `${(ev as MouseEvent).offsetY - 8}px`);
        })
        .on("mouseout", function() {
          d3.select(this).attr("r", 6);
          tooltip.style("opacity", 0);
        })
        .on("click", (_, d) => setSelected(d));
    });
  }, [events, fromYear, toYear]);

  return (
    <div className="relative px-4 py-6">
      {/* 年份范围 + 状态指示 */}
      <div className="flex items-center gap-4 mb-4 text-sm text-gray-400 flex-wrap">
        <label>
          起始年：
          <input
            type="number" value={fromYear} step={10}
            onChange={e => setFromYear(Number(e.target.value))}
            className="ml-2 w-20 bg-gray-800 border border-gray-700 rounded px-2 py-0.5 text-gray-100"
          />
        </label>
        <label>
          结束年：
          <input
            type="number" value={toYear} step={10}
            onChange={e => setToYear(Number(e.target.value))}
            className="ml-2 w-20 bg-gray-800 border border-gray-700 rounded px-2 py-0.5 text-gray-100"
          />
        </label>
        <span className="text-gray-600">共 {toYear - fromYear} 年</span>
        {loading && <span className="text-blue-400 text-xs animate-pulse">加载中…</span>}
        {apiError && !loading && (
          <span className="text-yellow-500 text-xs">· 离线数据</span>
        )}
      </div>

      {/* 时间线 SVG */}
      <div className="relative w-full">
        <svg ref={svgRef} className="w-full" />
      </div>

      {/* 图例 */}
      <div className="flex gap-4 mt-3 text-xs text-gray-500 flex-wrap">
        {Object.entries(COLOR).map(([k, c]) => (
          <span key={k} className="flex items-center gap-1">
            <span style={{ background: c }} className="inline-block w-2.5 h-2.5 rounded-full" />
            {{ birth:"出生", death:"逝世", work:"作品", life:"生平", world:"世界大事" }[k]}
          </span>
        ))}
      </div>

      {/* 详情面板 */}
      {selected && (
        <EventPanel event={selected} onClose={() => setSelected(null)} />
      )}
    </div>
  );
}
