"use client";

interface Props {
  authorId: number;
  authorName: string;
}

export default function AuthorCard({ authorId, authorName }: Props) {
  return (
    <div className="inline-flex items-center gap-2 bg-gray-800 rounded-lg px-3 py-2 text-sm">
      <div className="w-8 h-8 rounded-full bg-blue-700 flex items-center justify-center font-bold text-white text-xs">
        {authorName[0]}
      </div>
      <span className="text-gray-200">{authorName}</span>
    </div>
  );
}
