"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, ShieldCheck } from "lucide-react";
import { HealthIndicator } from "@/components/HealthIndicator";

export function HeroSection() {
  return (
    <section className="grid min-h-[calc(100vh-6rem)] items-center gap-8 lg:grid-cols-[1.08fr_0.92fr]">
      <div className="space-y-8">
        <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.45 }} className="space-y-5">
          <span className="inline-flex items-center gap-2 rounded-full border border-primary/35 bg-primary/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] text-primary">
            <ShieldCheck size={14} />
            AI Evidence Integrity Monitor
          </span>
          <h1 className="max-w-4xl font-geist text-5xl font-bold leading-tight text-on-surface md:text-7xl">
            VeriNews AI
          </h1>
          <p className="max-w-2xl text-lg leading-8 text-on-surface-variant">
            A production command center for claim analysis, semantic evidence retrieval, source trust scoring, explainability, and report generation.
          </p>
        </motion.div>
        <div className="flex flex-col gap-3 sm:flex-row">
          <Link href="/analyze" className="inline-flex h-12 items-center justify-center gap-2 rounded-lg bg-primary px-5 text-sm font-bold text-on-primary shadow-glow transition hover:bg-primary-container">
            Start analysis
            <ArrowRight size={17} />
          </Link>
          <Link href="/analytics" className="inline-flex h-12 items-center justify-center rounded-lg border border-outline-variant px-5 text-sm font-semibold text-on-surface transition hover:bg-surface-container-high">
            View analytics
          </Link>
        </div>
      </div>
      <div className="grid gap-4">
        <HealthIndicator />
        <div className="grid grid-cols-2 gap-4">
          {[
            ["99.96%", "Classifier F1"],
            ["44.8K", "Indexed claims"],
            ["6", "Evidence signals"],
            ["PDF", "Report ready"],
          ].map(([value, label]) => (
            <motion.div whileHover={{ y: -3 }} key={label} className="rounded-lg border border-outline-variant bg-surface-container-low p-5">
              <p className="font-geist text-3xl font-bold text-on-surface">{value}</p>
              <p className="mt-1 text-sm text-on-surface-variant">{label}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
