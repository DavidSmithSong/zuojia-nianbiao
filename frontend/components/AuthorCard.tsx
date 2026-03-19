"use client";

interface Props {
  authorId: number;
  authorName: string;
  portraitUrl?: string;
}

export default function AuthorCard({ authorId, authorName, portraitUrl }: Props) {
  return (
    <div
      className="inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm"
      style={{ background: "var(--surface2)", border: "1px solid var(--border)" }}
    >
      {portraitUrl ? (
        <img
          src={portraitUrl}
          alt={authorName}
          style={{ width: 32, height: 32, borderRadius: "50%", objectFit: "cover", flexShrink: 0 }}
        />
      ) : (
        <div
          style={{
            width: 32, height: 32, borderRadius: "50%",
            background: "#1d4ed8",
            display: "flex", alignItems: "center", justifyContent: "center",
            color: "#fff", fontSize: 12, fontWeight: 700, flexShrink: 0,
          }}
        >
          {authorName[0]}
        </div>
      )}
      <span style={{ color: "var(--text)" }}>{authorName}</span>
    </div>
  );
}
