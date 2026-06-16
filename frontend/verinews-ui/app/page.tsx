import { AppShell } from "@/components/AppShell";
import { AnalyticsChart } from "@/components/AnalyticsChart";
import { HeroSection } from "@/components/HeroSection";
import { LoadingPipeline } from "@/components/LoadingPipeline";

export default function LandingPage() {
  return (
    <AppShell>
      <HeroSection />
      <section className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
        <AnalyticsChart />
        <LoadingPipeline compact />
      </section>
    </AppShell>
  );
}
