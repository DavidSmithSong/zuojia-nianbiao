"use client";

import { useEffect, useState } from "react";

export default function ThemeToggle() {
  const [isDark, setIsDark] = useState(true);

  useEffect(() => {
    setIsDark(document.documentElement.classList.contains("dark"));
  }, []);

  function toggle() {
    const next = !isDark;
    setIsDark(next);
    if (next) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }

  return (
    <button
      onClick={toggle}
      title={isDark ? "切换浅色模式" : "切换深色模式"}
      style={{
        padding: "4px 12px",
        borderRadius: 8,
        fontSize: "0.8rem",
        background: "var(--surface2)",
        color: "var(--text)",
        border: "1px solid var(--border)",
        cursor: "pointer",
        transition: "background 0.15s",
        whiteSpace: "nowrap",
      }}
    >
      {isDark ? "☀ 明" : "☾ 暗"}
    </button>
  );
}
