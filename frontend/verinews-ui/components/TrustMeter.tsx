"use client";

import { trustSignals } from "@/lib/data";

export function TrustMeter() {
  return (
    <div className="rounded-lg border border-outline-variant bg-surface-container-low p-5">
      <p className="text-xs font-bold uppercase tracking-[0.16em] text-on-surface-variant">Evidence trust meter</p>
      <div className="mt-5 space-y-4">
        {trustSignals.map((signal) => (
          <div key={signal.label}>
            <div className="mb-2 flex justify-between text-sm">
              <span className="text-on-surface">{signal.label}</span>
              <span className="font-semibold text-secondary">{signal.value}%</span>
            </div>
            <div className="h-2 rounded-full bg-surface-container-high">
              <div className="h-full rounded-full bg-gradient-to-r from-primary to-secondary" style={{ width: `${signal.value}%` }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
