"use client";

import { healthSignals } from "@/lib/data";

export function HealthIndicator() {
  return (
    <div className="rounded-lg border border-outline-variant bg-surface-container-low p-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-on-surface-variant">System health</p>
          <h2 className="mt-2 font-geist text-2xl font-semibold text-on-surface">Verification stack</h2>
        </div>
        <span className="rounded-full bg-secondary/12 px-3 py-1 text-xs font-bold text-secondary">Live</span>
      </div>
      <div className="mt-5 grid gap-3 sm:grid-cols-2">
        {healthSignals.map((signal) => (
          <div key={signal.label} className="rounded-lg border border-outline-variant/60 bg-background/60 p-4">
            <div className="flex items-center justify-between gap-3">
              <p className="text-sm font-semibold text-on-surface">{signal.label}</p>
              <span className={signal.status === "Operational" ? "text-secondary" : "text-tertiary"}>{signal.value}</span>
            </div>
            <p className="mt-2 text-xs text-on-surface-variant">{signal.status}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
