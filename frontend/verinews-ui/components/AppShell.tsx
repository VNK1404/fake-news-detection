"use client";

import { motion } from "framer-motion";
import { TopNavBar } from "@/components/TopNavBar";
import { SideNavBar } from "@/components/SideNavBar";

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <SideNavBar />
      <div className="min-h-screen lg:pl-[280px]">
        <TopNavBar />
        <motion.main
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, ease: "easeOut" }}
          className="mx-auto flex w-full max-w-[1440px] flex-col gap-8 px-4 pb-10 pt-24 sm:px-6 lg:px-10"
        >
          {children}
        </motion.main>
      </div>
    </div>
  );
}
