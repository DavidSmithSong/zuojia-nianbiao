"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import * as d3 from "d3";
import { feature } from "topojson-client";
import ThemeToggle from "@/components/ThemeToggle";
import { PORTRAITS } from "@/components/portraits";
import { fetchAuthors, type ApiAuthor } from "@/lib/api";

// 国籍 → 经纬度（longitude, latitude）
const NAT_COORDS: Record<string, [number, number]> = {
  "古希腊":          [ 22.0,  38.5],
  "古罗马":          [ 12.5,  41.9],
  "意大利":          [ 12.5,  43.0],
  "西班牙":          [ -3.7,  40.4],
  "英国":            [ -1.5,  52.5],
  "法国":            [  2.3,  46.5],
  "德国":            [ 10.5,  51.5],
  "俄国":            [ 37.6,  55.8],
  "苏联":            [ 37.6,  55.8],
  "俄裔美国":        [-87.6,  41.9],
  "挪威":            [ 10.8,  59.9],
  "波兰":            [ 21.0,  52.2],
  "爱尔兰":          [ -8.2,  53.3],
  "美国":            [-98.5,  39.5],
  "美国/英国":       [-87.6,  41.9],
  "阿根廷":          [-64.0, -34.6],
  "哥伦比亚":        [-74.1,   4.7],
  "奥匈帝国（捷克）":[ 14.5,  50.1],
  "中国":            [104.0,  35.0],
  "中国（楚国）":    [112.0,  30.0],
  "中国（西汉）":    [108.5,  34.3],
  "中国（东汉末）":  [113.5,  34.7],
  "中国（三国）":    [113.5,  34.7],
  "中国（东晋）":    [118.8,  32.1],
  "中国（唐朝）":    [108.5,  34.3],
  "中国（南唐）":    [118.8,  32.0],
  "中国（北宋）":    [113.7,  34.8],
  "中国（两宋）":    [120.2,  30.3],
  "中国（南宋）":    [120.2,  30.3],
  "中国（元朝）":    [116.4,  39.9],
  "中国（元末明初）":[116.4,  39.9],
  "中国（明朝）":    [116.4,  39.9],
  "中国（清朝）":    [116.4,  39.9],
  "法国（阿尔及利亚裔）": [2.3, 46.5],
};

function getCoords(nationality: string): [number, number] | null {
  if (NAT_COORDS[nationality]) return NAT_COORDS[nationality];
  for (const key of Object.keys(NAT_COORDS)) {
    if (nationality.includes(key.replace("中国（", "").replace("）", "")) && key !== "中国") continue;
    if (nationality.startsWith(key.split("（")[0]) || nationality === key) return NAT_COORDS[key];
  }
  if (nationality.includes("中国")) return NAT_COORDS["中国"];
  if (nationality.includes("俄") || nationality.includes("苏联")) return NAT_COORDS["俄国"];
  if (nationality.includes("法国")) return NAT_COORDS["法国"];
  if (nationality.includes("英国")) return NAT_COORDS["英国"];
  if (nationality.includes("美国")) return NAT_COORDS["美国"];
  return null;
}

function natColor(nat: string): string {
  if (nat.includes("中国"))   return "#ef4444";
  if (nat.includes("古希腊") || nat.includes("古罗马")) return "#f59e0b";
  if (nat.includes("俄") || nat.includes("苏联"))       return "#f97316";
  if (nat.includes("法国"))   return "#3b82f6";
  if (nat.includes("英国") || nat.includes("美国") || nat.includes("爱尔兰")) return "#8b5cf6";
  return "#10b981";
}

// 区域预设: [经度, 纬度, 缩放倍数]
const REGION_PRESETS: Array<{ label: string; lon: number; lat: number; scale: number }> = [
  { label: "全球",   lon:   10, lat:  20, scale: 1   },
  { label: "中国",   lon:  112, lat:  32, scale: 3.8 },
  { label: "欧洲",   lon:   12, lat:  50, scale: 4.0 },
  { label: "俄国",   lon:   55, lat:  57, scale: 3.0 },
  { label: "美洲",   lon:  -80, lat:  10, scale: 2.2 },
  { label: "希腊",   lon:   23, lat:  39, scale: 7.0 },
];

export default function MapPage() {
  const router    = useRef(useRouter());
  const svgRef    = useRef<SVGSVGElement>(null);
  const zoomRef   = useRef<d3.ZoomBehavior<SVGSVGElement, unknown> | null>(null);
  const projRef   = useRef<d3.GeoProjection | null>(null);
  const sizeRef   = useRef<{ W: number; H: number }>({ W: 900, H: 520 });
  const [authors, setAuthors] = useState<ApiAuthor[]>([]);
  const [hover,   setHover]   = useState<{ author: ApiAuthor; x: number; y: number } | null>(null);
  const [theme,   setTheme]   = useState<"dark"|"light">("dark");

  useEffect(() => {
    fetchAuthors().then(setAuthors).catch(() => {});
    const html = document.documentElement;
    const sync = () => setTheme(html.classList.contains("dark") ? "dark" : "light");
    sync();
    const obs = new MutationObserver(sync);
    obs.observe(html, { attributes: true, attributeFilter: ["class"] });
    return () => obs.disconnect();
  }, []);

  function zoomToRegion(lon: number, lat: number, scale: number) {
    if (!svgRef.current || !zoomRef.current || !projRef.current) return;
    const proj = projRef.current([lon, lat]);
    if (!proj) return;
    const { W, H } = sizeRef.current;
    const [px, py] = proj;
    const t = d3.zoomIdentity.translate(W / 2 - scale * px, H / 2 - scale * py).scale(scale);
    d3.select(svgRef.current).transition().duration(650).call(zoomRef.current.transform, t);
  }

  function resetZoom() {
    zoomToRegion(10, 20, 1);
  }

  useEffect(() => {
    if (!svgRef.current || authors.length === 0) return;

    const isDark   = theme === "dark";
    const landFill = isDark ? "#1e293b" : "#e2e8f0";
    const landStk  = isDark ? "#334155" : "#cbd5e1";
    const waterFg  = isDark ? "#0f172a" : "#dbeafe";

    const el = svgRef.current;
    const W  = el.clientWidth  || 900;
    const H  = el.clientHeight || 520;
    sizeRef.current = { W, H };

    const svg = d3.select(el);
    svg.selectAll("*").remove();

    // 海洋背景（固定，不随zoom移动）
    svg.append("rect").attr("width", W).attr("height", H).attr("fill", waterFg);

    // Zoomable root group
    const root = svg.append("g").attr("class", "map-root");

    // 投影：自然地球
    const projection = d3.geoNaturalEarth1()
      .scale(W / 6.5)
      .translate([W / 2, H / 2]);
    projRef.current = projection;

    const pathGen = d3.geoPath().projection(projection);

    // defs for portrait clipPaths — inside SVG, but clipPaths are in root's coord system
    const defs = svg.append("defs");

    // Zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.5, 12])
      .on("zoom", (event) => {
        root.attr("transform", event.transform);
        setHover(null); // clear hover on pan/zoom
      });

    svg.call(zoom);
    zoomRef.current = zoom;

    // 加载地图
    d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json").then((world: unknown) => {
      const topo = world as { type: string; objects: { countries: unknown; land: unknown } };
      // @ts-ignore
      const land = feature(topo, topo.objects.land);

      root.append("path")
        .datum(land as d3.GeoPermissibleObjects)
        .attr("d", pathGen as unknown as string)
        .attr("fill", landFill)
        .attr("stroke", landStk)
        .attr("stroke-width", 0.5);

      drawAuthors();
    }).catch(() => {
      root.append("path")
        .datum({ type: "Sphere" } as d3.GeoPermissibleObjects)
        .attr("d", pathGen as unknown as string)
        .attr("fill", landFill).attr("stroke", landStk).attr("stroke-width", 0.5);
      drawAuthors();
    });

    function drawAuthors() {
      const placed: Array<{ author: ApiAuthor; px: number; py: number; coords: [number,number] }> = [];
      authors.forEach(a => {
        const coords = getCoords(a.nationality);
        if (!coords) return;
        const proj = projection(coords);
        if (!proj) return;
        const same = placed.filter(p =>
          Math.abs(p.coords[0] - coords[0]) < 0.5 && Math.abs(p.coords[1] - coords[1]) < 0.5);
        const jitter = same.length;
        const cols = 5;
        const dx = (jitter % cols) * 14 - (cols / 2) * 14;
        const dy = Math.floor(jitter / cols) * 14;
        placed.push({ author: a, px: proj[0] + dx, py: proj[1] + dy, coords });
      });

      placed.forEach(({ author, px, py }, i) => {
        const color   = natColor(author.nationality);
        const portrait = PORTRAITS[author.name_zh];
        const R = 10;
        const clipId = `mclip-${i}`;

        // clipPath at local origin — image/circle group will be translated to (px,py)
        defs.append("clipPath").attr("id", clipId)
          .append("circle").attr("cx", 0).attr("cy", 0).attr("r", R);

        const g = root.append("g")
          .attr("transform", `translate(${px},${py})`)
          .attr("cursor", "pointer");

        if (portrait) {
          g.append("image")
            .attr("href", portrait)
            .attr("x", -R).attr("y", -R)
            .attr("width", R * 2).attr("height", R * 2)
            .attr("clip-path", `url(#${clipId})`);
        } else {
          g.append("circle").attr("r", R).attr("fill", color);
          g.append("text")
            .attr("text-anchor", "middle").attr("dominant-baseline", "central")
            .attr("fill", "#fff").attr("font-size", 9).attr("font-weight", 700)
            .attr("pointer-events", "none")
            .text(author.name_zh[0]);
        }

        // 边框 + 交互（透明大圆覆盖，确保hit area）
        g.append("circle")
          .attr("r", R)
          .attr("fill", "transparent")
          .attr("stroke", color).attr("stroke-width", 1.5)
          .on("mouseover", (ev: MouseEvent) => {
            const cr = el.getBoundingClientRect();
            setHover({ author, x: ev.clientX - cr.left, y: ev.clientY - cr.top });
          })
          .on("mousemove", (ev: MouseEvent) => {
            const cr = el.getBoundingClientRect();
            setHover(prev => prev ? { ...prev, x: ev.clientX - cr.left, y: ev.clientY - cr.top } : null);
          })
          .on("mouseout",  () => setHover(null))
          .on("click",     (ev: MouseEvent) => {
            ev.stopPropagation();
            router.current.push(`/authors/${author.id}`);
          });
      });
    }
  }, [authors, theme]);

  return (
    <div className="min-h-screen t-bg t-text flex flex-col">
      <header className="px-8 py-4 flex items-center justify-between shrink-0"
        style={{ borderBottom: "1px solid var(--border)" }}>
        <button onClick={() => router.current.push("/")} className="text-sm t-text-m"
          style={{ display: "flex", alignItems: "center", gap: 4 }}>
          ← 返回年表
        </button>
        <span className="text-sm font-semibold">文学地图</span>
        <ThemeToggle />
      </header>

      {/* 图例 + 操作栏 */}
      <div className="flex gap-4 px-8 py-3 text-xs t-text-m flex-wrap items-center"
        style={{ borderBottom: "1px solid var(--border)" }}>
        {[
          { label: "中国",   color: "#ef4444" },
          { label: "希腊罗马", color: "#f59e0b" },
          { label: "俄国",   color: "#f97316" },
          { label: "法国",   color: "#3b82f6" },
          { label: "英美",   color: "#8b5cf6" },
          { label: "其他",   color: "#10b981" },
        ].map(({ label, color }) => (
          <span key={label} className="flex items-center gap-1.5">
            <span style={{ width: 10, height: 10, borderRadius: "50%", background: color, display: "inline-block" }} />
            {label}
          </span>
        ))}
        <span className="ml-auto flex items-center gap-2 flex-wrap">
          <span className="t-text-m" style={{ fontSize: 11 }}>滚轮缩放 · 拖拽平移</span>
          {REGION_PRESETS.map(r => (
            <button
              key={r.label}
              onClick={() => zoomToRegion(r.lon, r.lat, r.scale)}
              className="text-xs px-2 py-1 rounded"
              style={{ background: "var(--surface2)", border: "1px solid var(--border)", color: "var(--text-m)", cursor: "pointer" }}
            >
              {r.label}
            </button>
          ))}
        </span>
      </div>

      {/* 地图 */}
      <div className="relative flex-1">
        <svg ref={svgRef} style={{ width: "100%", height: "100%", minHeight: 480 }} />

        {hover && (() => {
          const { author, x: hx, y: hy } = hover;
          const portrait = PORTRAITS[author.name_zh];
          const bStr = author.birth < 0 ? `前${Math.abs(author.birth)}` : `${author.birth}`;
          const dStr = author.death == null ? "今" : author.death < 0 ? `前${Math.abs(author.death)}` : `${author.death}`;
          return (
            <div style={{
              position: "absolute", left: hx + 14, top: Math.max(0, hy - 50),
              width: 200, background: "var(--surface)", border: "1px solid var(--border)",
              borderRadius: 10, padding: "10px 12px", pointerEvents: "none", zIndex: 200,
              boxShadow: "0 8px 24px rgba(0,0,0,0.25)",
            }}>
              <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 6 }}>
                {portrait ? (
                  <img src={portrait} alt={author.name_zh} style={{ width: 36, height: 36, borderRadius: "50%", objectFit: "cover", flexShrink: 0 }} />
                ) : (
                  <div style={{ width: 36, height: 36, borderRadius: "50%", background: "#1d4ed8",
                    display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontSize: 14, fontWeight: 700 }}>
                    {author.name_zh[0]}
                  </div>
                )}
                <div>
                  <div style={{ fontWeight: 700, fontSize: 14, color: "var(--text)" }}>{author.name_zh}</div>
                  <div style={{ fontSize: 11, color: "var(--text-m)" }}>{bStr}–{dStr}</div>
                </div>
              </div>
              <div style={{ fontSize: 11, color: "var(--text-m)" }}>{author.nationality}</div>
            </div>
          );
        })()}
      </div>
    </div>
  );
}
