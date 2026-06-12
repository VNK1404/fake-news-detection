import { AppShell } from "@/components/AppShell";
import { LoadingPipeline } from "@/components/LoadingPipeline";
import { UploadZone } from "@/components/UploadZone";

export default function AnalyzePage() {
  return (
    <AppShell>
      <section>
        <p className="text-xs font-bold uppercase tracking-[0.16em] text-primary">Analyze news</p>
        <h1 className="mt-3 font-geist text-4xl font-bold text-on-surface">Claim intake workspace</h1>
        <p className="mt-3 max-w-2xl text-on-surface-variant">
          Stage a file or claim for the verification pipeline. API calls are prepared but intentionally not connected yet.
        </p>
      </section>
      <div className="grid gap-6 xl:grid-cols-[1fr_0.86fr]">
        <UploadZone />
        <div className="rounded-lg border border-outline-variant bg-surface-container-low p-5">
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-on-surface-variant">Claim text</p>
          <textarea
            className="mt-4 min-h-[220px] w-full resize-none rounded-lg border border-outline-variant bg-background p-4 text-sm leading-6 text-on-surface outline-none transition focus:border-secondary"
            placeholder="Paste a claim, article excerpt, or source URL..."
          />
          <button className="mt-4 w-full rounded-lg bg-primary px-5 py-3 text-sm font-bold text-on-primary transition hover:bg-primary-container">
            Queue analysis
          </button>
        </div>
      </div>
      <LoadingPipeline />
    </AppShell>
  );
}
