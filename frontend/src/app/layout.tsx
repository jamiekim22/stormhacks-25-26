import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/Sidebar";

export const metadata: Metadata = {
  title: "PhishPatrol Pro - Advanced Phishing Simulation Platform",
  description: "Comprehensive cybersecurity training platform with voice and email simulation capabilities",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        <div className="flex min-h-screen bg-transparent">
          <Sidebar />
          <main className="flex-1 overflow-auto">
            <div className="min-h-screen bg-transparent px-10 py-10">
              {children}
            </div>
          </main>
        </div>
      </body>
    </html>
  );
}
