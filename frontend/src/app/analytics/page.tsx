import PageTemplate from "@/components/PageTemplate";

export default function AnalyticsPage() {
  return (
    <PageTemplate
      title="Analytics"
      description="Generate executive-ready insights across channels, personas, and training efforts."
      bodyClassName="px-10 py-14 text-center"
    >
      <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-[var(--color-accent)]/15 text-[var(--color-accent)]">
        <svg className="h-7 w-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 3v18m-4-4h8m-8-5h8m-8-5h8" />
        </svg>
      </div>
      <h2 className="mt-6 text-2xl font-semibold text-white">Analytics dashboard coming soon</h2>
      <p className="mt-3 text-sm text-[var(--color-text-muted)]">Visualize click-throughs, voice simulation outcomes, and compliance KPIs with powerful filters.</p>
    </PageTemplate>
  );
}
