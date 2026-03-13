import Timeline from "@/components/Timeline";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-950 text-gray-100">
      <header className="px-8 py-6 border-b border-gray-800">
        <h1 className="text-2xl font-bold tracking-wide">作家年表</h1>
        <p className="text-gray-400 text-sm mt-1">将世界文学史变成一张可以探索的地图</p>
      </header>
      <Timeline />
    </main>
  );
}
