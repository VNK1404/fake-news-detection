import { AppShell } from "@/components/AppShell";

const settings = [
  ["Theme", "Synced through Zustand and applied to document theme variables."],
  ["API URL", "Read from NEXT_PUBLIC_API_URL in the typed API client."],
  ["Report mode", "Prepared for PDF download once backend integration is enabled."],
  ["Pipeline animation", "Framer Motion stages reflect the full evidence workflow."],
];

export default function SettingsPage() {
  return (
    <AppShell>
      <section>
        <p className="text-xs font-bold uppercase tracking-[0.16em] text-primary">Settings</p>
        <h1 className="mt-3 font-geist text-4xl font-bold text-on-surface">Control surface</h1>
      </section>
      <div className="grid gap-4 md:grid-cols-2">
        {settings.map(([label, description]) => (
          <div key={label} className="rounded-lg border border-outline-variant bg-surface-container-low p-5">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="font-geist text-xl font-semibold text-on-surface">{label}</h2>
                <p className="mt-2 text-sm leading-6 text-on-surface-variant">{description}</p>
              </div>
              <label className="relative inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full bg-surface-container-high">
                <input className="peer sr-only" type="checkbox" defaultChecked />
                <span className="absolute left-1 size-4 rounded-full bg-primary transition peer-checked:translate-x-5" />
              </label>
            </div>
          </div>
        ))}
      </div>
    </AppShell>
  );
}
