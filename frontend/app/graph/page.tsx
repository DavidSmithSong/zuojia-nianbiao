"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import * as d3 from "d3";
import ThemeToggle from "@/components/ThemeToggle";
import { PORTRAITS } from "@/components/portraits";
import { fetchAuthors, type ApiAuthor } from "@/lib/api";

// ── Relationship data ────────────────────────────────────────────────────────

type RelType = "影响" | "平行" | "师承";

interface Relationship {
  from: string;
  to: string;
  type: RelType;
}

const RELATIONSHIPS: Relationship[] = [
  // ── 古希腊罗马 ──────────────────────────────────────────────
  { from: "荷马",       to: "埃斯库罗斯",     type: "影响" },
  { from: "荷马",       to: "索福克勒斯",     type: "影响" },
  { from: "荷马",       to: "维吉尔",         type: "影响" },
  { from: "荷马",       to: "但丁",           type: "影响" },
  { from: "埃斯库罗斯", to: "索福克勒斯",     type: "影响" },
  { from: "索福克勒斯", to: "欧里庇得斯",     type: "影响" },
  { from: "维吉尔",     to: "奥维德",         type: "平行" },
  { from: "维吉尔",     to: "但丁",           type: "影响" },

  // ── 中世纪→文艺复兴 ─────────────────────────────────────────
  { from: "但丁",       to: "薄伽丘",         type: "影响" },
  { from: "薄伽丘",     to: "拉伯雷",         type: "影响" },
  { from: "拉伯雷",     to: "塞万提斯",       type: "影响" },
  { from: "塞万提斯",   to: "博尔赫斯",       type: "影响" },
  { from: "莎士比亚",   to: "弥尔顿",         type: "影响" },
  { from: "莎士比亚",   to: "歌德",           type: "影响" },
  { from: "莎士比亚",   to: "曹禺",           type: "影响" },
  { from: "弥尔顿",     to: "拜伦",           type: "影响" },
  { from: "笛福",       to: "奥斯丁",         type: "影响" },
  { from: "莫里哀",     to: "席勒",           type: "影响" },

  // ── 浪漫→现实→自然主义 ──────────────────────────────────────
  { from: "席勒",       to: "歌德",           type: "平行" },
  { from: "席勒",       to: "郭沫若",         type: "影响" },
  { from: "歌德",       to: "托尔斯泰",       type: "影响" },
  { from: "拜伦",       to: "普希金",         type: "影响" },
  { from: "拜伦",       to: "徐志摩",         type: "影响" },
  { from: "普希金",     to: "屠格涅夫",       type: "师承" },
  { from: "普希金",     to: "托尔斯泰",       type: "影响" },
  { from: "奥斯丁",     to: "哈代",           type: "影响" },
  { from: "奥斯丁",     to: "伍尔夫",         type: "影响" },
  { from: "惠特曼",     to: "郭沫若",         type: "影响" },
  { from: "惠特曼",     to: "劳伦斯",         type: "影响" },
  { from: "司汤达",     to: "巴尔扎克",       type: "平行" },
  { from: "巴尔扎克",   to: "福楼拜",         type: "影响" },
  { from: "巴尔扎克",   to: "左拉",           type: "影响" },
  { from: "巴尔扎克",   to: "茅盾",           type: "影响" },
  { from: "福楼拜",     to: "莫泊桑",         type: "师承" },
  { from: "福楼拜",     to: "乔伊斯",         type: "影响" },
  { from: "左拉",       to: "莫泊桑",         type: "影响" },
  { from: "波德莱尔",   to: "戴望舒",         type: "影响" },
  { from: "哈代",       to: "劳伦斯",         type: "影响" },
  { from: "哈代",       to: "乔伊斯",         type: "影响" },

  // ── 俄国文学 ───────────────────────────────────────────────
  { from: "果戈里",     to: "陀思妥耶夫斯基", type: "影响" },
  { from: "果戈里",     to: "契诃夫",         type: "影响" },
  { from: "屠格涅夫",   to: "托尔斯泰",       type: "平行" },
  { from: "屠格涅夫",   to: "契诃夫",         type: "影响" },
  { from: "托尔斯泰",   to: "契诃夫",         type: "影响" },
  { from: "陀思妥耶夫斯基", to: "卡夫卡",    type: "影响" },
  { from: "陀思妥耶夫斯基", to: "加缪",      type: "影响" },

  // ── 现代主义 ───────────────────────────────────────────────
  { from: "易卜生",     to: "萨特",           type: "影响" },
  { from: "易卜生",     to: "曹禺",           type: "影响" },
  { from: "普鲁斯特",   to: "伍尔夫",         type: "平行" },
  { from: "普鲁斯特",   to: "纳博科夫",       type: "影响" },
  { from: "乔伊斯",     to: "博尔赫斯",       type: "影响" },
  { from: "乔伊斯",     to: "纳博科夫",       type: "影响" },
  { from: "卡夫卡",     to: "加缪",           type: "影响" },
  { from: "卡夫卡",     to: "余华",           type: "影响" },
  { from: "卡夫卡",     to: "格非",           type: "影响" },
  { from: "萨特",       to: "加缪",           type: "平行" },
  { from: "博尔赫斯",   to: "加西亚·马尔克斯", type: "影响" },
  { from: "加西亚·马尔克斯", to: "莫言",     type: "影响" },
  { from: "加西亚·马尔克斯", to: "余华",     type: "影响" },
  { from: "福克纳",     to: "莫言",           type: "影响" },
  { from: "福克纳",     to: "余华",           type: "影响" },

  // ── 中国现代 ───────────────────────────────────────────────
  { from: "狄更斯",     to: "老舍",           type: "影响" },
  { from: "契诃夫",     to: "老舍",           type: "影响" },
  { from: "鲁迅",       to: "巴金",           type: "影响" },
  { from: "鲁迅",       to: "老舍",           type: "影响" },
  { from: "鲁迅",       to: "茅盾",           type: "影响" },
  { from: "鲁迅",       to: "余华",           type: "影响" },
  { from: "鲁迅",       to: "莫言",           type: "影响" },
  { from: "郭沫若",     to: "巴金",           type: "影响" },
  { from: "巴金",       to: "曹禺",           type: "平行" },
  { from: "沈从文",     to: "汪曾祺",         type: "师承" },
  { from: "沈从文",     to: "苏童",           type: "影响" },
  { from: "沈从文",     to: "张爱玲",         type: "平行" },
  { from: "汪曾祺",     to: "苏童",           type: "影响" },
  { from: "张爱玲",     to: "王安忆",         type: "影响" },
  { from: "曹雪芹",     to: "张爱玲",         type: "影响" },
  { from: "曹雪芹",     to: "鲁迅",           type: "影响" },
  { from: "吴敬梓",     to: "鲁迅",           type: "影响" },

  // ── 中国古典 ───────────────────────────────────────────────
  { from: "屈原",       to: "司马迁",         type: "影响" },
  { from: "屈原",       to: "曹植",           type: "影响" },
  { from: "屈原",       to: "陶渊明",         type: "影响" },
  { from: "屈原",       to: "李白",           type: "影响" },
  { from: "曹操",       to: "曹植",           type: "师承" },
  { from: "陶渊明",     to: "李白",           type: "影响" },
  { from: "李白",       to: "杜甫",           type: "平行" },
  { from: "李白",       to: "白居易",         type: "影响" },
  { from: "李白",       to: "苏轼",           type: "影响" },
  { from: "杜甫",       to: "白居易",         type: "影响" },
  { from: "杜甫",       to: "韩愈",           type: "影响" },
  { from: "韩愈",       to: "苏轼",           type: "影响" },
  { from: "柳永",       to: "李清照",         type: "影响" },
  { from: "苏轼",       to: "李清照",         type: "影响" },
  { from: "苏轼",       to: "辛弃疾",         type: "影响" },
  { from: "辛弃疾",     to: "李清照",         type: "平行" },
  { from: "关汉卿",     to: "汤显祖",         type: "影响" },
  { from: "施耐庵",     to: "罗贯中",         type: "师承" },
  { from: "罗贯中",     to: "吴承恩",         type: "影响" },
  { from: "吴承恩",     to: "蒲松龄",         type: "影响" },
  { from: "蒲松龄",     to: "吴敬梓",         type: "平行" },
  { from: "汤显祖",     to: "曹雪芹",         type: "影响" },
  { from: "司马迁",     to: "曹雪芹",         type: "影响" },
];

// ── Nationality color ────────────────────────────────────────────────────────

function natColor(nat: string): string {
  if (nat.includes("中国")) return "#ef4444";
  if (nat.includes("古希腊") || nat.includes("古罗马")) return "#f59e0b";
  if (nat.includes("俄") || nat.includes("苏联")) return "#f97316";
  if (nat.includes("法国")) return "#3b82f6";
  if (nat.includes("英国") || nat.includes("美国") || nat.includes("爱尔兰")) return "#8b5cf6";
  return "#10b981";
}

// ── Edge style helpers ───────────────────────────────────────────────────────

function edgeColor(type: RelType): string {
  if (type === "影响") return "#60a5fa";
  if (type === "师承") return "#34d399";
  return "#a78bfa";
}

function edgeOpacity(type: RelType): number {
  if (type === "影响") return 0.6;
  if (type === "师承") return 0.8;
  return 0.4;
}

function edgeWidth(type: RelType): number {
  if (type === "师承") return 2.5;
  if (type === "影响") return 1.5;
  return 1;
}

// ── D3 node/link types ───────────────────────────────────────────────────────

interface GraphNode extends d3.SimulationNodeDatum {
  id: number;
  name_zh: string;
  nationality: string;
  hasPortrait: boolean;
  degree: number;
}

function nodeRadius(d: GraphNode): number {
  return Math.min(30, 13 + d.degree * 1.8);
}

interface GraphLink extends d3.SimulationLinkDatum<GraphNode> {
  type: RelType;
  sourceId: number;
  targetId: number;
}

// ── Component ────────────────────────────────────────────────────────────────

export default function GraphPage() {
  const router = useRouter();
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [authors, setAuthors] = useState<ApiAuthor[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const selectedIdRef = useRef<number | null>(null);

  // Fetch authors on mount
  useEffect(() => {
    fetchAuthors()
      .then(setAuthors)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  // Build and render D3 graph whenever authors change
  useEffect(() => {
    if (loading || !svgRef.current || !containerRef.current) return;

    const svgEl = svgRef.current;
    const container = containerRef.current;

    // Clear previous render
    d3.select(svgEl).selectAll("*").remove();

    const width = container.clientWidth;
    const height = container.clientHeight;

    // Build name_zh → author map
    const authorByName = new Map<string, ApiAuthor>();
    for (const a of authors) {
      authorByName.set(a.name_zh, a);
    }

    // Filter relationships to those where both endpoints are present
    const validRels = RELATIONSHIPS.filter(
      r => authorByName.has(r.from) && authorByName.has(r.to)
    );

    // Collect node IDs involved in relationships
    const nodeIds = new Set<number>();
    for (const a of authors) {
      nodeIds.add(a.id);
    }

    // Compute degree from valid relationships
    const degreeByName = new Map<string, number>();
    for (const r of validRels) {
      degreeByName.set(r.from, (degreeByName.get(r.from) ?? 0) + 1);
      degreeByName.set(r.to,   (degreeByName.get(r.to)   ?? 0) + 1);
    }

    // Build nodes
    const nodes: GraphNode[] = authors.map(a => ({
      id: a.id,
      name_zh: a.name_zh,
      nationality: a.nationality,
      hasPortrait: !!PORTRAITS[a.name_zh],
      degree: degreeByName.get(a.name_zh) ?? 0,
    }));

    const nodeById = new Map<number, GraphNode>();
    for (const n of nodes) nodeById.set(n.id, n);

    // Build links
    const links: GraphLink[] = validRels.map(r => {
      const s = authorByName.get(r.from)!;
      const t = authorByName.get(r.to)!;
      return {
        source: s.id,
        target: t.id,
        type: r.type,
        sourceId: s.id,
        targetId: t.id,
      };
    });

    // SVG setup
    const svg = d3.select(svgEl)
      .attr("width", width)
      .attr("height", height);

    // Defs for clipPaths and arrowheads
    const defs = svg.append("defs");

    // Arrowhead markers per type
    const types: RelType[] = ["影响", "师承", "平行"];
    for (const type of types) {
      defs.append("marker")
        .attr("id", `arrow-${type}`)
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 34)
        .attr("refY", 0)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5")
        .attr("fill", edgeColor(type))
        .attr("opacity", edgeOpacity(type));
    }

    // Portrait clipPaths — radius matches nodeRadius per author
    for (const n of nodes) {
      if (n.hasPortrait) {
        const R = nodeRadius(n);
        defs.append("clipPath")
          .attr("id", `clip-${n.id}`)
          .append("circle")
          .attr("r", R)
          .attr("cx", 0)
          .attr("cy", 0);
      }
    }

    // Root group with zoom
    const root = svg.append("g").attr("class", "root");

    svg.call(
      d3.zoom<SVGSVGElement, unknown>()
        .scaleExtent([0.2, 4])
        .on("zoom", (event) => {
          root.attr("transform", event.transform);
        })
    );

    // Click background to deselect
    svg.on("click", () => {
      selectedIdRef.current = null;
      setSelectedId(null);
      updateHighlight(null);
    });

    // Build adjacency set for highlight
    function getConnected(nodeId: number): Set<number> {
      const connected = new Set<number>([nodeId]);
      for (const l of links) {
        const sId = typeof l.source === "object" ? (l.source as GraphNode).id : l.source as number;
        const tId = typeof l.target === "object" ? (l.target as GraphNode).id : l.target as number;
        if (sId === nodeId) connected.add(tId);
        if (tId === nodeId) connected.add(sId);
      }
      return connected;
    }

    // Draw links
    const linkSel = root.append("g")
      .attr("class", "links")
      .selectAll<SVGLineElement, GraphLink>("line")
      .data(links)
      .join("line")
      .attr("stroke", d => edgeColor(d.type))
      .attr("stroke-opacity", d => edgeOpacity(d.type))
      .attr("stroke-width", d => edgeWidth(d.type))
      .attr("marker-end", d => `url(#arrow-${d.type})`);

    // Draw node groups
    const nodeSel = root.append("g")
      .attr("class", "nodes")
      .selectAll<SVGGElement, GraphNode>("g")
      .data(nodes)
      .join("g")
      .attr("class", "node")
      .style("cursor", "pointer");

    // Circle background
    nodeSel.append("circle")
      .attr("r", d => nodeRadius(d))
      .attr("fill", d => d.hasPortrait ? "transparent" : natColor(d.nationality))
      .attr("stroke", d => natColor(d.nationality))
      .attr("stroke-width", d => d.degree > 3 ? 2.5 : 2);

    // Portrait image via clipPath
    nodeSel.filter(d => d.hasPortrait)
      .append("image")
      .attr("href", d => PORTRAITS[d.name_zh])
      .attr("x", d => -nodeRadius(d))
      .attr("y", d => -nodeRadius(d))
      .attr("width", d => nodeRadius(d) * 2)
      .attr("height", d => nodeRadius(d) * 2)
      .attr("clip-path", d => `url(#clip-${d.id})`)
      .attr("preserveAspectRatio", "xMidYMid slice");

    // Initial letter for nodes without portrait
    nodeSel.filter(d => !d.hasPortrait)
      .append("text")
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "central")
      .attr("font-size", d => Math.max(9, nodeRadius(d) * 0.6))
      .attr("font-weight", "700")
      .attr("fill", "#fff")
      .attr("pointer-events", "none")
      .text(d => d.name_zh[0]);

    // Name label — always visible for high-degree nodes, else on hover
    const labelSel = nodeSel.append("text")
      .attr("class", "node-label")
      .attr("text-anchor", "middle")
      .attr("y", d => nodeRadius(d) + 13)
      .attr("font-size", d => d.degree >= 5 ? 12 : 10)
      .attr("font-weight", d => d.degree >= 5 ? "700" : "500")
      .attr("fill", "var(--text)")
      .attr("pointer-events", "none")
      .attr("opacity", d => d.degree >= 5 ? 0.85 : 0)
      .text(d => d.name_zh);

    // Highlight function
    function updateHighlight(activeId: number | null) {
      if (activeId === null) {
        nodeSel.attr("opacity", 1).select("transform");
        nodeSel.selectAll<SVGTextElement, GraphNode>(".node-label").attr("opacity", 0);
        linkSel.attr("opacity", 1);
        // Reset transform
        nodeSel.attr("transform", function(this: SVGGElement) {
          const el = d3.select(this);
          const tx = el.attr("data-tx") || "0";
          const ty = el.attr("data-ty") || "0";
          return `translate(${tx},${ty})`;
        });
      } else {
        const connected = getConnected(activeId);
        nodeSel.each(function(d) {
          const g = d3.select(this);
          const isConnected = connected.has(d.id);
          const isSelected = d.id === activeId;
          g.attr("opacity", isConnected ? 1 : 0.2);
          g.select<SVGTextElement>(".node-label").attr("opacity", isConnected ? 1 : 0);
          // Scale selected node
          const tx = g.attr("data-tx") || "0";
          const ty = g.attr("data-ty") || "0";
          if (isSelected) {
            g.attr("transform", `translate(${tx},${ty}) scale(1.3)`);
          } else {
            g.attr("transform", `translate(${tx},${ty})`);
          }
        });
        linkSel.each(function(d) {
          const sId = typeof d.source === "object" ? (d.source as GraphNode).id : d.source as number;
          const tId = typeof d.target === "object" ? (d.target as GraphNode).id : d.target as number;
          const isConnected = connected.has(sId) && connected.has(tId);
          d3.select(this).attr("opacity", isConnected ? 1 : 0.1);
        });
      }
    }

    // Hover: show label
    nodeSel
      .on("mouseenter", function(_, d) {
        const g = d3.select(this);
        g.select<SVGTextElement>(".node-label").attr("opacity", 1);
        if (selectedIdRef.current === null) {
          const connected = getConnected(d.id);
          nodeSel.each(function(n) {
            d3.select(this).attr("opacity", connected.has(n.id) ? 1 : 0.3);
          });
          linkSel.each(function(l) {
            const sId = typeof l.source === "object" ? (l.source as GraphNode).id : l.source as number;
            const tId = typeof l.target === "object" ? (l.target as GraphNode).id : l.target as number;
            const isConnected = connected.has(sId) && connected.has(tId);
            d3.select(this).attr("opacity", isConnected ? 1 : 0.1);
          });
        }
      })
      .on("mouseleave", function(_, d) {
        if (selectedIdRef.current === null) {
          nodeSel.attr("opacity", 1);
          linkSel.attr("opacity", 1);
          const g = d3.select(this);
          g.select<SVGTextElement>(".node-label").attr("opacity", 0);
        } else if (d.id !== selectedIdRef.current) {
          const connected = getConnected(selectedIdRef.current!);
          if (!connected.has(d.id)) {
            d3.select(this).select<SVGTextElement>(".node-label").attr("opacity", 0);
          }
        }
      });

    // Click node
    nodeSel.on("click", function(event, d) {
      event.stopPropagation();
      if (selectedIdRef.current === d.id) {
        // Navigate on second click
        router.push(`/authors/${d.id}`);
        return;
      }
      selectedIdRef.current = d.id;
      setSelectedId(d.id);
      updateHighlight(d.id);
    });

    // Drag
    const drag = d3.drag<SVGGElement, GraphNode>()
      .on("start", (event, d) => {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      })
      .on("drag", (event, d) => {
        d.fx = event.x;
        d.fy = event.y;
      })
      .on("end", (event, d) => {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      });

    nodeSel.call(drag);

    // Force simulation
    const simulation = d3.forceSimulation<GraphNode>(nodes)
      .force("link", d3.forceLink<GraphNode, GraphLink>(links)
        .id(d => d.id)
        .distance(d => {
          const s = d.source as GraphNode;
          const t = d.target as GraphNode;
          return 90 + (s.degree + t.degree) * 5;
        }))
      .force("charge", d3.forceManyBody().strength(d => -200 - (d as GraphNode).degree * 30))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide<GraphNode>(d => nodeRadius(d) + 6))
      .on("tick", () => {
        linkSel
          .attr("x1", d => (d.source as GraphNode).x ?? 0)
          .attr("y1", d => (d.source as GraphNode).y ?? 0)
          .attr("x2", d => (d.target as GraphNode).x ?? 0)
          .attr("y2", d => (d.target as GraphNode).y ?? 0);

        nodeSel.attr("transform", function(d) {
          const x = d.x ?? 0;
          const y = d.y ?? 0;
          d3.select(this).attr("data-tx", x).attr("data-ty", y);
          const isSelected = d.id === selectedIdRef.current;
          return isSelected
            ? `translate(${x},${y}) scale(1.3)`
            : `translate(${x},${y})`;
        });
      });

    return () => {
      simulation.stop();
    };
  }, [authors, loading, router]);

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "var(--bg)",
        color: "var(--text)",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Header */}
      <header
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "12px 32px",
          borderBottom: "1px solid var(--border)",
          background: "var(--bg)",
          flexShrink: 0,
        }}
      >
        <button
          onClick={() => router.push("/")}
          style={{
            display: "flex",
            alignItems: "center",
            gap: 4,
            fontSize: "0.875rem",
            color: "var(--text-m)",
            background: "none",
            border: "none",
            cursor: "pointer",
          }}
        >
          ← 返回年表
        </button>
        <span
          style={{
            fontWeight: 700,
            fontSize: "1rem",
            color: "var(--text)",
          }}
        >
          文学影响关系图
        </span>
        <ThemeToggle />
      </header>

      {/* Graph area */}
      <div
        ref={containerRef}
        style={{
          flex: 1,
          position: "relative",
          overflow: "hidden",
        }}
      >
        {loading ? (
          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "var(--text-m)",
              fontSize: "0.9rem",
            }}
          >
            加载中…
          </div>
        ) : (
          <svg
            ref={svgRef}
            style={{ width: "100%", height: "100%", display: "block" }}
          />
        )}

        {/* Selected node hint */}
        {selectedId !== null && (
          <div
            style={{
              position: "absolute",
              bottom: 80,
              left: "50%",
              transform: "translateX(-50%)",
              background: "var(--surface)",
              border: "1px solid var(--border)",
              borderRadius: 8,
              padding: "6px 16px",
              fontSize: "0.8rem",
              color: "var(--text-m)",
              pointerEvents: "none",
            }}
          >
            再次点击节点前往作家详情页
          </div>
        )}

        {/* Legend */}
        <div
          style={{
            position: "absolute",
            bottom: 20,
            right: 20,
            background: "var(--surface)",
            border: "1px solid var(--border)",
            borderRadius: 10,
            padding: "12px 16px",
            fontSize: "0.75rem",
            color: "var(--text)",
            minWidth: 180,
          }}
        >
          <div style={{ fontWeight: 700, marginBottom: 8, color: "var(--text)" }}>关系类型</div>
          {(["影响", "师承", "平行"] as RelType[]).map(type => (
            <div key={type} style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 5 }}>
              <svg width="32" height="10">
                <line
                  x1="0" y1="5" x2="28" y2="5"
                  stroke={edgeColor(type)}
                  strokeWidth={edgeWidth(type)}
                  strokeOpacity={edgeOpacity(type)}
                />
              </svg>
              <span style={{ color: "var(--text-m)" }}>{type}</span>
            </div>
          ))}

          <div style={{ fontWeight: 700, margin: "10px 0 8px", color: "var(--text)" }}>国籍</div>
          {[
            { label: "中国", color: "#ef4444" },
            { label: "古希腊/罗马", color: "#f59e0b" },
            { label: "俄国/苏联", color: "#f97316" },
            { label: "法国", color: "#3b82f6" },
            { label: "英美/爱尔兰", color: "#8b5cf6" },
            { label: "其他", color: "#10b981" },
          ].map(({ label, color }) => (
            <div key={label} style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 5 }}>
              <div
                style={{
                  width: 12,
                  height: 12,
                  borderRadius: "50%",
                  background: color,
                  flexShrink: 0,
                }}
              />
              <span style={{ color: "var(--text-m)" }}>{label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
