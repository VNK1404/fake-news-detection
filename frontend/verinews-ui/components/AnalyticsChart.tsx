"use client";

import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { analyticsSeries } from "@/lib/data";

export function AnalyticsChart() {
  return (
    <div className="h-[360px] rounded-lg border border-outline-variant bg-surface-container-low p-5">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-on-surface-variant">Verdict distribution</p>
          <h2 className="mt-2 font-geist text-2xl font-semibold text-on-surface">Claims analyzed over time</h2>
        </div>
      </div>
      <ResponsiveContainer width="100%" height="78%">
        <AreaChart data={analyticsSeries}>
          <defs>
            <linearGradient id="real" x1="0" x2="0" y1="0" y2="1">
              <stop offset="5%" stopColor="#4cd7f6" stopOpacity={0.5} />
              <stop offset="95%" stopColor="#4cd7f6" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="false" x1="0" x2="0" y1="0" y2="1">
              <stop offset="5%" stopColor="#ffb4ab" stopOpacity={0.45} />
              <stop offset="95%" stopColor="#ffb4ab" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid stroke="#353437" strokeDasharray="3 3" />
          <XAxis dataKey="day" stroke="#c7c4d7" tickLine={false} />
          <YAxis stroke="#c7c4d7" tickLine={false} />
          <Tooltip contentStyle={{ background: "#1c1b1d", border: "1px solid #464554", borderRadius: 8 }} />
          <Area type="monotone" dataKey="real" stroke="#4cd7f6" fill="url(#real)" />
          <Area type="monotone" dataKey="false" stroke="#ffb4ab" fill="url(#false)" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
