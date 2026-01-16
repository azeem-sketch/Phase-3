import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Evolution Todo | Modern Task Management",
  description: "A premium full-stack todo application with Better Auth and FastAPI.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Navbar />
        <main className="flex-1">
          {children}
        </main>
        <footer className="py-8 text-center text-text-muted text-sm border-t border-card-border mt-auto">
          &copy; {new Date().getFullYear()} Evolution of Todo. All rights reserved.
        </footer>
      </body>
    </html>
  );
}
