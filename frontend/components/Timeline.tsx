"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import * as d3 from "d3";
import { useRouter } from "next/navigation";
import EventPanel from "./EventPanel";
import { PORTRAITS } from "./portraits";
import { fetchTimeline, fetchAuthors, type ApiTimelineEvent, type ApiAuthor } from "../lib/api";

// ── 兜底数据 ──────────────────────────────────────────────────────────────────

const FALLBACK_EVENTS: ApiTimelineEvent[] = [
  { year: 1821, type: "birth",  label: "陀思妥耶夫斯基 出生", author_id: 4,  author_name_zh: "陀思妥耶夫斯基" },
  { year: 1881, type: "death",  label: "陀思妥耶夫斯基 逝世", author_id: 4,  author_name_zh: "陀思妥耶夫斯基" },
  { year: 1881, type: "birth",  label: "鲁迅 出生",           author_id: 1,  author_name_zh: "鲁迅" },
  { year: 1882, type: "birth",  label: "伍尔夫 出生",         author_id: 7,  author_name_zh: "伍尔夫" },
  { year: 1883, type: "birth",  label: "卡夫卡 出生",         author_id: 11, author_name_zh: "卡夫卡" },
  { year: 1899, type: "birth",  label: "博尔赫斯 出生",       author_id: 12, author_name_zh: "博尔赫斯" },
  { year: 1899, type: "birth",  label: "老舍 出生",           author_id: 6,  author_name_zh: "老舍" },
  { year: 1890, type: "birth",  label: "海明威 出生",         author_id: 20, author_name_zh: "海明威" },
  { year: 1897, type: "birth",  label: "福克纳 出生",         author_id: 15, author_name_zh: "福克纳" },
  { year: 1913, type: "birth",  label: "加缪 出生",           author_id: 13, author_name_zh: "加缪" },
  { year: 1918, type: "work",   label: "《狂人日记》出版",    author_id: 1,  author_name_zh: "鲁迅" },
  { year: 1924, type: "death",  label: "卡夫卡 逝世",         author_id: 11, author_name_zh: "卡夫卡" },
  { year: 1925, type: "work",   label: "《达洛维夫人》出版",  author_id: 7,  author_name_zh: "伍尔夫" },
  { year: 1926, type: "work",   label: "《太阳照常升起》出版", author_id: 20, author_name_zh: "海明威" },
  { year: 1927, type: "birth",  label: "加西亚·马尔克斯 出生", author_id: 18, author_name_zh: "加西亚·马尔克斯" },
  { year: 1929, type: "work",   label: "《喧哗与骚动》出版",  author_id: 15, author_name_zh: "福克纳" },
  { year: 1934, type: "work",   label: "《边城》出版",        author_id: 3,  author_name_zh: "沈从文" },
  { year: 1902, type: "birth",  label: "沈从文 出生",         author_id: 3,  author_name_zh: "沈从文" },
  { year: 1936, type: "death",  label: "鲁迅 逝世",           author_id: 1,  author_name_zh: "鲁迅" },
  { year: 1941, type: "death",  label: "伍尔夫 逝世",         author_id: 7,  author_name_zh: "伍尔夫" },
  { year: 1942, type: "work",   label: "《局外人》出版",      author_id: 13, author_name_zh: "加缪" },
  { year: 1944, type: "work",   label: "《虚构集》出版",      author_id: 12, author_name_zh: "博尔赫斯" },
  { year: 1952, type: "work",   label: "《老人与海》出版",    author_id: 20, author_name_zh: "海明威" },
  { year: 1960, type: "death",  label: "加缪 逝世",           author_id: 13, author_name_zh: "加缪" },
  { year: 1961, type: "death",  label: "海明威 逝世",         author_id: 20, author_name_zh: "海明威" },
  { year: 1962, type: "death",  label: "福克纳 逝世",         author_id: 15, author_name_zh: "福克纳" },
  { year: 1967, type: "work",   label: "《百年孤独》出版",    author_id: 18, author_name_zh: "加西亚·马尔克斯" },
  { year: 1972, type: "work",   label: "《看不见的城市》出版", author_id: 19, author_name_zh: "卡尔维诺" },
  { year: 1923, type: "birth",  label: "卡尔维诺 出生",       author_id: 19, author_name_zh: "卡尔维诺" },
  { year: 1985, type: "death",  label: "卡尔维诺 逝世",       author_id: 19, author_name_zh: "卡尔维诺" },
  { year: 1986, type: "death",  label: "博尔赫斯 逝世",       author_id: 12, author_name_zh: "博尔赫斯" },
  { year: 1988, type: "death",  label: "沈从文 逝世",         author_id: 3,  author_name_zh: "沈从文" },
  { year: 1992, type: "work",   label: "《活着》出版",        author_id: 40, author_name_zh: "余华" },
  { year: 1960, type: "birth",  label: "余华 出生",           author_id: 40, author_name_zh: "余华" },
  { year: 2014, type: "death",  label: "加西亚·马尔克斯 逝世", author_id: 18, author_name_zh: "加西亚·马尔克斯" },
  { year: 1914, type: "world",  label: "第一次世界大战爆发",  event_id: 1,  category: "war" },
  { year: 1917, type: "world",  label: "俄国十月革命",        event_id: 2,  category: "politics" },
  { year: 1919, type: "world",  label: "五四运动",            event_id: 4,  category: "politics" },
  { year: 1929, type: "world",  label: "全球经济大萧条",      event_id: 5,  category: "economy" },
  { year: 1937, type: "world",  label: "中国全面抗战爆发",    event_id: 7,  category: "war" },
  { year: 1939, type: "world",  label: "第二次世界大战爆发",  event_id: 8,  category: "war" },
  { year: 1945, type: "world",  label: "二战结束·联合国成立", event_id: 9,  category: "war" },
  { year: 1949, type: "world",  label: "中华人民共和国成立",  event_id: 10, category: "politics" },
  { year: 1966, type: "world",  label: "文化大革命开始",      event_id: 14, category: "politics" },
  { year: 1969, type: "world",  label: "人类首次登月",        event_id: 15, category: "science" },
  { year: 1989, type: "world",  label: "柏林墙倒塌",          event_id: 17, category: "politics" },
  { year: 1991, type: "world",  label: "苏联解体",            event_id: 18, category: "politics" },
];

const WORLD_CAT_COLOR: Record<string, string> = {
  war:      "#ef4444",
  politics: "#f97316",
  economy:  "#eab308",
  science:  "#22d3ee",
  culture:  "#a78bfa",
  disaster: "#f43f5e",
  general:  "#f87171",
};

// 从兜底事件推导作家泳道列表
function deriveFallbackAuthors(): ApiAuthor[] {
  const map = new Map<string, { birth?: number; death?: number; id: number }>();
  FALLBACK_EVENTS.forEach(e => {
    if (!e.author_name_zh || e.type === "world") return;
    if (!map.has(e.author_name_zh)) map.set(e.author_name_zh, { id: e.author_id ?? 0 });
    const a = map.get(e.author_name_zh)!;
    if (e.type === "birth") a.birth = e.year;
    if (e.type === "death") a.death = e.year;
  });
  return Array.from(map.entries())
    .filter(([, a]) => a.birth !== undefined)
    .map(([name, a]) => ({
      id: a.id,
      name: name,
      name_zh: name,
      birth: a.birth!,
      death: a.death,
      nationality: "",
      bio_zh: "",
      tags: [],
    }))
    .sort((a, b) => a.birth - b.birth);
}

// 作家颜色（固定调色板，保证每次渲染颜色稳定）
const PALETTE = [
  "#3b82f6","#8b5cf6","#06b6d4","#10b981","#f59e0b",
  "#ef4444","#ec4899","#6366f1","#14b8a6","#f97316",
  "#84cc16","#a78bfa","#fb7185","#34d399","#fbbf24",
];
const authorColor = (name: string, idx: number) => PALETTE[idx % PALETTE.length];

// ── 主组件 ────────────────────────────────────────────────────────────────────

export default function Timeline() {
  const svgRef    = useRef<SVGSVGElement>(null);
  const router    = useRouter();
  const routerRef = useRef(router);
  useEffect(() => { routerRef.current = router; });

  const [events,    setEvents]   = useState<ApiTimelineEvent[]>(FALLBACK_EVENTS);
  const [authors,   setAuthors]  = useState<ApiAuthor[]>([]);
  const [loading,   setLoading]  = useState(false);
  const [apiError,  setApiError] = useState(false);
  const [selected,  setSelected] = useState<ApiTimelineEvent | null>(null);
  const [fromYear,  setFromYear] = useState(1850);
  const [toYear,    setToYear]   = useState(1950);
  const [theme,     setTheme]    = useState<"dark" | "light">("dark");
  const [natFilter,   setNatFilter]   = useState<string>("全部");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [hoverCard,   setHoverCard]   = useState<{ author: ApiAuthor; x: number; y: number } | null>(null);

  const setHoverRef = useRef(setHoverCard);
  useEffect(() => { setHoverRef.current = setHoverCard; });

  // 同步主题
  useEffect(() => {
    const html = document.documentElement;
    const sync = () => setTheme(html.classList.contains("dark") ? "dark" : "light");
    sync();
    const obs = new MutationObserver(sync);
    obs.observe(html, { attributes: true, attributeFilter: ["class"] });
    return () => obs.disconnect();
  }, []);

  // 拉取数据
  const loadData = useCallback(async (from: number, to: number) => {
    setLoading(true);
    try {
      const [tl, au] = await Promise.all([fetchTimeline(from, to), fetchAuthors()]);
      setEvents(tl.events);
      setAuthors(au.slice().sort((a, b) => a.birth - b.birth));
      setApiError(false);
    } catch {
      setApiError(true);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const t = setTimeout(() => loadData(fromYear, toYear), 300);
    return () => clearTimeout(t);
  }, [fromYear, toYear, loadData]);

  // D3 绘制
  useEffect(() => {
    if (!svgRef.current) return;

    const isDark   = theme === "dark";
    const bgPage   = isDark ? "#0f172a" : "#ffffff";
    const rowOdd   = isDark ? "rgba(255,255,255,0.025)" : "rgba(0,0,0,0.025)";
    const rowHover = isDark ? "#1e3a5f" : "#dbeafe";
    const axisClr  = isDark ? "#334155" : "#cbd5e1";
    const axisText = isDark ? "#64748b" : "#94a3b8";
    const nameClr  = isDark ? "#e2e8f0" : "#1e293b";
    const yearClr  = isDark ? "#475569" : "#94a3b8";
    const sepClr   = isDark ? "#1e293b" : "#f1f5f9";
    const tipBg    = isDark ? "#1e293b" : "#ffffff";
    const tipFg    = isDark ? "#f1f5f9" : "#0f172a";
    const tipBrd   = isDark ? "#334155" : "#e2e8f0";

    // 作家泳道数据：优先 API，降级到兜底推导
    const laneAuthors: ApiAuthor[] = authors.length > 0
      ? authors
      : deriveFallbackAuthors();

    const natMatch = (nat: string) => {
      if (natFilter === "全部") return true;
      if (natFilter === "中国") return nat.includes("中国");
      if (natFilter === "希腊罗马") return nat.includes("古希腊") || nat.includes("古罗马");
      if (natFilter === "俄国") return nat.includes("俄") || nat.includes("苏联");
      if (natFilter === "法国") return nat.includes("法国");
      if (natFilter === "英美") return nat.includes("英国") || nat.includes("美国") || nat.includes("爱尔兰");
      if (natFilter === "其他") return !nat.includes("中国") && !nat.includes("古希腊") && !nat.includes("古罗马") && !nat.includes("俄") && !nat.includes("法国") && !nat.includes("英国") && !nat.includes("美国") && !nat.includes("爱尔兰");
      return true;
    };

    const sq = searchQuery.trim().toLowerCase();
    const visibleAuthors = laneAuthors.filter(a => {
      const end = a.death ?? 2030;
      return a.birth <= toYear && end >= fromYear && natMatch(a.nationality);
    });

    const totalAuthors = visibleAuthors.length;
    const LANE_H  = totalAuthors > 60 ? 32 : totalAuthors > 30 ? 42 : 56;
    const BAR_H   = totalAuthors > 60 ? 12 : totalAuthors > 30 ? 16 : 22;
    const PORT_R  = totalAuthors > 60 ?  9 : totalAuthors > 30 ? 12 : 16;
    const LEFT_W  = 156;
    const BAND_H  = 28;   // 思潮色带高度
    const M       = { top: 44 + BAND_H, right: 24, bottom: 16, left: 0 };
    const WORLD_H = 68;
    const GAP     = 32;

    // ── 文学思潮定义 ──────────────────────────────────────────────────────────
    const WEST_MOVEMENTS = [
      { label: "古希腊", from: -800, to: -100, color: "#0ea5e9" },
      { label: "古罗马", from: -100, to:  400, color: "#f59e0b" },
      { label: "中世纪", from:  400, to: 1400, color: "#8b5cf6" },
      { label: "文艺复兴", from: 1400, to: 1620, color: "#f97316" },
      { label: "古典/启蒙", from: 1620, to: 1800, color: "#06b6d4" },
      { label: "浪漫主义", from: 1780, to: 1870, color: "#ec4899" },
      { label: "现实主义", from: 1830, to: 1920, color: "#22c55e" },
      { label: "现代主义", from: 1890, to: 1960, color: "#6366f1" },
      { label: "后现代",   from: 1960, to: 2030, color: "#94a3b8" },
    ];
    const CN_MOVEMENTS = [
      { label: "先秦",   from: -800, to: -200, color: "#ef4444" },
      { label: "汉魏六朝", from: -200, to:  600, color: "#f97316" },
      { label: "隋唐",   from:  600, to:  960, color: "#eab308" },
      { label: "宋元",   from:  960, to: 1368, color: "#84cc16" },
      { label: "明清",   from: 1368, to: 1912, color: "#14b8a6" },
      { label: "中国现代", from: 1912, to: 1949, color: "#f43f5e" },
      { label: "中国当代", from: 1949, to: 2030, color: "#a855f7" },
    ];

    const svg   = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth || 900;
    const chartW = width - LEFT_W - M.right;

    const zoneH  = visibleAuthors.length * LANE_H;
    const totalH = M.top + zoneH + GAP + WORLD_H + M.bottom;

    svg.selectAll("*").remove();
    svg.attr("height", totalH);

    const defs = svg.append("defs");

    const x = d3.scaleLinear()
      .domain([fromYear, toYear])
      .range([0, chartW]);

    // ── 思潮色带（两行：西方 + 中国） ────────────────────────────────────────
    const drawBands = (movements: typeof WEST_MOVEMENTS, rowY: number, rowH: number) => {
      movements.forEach(mv => {
        const bFrom = Math.max(fromYear, mv.from);
        const bTo   = Math.min(toYear,   mv.to);
        if (bFrom >= bTo) return;
        const bx = LEFT_W + x(bFrom);
        const bw = x(bTo) - x(bFrom);
        svg.append("rect")
          .attr("x", bx).attr("y", rowY)
          .attr("width", bw).attr("height", rowH)
          .attr("fill", mv.color).attr("opacity", 0.18).attr("rx", 2);
        if (bw > 40) {
          svg.append("text")
            .attr("x", bx + bw / 2).attr("y", rowY + rowH / 2 + 4)
            .attr("text-anchor", "middle").attr("font-size", 9)
            .attr("fill", mv.color).attr("opacity", 0.9)
            .attr("pointer-events", "none")
            .text(mv.label);
        }
      });
    };
    const bandRowH = BAND_H / 2;
    drawBands(WEST_MOVEMENTS, 44,              bandRowH);
    drawBands(CN_MOVEMENTS,   44 + bandRowH,   bandRowH);

    // 色带左侧标签
    svg.append("text").attr("x", 2).attr("y", 44 + bandRowH / 2 + 3)
      .attr("font-size", 8).attr("fill", axisText).attr("opacity", 0.7).text("西");
    svg.append("text").attr("x", 2).attr("y", 44 + bandRowH + bandRowH / 2 + 3)
      .attr("font-size", 8).attr("fill", axisText).attr("opacity", 0.7).text("中");

    // ── X 轴（顶部） ──────────────────────────────────────────────────────────
    const tickCount = Math.min(Math.round((toYear - fromYear) / 10), 24);
    svg.append("g")
      .attr("transform", `translate(${LEFT_W}, ${M.top - 6})`)
      .call(
        d3.axisTop(x)
          .ticks(tickCount)
          .tickFormat(d => {
            const y = Number(d);
            if (y < 0) return `前${Math.abs(y)}`;
            return `${y}`;
          })
          .tickSize(5)
      )
      .call(g => g.select(".domain").attr("stroke", axisClr))
      .call(g => g.selectAll("text").attr("fill", axisText).attr("font-size", 11))
      .call(g => g.selectAll("line").attr("stroke", axisClr));

    // ── 竖向网格线（淡） ──────────────────────────────────────────────────────
    x.ticks(tickCount).forEach(tick => {
      svg.append("line")
        .attr("x1", LEFT_W + x(tick)).attr("y1", M.top)
        .attr("x2", LEFT_W + x(tick)).attr("y2", M.top + zoneH)
        .attr("stroke", isDark ? "rgba(255,255,255,0.04)" : "rgba(0,0,0,0.05)")
        .attr("stroke-width", 1);
    });

    // ── Tooltip ───────────────────────────────────────────────────────────────
    const container = svgRef.current.parentElement!;
    let tip = d3.select(container).select<HTMLDivElement>(".tl-tip");
    if (tip.empty()) {
      tip = d3.select(container).append("div").attr("class", "tl-tip")
        .style("position", "absolute").style("padding", "5px 12px")
        .style("border-radius", "8px").style("font-size", "12px")
        .style("pointer-events", "none").style("opacity", "0")
        .style("white-space", "nowrap").style("z-index", "200")
        .style("transition", "opacity 0.1s");
    }
    tip.style("background", tipBg).style("color", tipFg)
       .style("border", `1px solid ${tipBrd}`)
       .style("box-shadow", "0 4px 12px rgba(0,0,0,0.15)");

    const showTip = (ev: MouseEvent, html: string) => {
      const cr = container.getBoundingClientRect();
      tip.style("opacity", "1").html(html)
         .style("left", `${ev.clientX - cr.left + 14}px`)
         .style("top",  `${ev.clientY - cr.top  - 10}px`);
    };
    const hideTip = () => tip.style("opacity", "0");

    // ── 作家泳道 ──────────────────────────────────────────────────────────────
    visibleAuthors.forEach((author, i) => {
      const laneY  = M.top + i * LANE_H;
      const midY   = laneY + LANE_H / 2;
      const barY   = midY - BAR_H / 2;
      const color  = authorColor(author.name_zh, i);

      const barFrom = Math.max(fromYear, author.birth);
      const barTo   = Math.min(toYear,   author.death ?? toYear + 20);
      const bx      = LEFT_W + x(barFrom);
      const bw      = x(barTo) - x(barFrom);

      // 交替行底色
      svg.append("rect")
        .attr("x", 0).attr("y", laneY)
        .attr("width", width).attr("height", LANE_H)
        .attr("fill", i % 2 === 0 ? "transparent" : rowOdd);

      // 搜索 dim：不匹配时整行半透明
      const matched = !sq || author.name_zh.includes(sq) || author.name.toLowerCase().includes(sq);
      if (!matched) {
        svg.append("rect")
          .attr("x", 0).attr("y", laneY)
          .attr("width", width).attr("height", LANE_H)
          .attr("fill", isDark ? "rgba(15,23,42,0.65)" : "rgba(255,255,255,0.65)")
          .attr("pointer-events", "none");
      }

      // 悬停高亮（透明覆盖，监听整行）
      const cr = svgRef.current!.getBoundingClientRect();
      svg.append("rect")
        .attr("x", 0).attr("y", laneY)
        .attr("width", width).attr("height", LANE_H)
        .attr("fill", "transparent")
        .attr("cursor", "pointer")
        .on("mouseover", function(ev: MouseEvent) {
          d3.select(this).attr("fill", rowHover);
          setHoverRef.current({
            author,
            x: ev.clientX - cr.left,
            y: ev.clientY - cr.top,
          });
        })
        .on("mousemove", function(ev: MouseEvent) {
          setHoverRef.current(prev => prev
            ? { ...prev, x: ev.clientX - cr.left, y: ev.clientY - cr.top }
            : null);
        })
        .on("mouseout",  function() {
          d3.select(this).attr("fill", "transparent");
          setHoverRef.current(null);
        })
        .on("click", () => routerRef.current.push(`/authors/${author.id}`));

      // ── 左侧：头像 ────────────────────────────────────────────────────────
      const px = 8 + PORT_R;
      const py = midY;
      const clipId = `clip-a${i}`;
      defs.append("clipPath").attr("id", clipId)
        .append("circle").attr("cx", px).attr("cy", py).attr("r", PORT_R);

      const portraitUrl = PORTRAITS[author.name_zh];
      if (portraitUrl) {
        svg.append("image")
          .attr("href", portraitUrl)
          .attr("x", px - PORT_R).attr("y", py - PORT_R)
          .attr("width", PORT_R * 2).attr("height", PORT_R * 2)
          .attr("clip-path", `url(#${clipId})`);
      } else {
        svg.append("circle")
          .attr("cx", px).attr("cy", py).attr("r", PORT_R)
          .attr("fill", color);
        svg.append("text")
          .attr("x", px).attr("y", py)
          .attr("text-anchor", "middle").attr("dominant-baseline", "central")
          .attr("fill", "#fff").attr("font-size", 13).attr("font-weight", 700)
          .attr("pointer-events", "none")
          .text(author.name_zh[0]);
      }
      // 头像边框环
      svg.append("circle")
        .attr("cx", px).attr("cy", py).attr("r", PORT_R)
        .attr("fill", "none").attr("stroke", color).attr("stroke-width", 2)
        .attr("pointer-events", "none");

      // ── 左侧：姓名 + 年份 ────────────────────────────────────────────────
      const textX    = px + PORT_R + 6;
      const nameFz   = totalAuthors > 60 ? 10 : totalAuthors > 30 ? 11 : 13;
      const yearFz   = totalAuthors > 60 ?  8 : 10;
      const nameOffY = totalAuthors > 60 ?  3 :  5;
      const yearOffY = totalAuthors > 60 ?  3 : 10;
      svg.append("text")
        .attr("x", textX).attr("y", midY - nameOffY)
        .attr("fill", nameClr).attr("font-size", nameFz).attr("font-weight", 600)
        .attr("pointer-events", "none")
        .text(author.name_zh);
      if (totalAuthors <= 60) {
        const bStr = author.birth < 0 ? `前${Math.abs(author.birth)}` : `${author.birth}`;
        const dStr = author.death == null ? "今" : author.death < 0 ? `前${Math.abs(author.death)}` : `${author.death}`;
        svg.append("text")
          .attr("x", textX).attr("y", midY + yearOffY)
          .attr("fill", yearClr).attr("font-size", yearFz)
          .attr("pointer-events", "none")
          .text(`${bStr}–${dStr}`);
      }

      // ── 生命横条 ─────────────────────────────────────────────────────────
      if (bw > 0) {
        // 渐变定义
        const gradId = `grad${i}`;
        const grad = defs.append("linearGradient")
          .attr("id", gradId).attr("x1", "0%").attr("y1", "0%").attr("x2", "100%").attr("y2", "0%");
        grad.append("stop").attr("offset", "0%")
          .attr("stop-color", color).attr("stop-opacity", 0.9);
        grad.append("stop").attr("offset", "100%")
          .attr("stop-color", color).attr("stop-opacity", 0.6);

        // 条阴影
        svg.append("rect")
          .attr("x", bx + 1).attr("y", barY + 2)
          .attr("width", bw).attr("height", BAR_H)
          .attr("fill", "rgba(0,0,0,0.2)").attr("rx", 5)
          .attr("pointer-events", "none");

        // 主条
        svg.append("rect")
          .attr("x", bx).attr("y", barY)
          .attr("width", bw).attr("height", BAR_H)
          .attr("fill", `url(#${gradId})`).attr("rx", 5)
          .attr("pointer-events", "none");

        // 左端箭头（出生在视窗之前）
        if (author.birth < fromYear) {
          svg.append("polygon")
            .attr("points", `${bx},${barY} ${bx - 10},${midY} ${bx},${barY + BAR_H}`)
            .attr("fill", color).attr("opacity", 0.5)
            .attr("pointer-events", "none");
        }
        // 右端箭头（仍在世 / 超出视窗）
        if (!author.death || author.death > toYear) {
          svg.append("polygon")
            .attr("points", `${bx + bw},${barY} ${bx + bw + 10},${midY} ${bx + bw},${barY + BAR_H}`)
            .attr("fill", color).attr("opacity", 0.5)
            .attr("pointer-events", "none");
        }

        // ── 著作竖线 ───────────────────────────────────────────────────────
        const works = events.filter(e =>
          e.author_name_zh === author.name_zh &&
          e.type === "work" &&
          e.year >= fromYear && e.year <= toYear
        );
        works.forEach(w => {
          const wx = LEFT_W + x(w.year);
          // 白色竖线
          svg.append("line")
            .attr("x1", wx).attr("y1", barY + 3)
            .attr("x2", wx).attr("y2", barY + BAR_H - 3)
            .attr("stroke", "rgba(255,255,255,0.85)").attr("stroke-width", 2)
            .attr("pointer-events", "none");
          // 命中区
          svg.append("rect")
            .attr("x", wx - 5).attr("y", barY)
            .attr("width", 10).attr("height", BAR_H)
            .attr("fill", "transparent").attr("cursor", "pointer")
            .on("mouseover", ev => showTip(ev, `📖 ${w.label}`))
            .on("mouseout",  hideTip)
            .on("click",  (ev) => { ev.stopPropagation(); setSelected(w); });
        });
      }
    });

    // ── 分隔线 + "世界大事"标题 ───────────────────────────────────────────────
    const worldTop = M.top + zoneH + GAP;
    svg.append("line")
      .attr("x1", LEFT_W).attr("y1", worldTop - GAP / 2)
      .attr("x2", width - M.right).attr("y2", worldTop - GAP / 2)
      .attr("stroke", axisClr).attr("stroke-dasharray", "4 4");

    // ── 世界大事轨道 ──────────────────────────────────────────────────────────
    const worldMid = worldTop + WORLD_H / 2;
    svg.append("rect")
      .attr("x", LEFT_W).attr("y", worldTop)
      .attr("width", chartW).attr("height", WORLD_H)
      .attr("fill", sepClr).attr("rx", 8);

    svg.append("text")
      .attr("x", LEFT_W + 10).attr("y", worldMid + 4)
      .attr("fill", axisText).attr("font-size", 11).attr("font-weight", 500)
      .text("世界大事");

    const worldEvents = events.filter(e =>
      e.type === "world" && e.year >= fromYear && e.year <= toYear
    );
    worldEvents.forEach(e => {
      const cx = LEFT_W + x(e.year);
      const cy = worldMid;
      const fc = WORLD_CAT_COLOR[e.category ?? ""] ?? "#f87171";
      svg.append("circle")
        .attr("cx", cx).attr("cy", cy).attr("r", 7)
        .attr("fill", fc).attr("stroke", bgPage).attr("stroke-width", 1.5)
        .attr("cursor", "pointer")
        .on("mouseover", ev => { d3.select(ev.currentTarget as Element).attr("r", 10); showTip(ev, e.label); })
        .on("mouseout",  ev => { d3.select(ev.currentTarget as Element).attr("r", 7); hideTip(); })
        .on("click",  () => setSelected(e));
    });

  }, [events, authors, fromYear, toYear, theme, natFilter, searchQuery]);

  const NAT_GROUPS = [
    { label: "全部",   color: "#64748b" },
    { label: "中国",   color: "#ef4444" },
    { label: "希腊罗马", color: "#f59e0b" },
    { label: "俄国",   color: "#f97316" },
    { label: "法国",   color: "#3b82f6" },
    { label: "英美",   color: "#8b5cf6" },
    { label: "其他",   color: "#10b981" },
  ];

  // 各组作家数量统计
  const allLaneAuthors = authors.length > 0 ? authors : deriveFallbackAuthors();
  const natCount = (label: string) => {
    if (label === "全部") return allLaneAuthors.length;
    return allLaneAuthors.filter(a => {
      const n = a.nationality;
      if (label === "中国")   return n.includes("中国");
      if (label === "希腊罗马") return n.includes("古希腊") || n.includes("古罗马");
      if (label === "俄国")   return n.includes("俄") || n.includes("苏联");
      if (label === "法国")   return n.includes("法国");
      if (label === "英美")   return n.includes("英国") || n.includes("美国") || n.includes("爱尔兰");
      if (label === "其他")   return !n.includes("中国") && !n.includes("古希腊") && !n.includes("古罗马") && !n.includes("俄") && !n.includes("法国") && !n.includes("英国") && !n.includes("美国") && !n.includes("爱尔兰");
      return false;
    }).length;
  };

  const ERA_PRESETS = [
    { label: "古希腊罗马", from: -800, to:  600 },
    { label: "中古",       from:  600, to: 1600 },
    { label: "近代",       from: 1600, to: 1850 },
    { label: "现代",       from: 1850, to: 1950 },
    { label: "当代",       from: 1950, to: 2030 },
    { label: "全览",       from: -800, to: 2030 },
  ];

  return (
    <div className="px-4 py-6">
      {/* 时代快捷按钮 */}
      <div className="flex items-center gap-2 flex-wrap mb-3">
        <span className="text-xs t-text-m mr-1">时代</span>
        {ERA_PRESETS.map(({ label, from, to }) => {
          const active = fromYear === from && toYear === to;
          return (
            <button
              key={label}
              onClick={() => { setFromYear(from); setToYear(to); }}
              className="text-xs px-3 py-1 rounded-full transition-all"
              style={{
                background: active ? "#1d4ed8" : "var(--surface2)",
                color:      active ? "#fff"    : "var(--text-m)",
                border:     `1px solid ${active ? "#1d4ed8" : "var(--border)"}`,
                fontWeight: active ? 600 : 400,
              }}
            >
              {label}
            </button>
          );
        })}
      </div>

      {/* 控制栏 */}
      <div className="flex flex-wrap items-center gap-x-6 gap-y-3 mb-5">
        {/* 年份范围 */}
        <div className="flex items-center gap-3 text-sm t-text-m">
          <label className="flex items-center gap-2">
            起始年
            <input type="number" value={fromYear} step={10}
              onChange={e => setFromYear(Number(e.target.value))}
              className="w-20 t-input" />
          </label>
          <span>—</span>
          <label className="flex items-center gap-2">
            结束年
            <input type="number" value={toYear} step={10}
              onChange={e => setToYear(Number(e.target.value))}
              className="w-20 t-input" />
          </label>
          <span className="text-xs">共 {toYear - fromYear} 年</span>
          {loading && <span className="text-blue-400 text-xs animate-pulse">· 加载中</span>}
          {apiError && !loading && <span className="text-amber-500 text-xs">· 离线数据</span>}
        </div>

        {/* 搜索框 */}
        <div className="relative">
          <span className="absolute left-2.5 top-1/2 -translate-y-1/2 text-xs" style={{ color: "var(--text-m)" }}>⌕</span>
          <input
            type="text"
            placeholder="搜索作家…"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            className="t-input rounded-lg pl-7 pr-7 py-1.5 text-sm"
            style={{ width: 160 }}
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery("")}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-xs"
              style={{ color: "var(--text-m)" }}
            >✕</button>
          )}
        </div>

        {/* 分隔线 */}
        <div className="h-4 w-px t-border" style={{ borderLeft: "1px solid var(--border)" }} />

        {/* 国籍筛选胶囊 */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs t-text-m mr-1">地区</span>
          {NAT_GROUPS.map(({ label, color }) => {
            const count = natCount(label);
            const active = natFilter === label;
            return (
              <button
                key={label}
                onClick={() => setNatFilter(label)}
                className="flex items-center gap-1.5 text-xs px-3 py-1 rounded-full transition-all"
                style={{
                  background:   active ? color : "var(--surface2)",
                  color:        active ? "#fff" : "var(--text-m)",
                  border:       `1px solid ${active ? color : "var(--border)"}`,
                  fontWeight:   active ? 600 : 400,
                  boxShadow:    active ? `0 0 0 2px ${color}33` : "none",
                }}
              >
                {label !== "全部" && (
                  <span style={{
                    width: 7, height: 7, borderRadius: "50%",
                    background: active ? "rgba(255,255,255,0.7)" : color,
                    display: "inline-block", flexShrink: 0,
                  }} />
                )}
                {label}
                <span style={{
                  fontSize: 10,
                  opacity: 0.75,
                  marginLeft: 1,
                }}>
                  {count}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 时间线 */}
      <div className="relative w-full overflow-x-auto">
        <svg ref={svgRef} className="w-full" style={{ minWidth: 640 }} />

        {/* Hover 卡片 */}
        {hoverCard && (() => {
          const { author, x: hx, y: hy } = hoverCard;
          const portrait = PORTRAITS[author.name_zh];
          const bStr = author.birth < 0 ? `前${Math.abs(author.birth)}` : `${author.birth}`;
          const dStr = author.death == null ? "今" : author.death < 0 ? `前${Math.abs(author.death)}` : `${author.death}`;
          return (
            <div
              style={{
                position: "absolute",
                left: hx + 20,
                top: Math.max(0, hy - 60),
                width: 240,
                background: "var(--surface)",
                border: "1px solid var(--border)",
                borderRadius: 12,
                padding: "12px 14px",
                pointerEvents: "none",
                zIndex: 300,
                boxShadow: "0 8px 24px rgba(0,0,0,0.25)",
              }}
            >
              <div style={{ display: "flex", gap: 10, alignItems: "center", marginBottom: 8 }}>
                {portrait ? (
                  <img src={portrait} alt={author.name_zh}
                    style={{ width: 44, height: 44, borderRadius: "50%", objectFit: "cover", flexShrink: 0, border: "2px solid var(--border)" }} />
                ) : (
                  <div style={{ width: 44, height: 44, borderRadius: "50%", background: "#1d4ed8",
                    display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontSize: 18, fontWeight: 700, flexShrink: 0 }}>
                    {author.name_zh[0]}
                  </div>
                )}
                <div>
                  <div style={{ fontWeight: 700, fontSize: 15, color: "var(--text)" }}>{author.name_zh}</div>
                  <div style={{ fontSize: 11, color: "var(--text-m)", marginTop: 1 }}>{author.nationality} · {bStr}–{dStr}</div>
                </div>
              </div>
              {author.tags.length > 0 && (
                <div style={{ display: "flex", gap: 4, flexWrap: "wrap", marginBottom: 7 }}>
                  {author.tags.slice(0, 3).map(t => (
                    <span key={t} style={{ fontSize: 10, padding: "1px 6px", borderRadius: 99,
                      background: "var(--surface2)", color: "var(--text-m)", border: "1px solid var(--border)" }}>{t}</span>
                  ))}
                </div>
              )}
              {author.bio_zh && (
                <p style={{ fontSize: 11, color: "var(--text-m)", lineHeight: 1.6, margin: 0 }}>
                  {author.bio_zh.slice(0, 80)}…
                </p>
              )}
            </div>
          );
        })()}
      </div>

      {/* 图例 */}
      <div className="flex gap-4 mt-4 text-xs flex-wrap t-text-m">
        <span className="flex items-center gap-1.5">
          <span className="inline-block w-6 h-2 rounded" style={{ background: "rgba(255,255,255,0.6)", border: "1px solid #64748b" }} />
          著作标记
        </span>
        {[
          { c: "#ef4444", l: "战争" }, { c: "#f97316", l: "政治" },
          { c: "#eab308", l: "经济" }, { c: "#22d3ee", l: "科技" },
          { c: "#a78bfa", l: "文化" },
        ].map(({ c, l }) => (
          <span key={l} className="flex items-center gap-1">
            <span style={{ background: c }} className="inline-block w-2.5 h-2.5 rounded-full" />
            {l}
          </span>
        ))}
      </div>

      {selected && <EventPanel event={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
