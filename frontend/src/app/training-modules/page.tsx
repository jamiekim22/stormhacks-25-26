import PageTemplate from "@/components/PageTemplate";

export default function TrainingModulesPage() {
  return (
    <PageTemplate
      title="Training Modules"
      description="Deliver personalized awareness paths and track learner mastery."
      bodyClassName="px-10 py-14 text-center"
    >
      <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-[var(--color-accent)]/15 text-[var(--color-accent)]">
        <svg className="h-7 w-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6h4" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 12a8 8 0 11-16 0 8 8 0 0116 0z" />
        </svg>
      </div>
      <h2 className="mt-6 text-2xl font-semibold text-white">Training library coming soon</h2>
      <p className="mt-3 text-sm text-[var(--color-text-muted)]">Launch immersive phishing drills, host microlearning, and award certifications automatically.</p>
    </PageTemplate>
  );
}
