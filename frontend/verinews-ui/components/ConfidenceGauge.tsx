"use client";

import { motion } from "framer-motion";

export function ConfidenceGauge({ value = 91 }: { value?: number }) {
  const radius = 72;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;

  return (
    <div className="rounded-lg border border-outline-variant bg-surface-container-low p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-on-surface-variant">Confidence gauge</p>
          <p className="mt-2 text-sm text-on-surface-variant">Weighted consensus across model, source, and verification signals.</p>
        </div>
      </div>
      <div className="mt-6 grid place-items-center">
        <svg className="size-44 -rotate-90" viewBox="0 0 180 180">
          <circle cx="90" cy="90" r={radius} fill="none" stroke="var(--surface-container-high)" strokeWidth="14" />
          <motion.circle
            cx="90"
            cy="90"
            r={radius}
            fill="none"
            stroke="var(--secondary)"
            strokeLinecap="round"
            strokeWidth="14"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1, ease: "easeOut" }}
          />
        </svg>
        <div className="absolute text-center">
          <p className="font-geist text-4xl font-bold text-on-surface">{value}%</p>
          <p className="text-xs text-on-surface-variant">High</p>
        </div>
      </div>
    </div>
  );
}
