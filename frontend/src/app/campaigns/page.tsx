import PageTemplate from "@/components/PageTemplate";

export default function CampaignsPage() {
  return (
    <PageTemplate
      title="Campaigns"
      description="Coordinate, launch, and analyse phishing simulation campaigns."
      bodyClassName="px-10 py-14 text-center"
    >
      <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-[var(--color-accent)]/15 text-[var(--color-accent)]">
        <svg className="h-7 w-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 13h3l3 8 4-16 3 8h5" />
        </svg>
      </div>
      <h2 className="mt-6 text-2xl font-semibold text-white">Campaign workspace coming soon</h2>
      <p className="mt-3 text-sm text-[var(--color-text-muted)]">Plan multi-channel simulations, automate schedules, and track campaign effectiveness in real time.</p>
    </PageTemplate>
  );
}
