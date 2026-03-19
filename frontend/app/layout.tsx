import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "作家年表",
  description: "将世界文学史变成一张可以探索的地图",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <head>
        {/* FOUC 防闪：在渲染前读取主题偏好 */}
        <script dangerouslySetInnerHTML={{ __html: `(function(){
          try {
            var t = localStorage.getItem('theme') || 'dark';
            if (t === 'dark') document.documentElement.classList.add('dark');
          } catch(e) {
            document.documentElement.classList.add('dark');
          }
        })();` }} />
      </head>
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        {children}
      </body>
    </html>
  );
}
