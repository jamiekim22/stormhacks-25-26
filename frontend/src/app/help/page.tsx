import PageTemplate from "@/components/PageTemplate";

export default function HelpPage() {
  return (
    <PageTemplate
      title="Help & Support"
      description="Access knowledge base articles, tutorials, and live assistance."
      bodyClassName="px-10 py-14 text-center"
    >
      <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-[var(--color-accent)]/15 text-[var(--color-accent)]">
        <svg className="h-7 w-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h2 className="mt-6 text-2xl font-semibold text-white">Support hub coming soon</h2>
      <p className="mt-3 text-sm text-[var(--color-text-muted)]">Get guided onboarding, voice simulation tips, and incident response playbooks.</p>
    </PageTemplate>
  );
}
