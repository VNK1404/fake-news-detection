"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import { Activity, Menu } from "lucide-react";
import { navItems } from "@/lib/data";

export function SideNavBar() {
  const pathname = usePathname();

  return (
    <>
      <div className="fixed left-4 top-4 z-50 lg:hidden">
        <button className="grid size-11 place-items-center rounded-lg border border-outline-variant bg-surface-container/90 text-on-surface shadow-panel backdrop-blur">
          <Menu size={20} />
        </button>
      </div>
      <aside className="fixed left-0 top-0 z-40 hidden h-full w-[280px] flex-col border-r border-outline-variant/60 bg-background/86 px-4 py-6 backdrop-blur-xl lg:flex">
        <Link href="/" className="mb-10 block px-2">
          <p className="font-geist text-2xl font-bold text-primary">VeriNews AI</p>
          <p className="mt-1 text-xs font-medium uppercase tracking-[0.18em] text-on-surface-variant">Intelligence Suite</p>
        </Link>

        <nav className="flex flex-1 flex-col gap-1">
          {navItems.map((item) => {
            const active = pathname === item.href;
            const Icon = item.icon;
            return (
              <Link key={item.href} href={item.href} className="relative">
                <motion.span
                  whileHover={{ x: 3 }}
                  className={`flex items-center gap-3 rounded-lg px-3 py-3 text-sm font-medium transition ${
                    active ? "bg-surface-container-high text-primary" : "text-on-surface-variant hover:bg-surface-container-low hover:text-on-surface"
                  }`}
                >
                  <Icon size={19} />
                  {item.label}
                </motion.span>
                {active ? <span className="absolute right-0 top-2 h-8 w-0.5 rounded-full bg-primary" /> : null}
              </Link>
            );
          })}
        </nav>

        <div className="rounded-lg border border-outline-variant/60 bg-surface-container-low p-4">
          <div className="mb-3 flex items-center gap-3">
            <span className="grid size-9 place-items-center rounded-lg bg-secondary/15 text-secondary">
              <Activity size={18} />
            </span>
            <div>
              <p className="text-sm font-semibold text-on-surface">V-Node 01</p>
              <p className="text-xs text-secondary">Active cluster</p>
            </div>
          </div>
          <div className="h-1.5 rounded-full bg-surface-container-high">
            <div className="h-full w-[82%] rounded-full bg-secondary" />
          </div>
        </div>
      </aside>
    </>
  );
}
