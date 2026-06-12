import { AppShell } from "@/components/AppShell";
import { ReportTable } from "@/components/ReportTable";

export default function ReportsPage() {
  return (
    <AppShell>
      <section>
        <p className="text-xs font-bold uppercase tracking-[0.16em] text-primary">Reports</p>
        <h1 className="mt-3 font-geist text-4xl font-bold text-on-surface">PDF evidence archive</h1>
        <p className="mt-3 max-w-2xl text-on-surface-variant">
          Browse generated report packages. Live download integration is prepared in the API client and ready for backend wiring.
        </p>
      </section>
      <ReportTable />
    </AppShell>
  );
}
