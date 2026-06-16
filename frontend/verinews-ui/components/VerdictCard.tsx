"use client";

import { motion } from "framer-motion";
import { AlertTriangle, CheckCircle2, XCircle } from "lucide-react";

const verdictStyles = {
  Verified: { icon: CheckCircle2, color: "text-secondary", bg: "bg-secondary/12", label: "Verified" },
  False: { icon: XCircle, color: "text-error", bg: "bg-error/12", label: "False" },
  Questionable: { icon: AlertTriangle, color: "text-tertiary", bg: "bg-tertiary/12", label: "Questionable" },
};

export function VerdictCard({ verdict = "False", confidence = 91, score = -0.84 }: { verdict?: keyof typeof verdictStyles; confidence?: number; score?: number }) {
  const style = verdictStyles[verdict];
  const Icon = style.icon;

  return (
    <motion.section whileHover={{ y: -3 }} className="relative overflow-hidden rounded-lg border border-outline-variant bg-surface-container-low p-6 shadow-panel">
      <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-primary via-secondary to-tertiary" />
      <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-4">
          <span className={`grid size-16 place-items-center rounded-lg ${style.bg} ${style.color}`}>
            <Icon size={34} />
          </span>
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.16em] text-on-surface-variant">Final verdict</p>
            <h2 className={`mt-2 font-geist text-4xl font-bold ${style.color}`}>{style.label}</h2>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-3 sm:w-64">
          <div className="rounded-lg border border-outline-variant bg-background/60 p-4">
            <p className="text-xs text-on-surface-variant">Confidence</p>
            <p className="mt-1 font-geist text-2xl font-bold text-on-surface">{confidence}%</p>
          </div>
          <div className="rounded-lg border border-outline-variant bg-background/60 p-4">
            <p className="text-xs text-on-surface-variant">Score</p>
            <p className="mt-1 font-geist text-2xl font-bold text-on-surface">{score.toFixed(2)}</p>
          </div>
        </div>
      </div>
    </motion.section>
  );
}
