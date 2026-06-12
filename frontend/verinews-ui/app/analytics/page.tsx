import { AppShell } from "@/components/AppShell";
import { AnalyticsChart } from "@/components/AnalyticsChart";
import { HealthIndicator } from "@/components/HealthIndicator";

export default function AnalyticsPage() {
  return (
    <AppShell>
      <section>
        <p className="text-xs font-bold uppercase tracking-[0.16em] text-primary">Analytics</p>
        <h1 className="mt-3 font-geist text-4xl font-bold text-on-surface">Operational intelligence</h1>
      </section>
      <div className="grid gap-4 md:grid-cols-4">
        {[
          ["1.2M", "Total analyses"],
          ["94.2%", "Avg confidence"],
          ["1.8s", "Avg latency"],
          ["99.1%", "API success"],
        ].map(([value, label]) => (
          <div key={label} className="rounded-lg border border-outline-variant bg-surface-container-low p-5">
            <p className="font-geist text-3xl font-bold text-on-surface">{value}</p>
            <p className="mt-2 text-sm text-on-surface-variant">{label}</p>
          </div>
        ))}
      </div>
      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <AnalyticsChart />
        <HealthIndicator />
      </div>
    </AppShell>
  );
}
