import { AppShell } from "@/components/AppShell";
import { ConfidenceGauge } from "@/components/ConfidenceGauge";
import { SimilarityCard } from "@/components/SimilarityCard";
import { TrustMeter } from "@/components/TrustMeter";
import { VerdictCard } from "@/components/VerdictCard";
import { evidenceItems } from "@/lib/data";

export default function ResultsPage() {
  return (
    <AppShell>
      <section>
        <p className="text-xs font-bold uppercase tracking-[0.16em] text-primary">Analysis results</p>
        <h1 className="mt-3 font-geist text-4xl font-bold text-on-surface">Evidence verdict dashboard</h1>
      </section>
      <VerdictCard />
      <div className="grid gap-6 xl:grid-cols-[0.8fr_1.2fr]">
        <ConfidenceGauge />
        <TrustMeter />
      </div>
      <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <SimilarityCard />
        <section className="rounded-lg border border-outline-variant bg-surface-container-low p-5">
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-on-surface-variant">Explainability reasons</p>
          <div className="mt-4 space-y-3">
            {evidenceItems.map((item) => (
              <p key={item} className="rounded-lg border border-outline-variant/60 bg-background/60 p-4 text-sm leading-6 text-on-surface-variant">
                {item}
              </p>
            ))}
          </div>
        </section>
      </div>
    </AppShell>
  );
}
