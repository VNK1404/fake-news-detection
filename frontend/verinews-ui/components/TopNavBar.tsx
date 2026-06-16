"use client";

import { Bell, Moon, Search, Sun } from "lucide-react";
import { useAppStore } from "@/store/useAppStore";

export function TopNavBar() {
  const theme = useAppStore((state) => state.theme);
  const setTheme = useAppStore((state) => state.setTheme);

  return (
    <header className="fixed right-0 top-0 z-30 flex h-16 w-full items-center justify-between border-b border-outline-variant/40 bg-background/70 px-4 backdrop-blur-xl lg:w-[calc(100%-280px)] lg:px-8">
      <div className="ml-14 flex w-full max-w-xl items-center gap-3 rounded-full border border-outline-variant/50 bg-surface-container-low px-4 py-2 text-on-surface-variant lg:ml-0">
        <Search size={18} />
        <input
          aria-label="Search claims"
          placeholder="Search claims, reports, sources..."
          className="w-full bg-transparent text-sm text-on-surface outline-none placeholder:text-on-surface-variant/70"
        />
      </div>
      <div className="ml-4 flex items-center gap-2">
        <button className="grid size-10 place-items-center rounded-lg text-on-surface-variant hover:bg-surface-container-high hover:text-primary" aria-label="Notifications">
          <Bell size={18} />
        </button>
        <button
          className="grid size-10 place-items-center rounded-lg text-on-surface-variant hover:bg-surface-container-high hover:text-primary"
          aria-label="Toggle theme"
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        >
          {theme === "dark" ? <Moon size={18} /> : <Sun size={18} />}
        </button>
      </div>
    </header>
  );
}
