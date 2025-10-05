export default function AnalyticsPage() {
  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-semibold text-white">Analytics</h1>
        <p className="text-sm text-[var(--color-text-muted)] mt-1">Generate executive-ready insights across channels, personas, and training efforts.</p>
      </header>

      <div className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)]/90 px-10 py-14 text-center shadow-[0_18px_40px_rgba(5,12,26,0.35)]">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-[var(--color-accent)]/15 text-[var(--color-accent)]">
          <svg className="h-7 w-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 3v18m-4-4h8m-8-5h8m-8-5h8" />
          </svg>
        </div>
        <h2 className="mt-6 text-2xl font-semibold text-white">Analytics dashboard coming soon</h2>
        <p className="mt-3 text-sm text-[var(--color-text-muted)]">Visualize click-throughs, voice simulation outcomes, and compliance KPIs with powerful filters.</p>
      </div>
    </div>
  );
}
