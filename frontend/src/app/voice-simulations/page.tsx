export default function VoiceSimulationsPage() {
  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-semibold text-white">Voice Simulations</h1>
        <p className="text-sm text-[var(--color-text-muted)] mt-1">Manage vishing scenarios, monitor call quality, and analyse AI-guided conversations.</p>
      </header>

      <div className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)]/90 px-10 py-14 text-center shadow-[0_18px_40px_rgba(5,12,26,0.35)]">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-[var(--color-accent)]/15 text-[var(--color-accent)]">
          <svg className="h-7 w-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2 8.5c1.72 3.82 5 7.1 8.82 8.82L13 15l5 5-2.5 2.5C9 21 3 15 1.5 8.5L4 6l-2-2 3-3 5 5-3 3z" />
          </svg>
        </div>
        <h2 className="mt-6 text-2xl font-semibold text-white">Voice command center coming soon</h2>
        <p className="mt-3 text-sm text-[var(--color-text-muted)]">Replay recordings, inspect sentiment, and orchestrate blended voice + email scenarios.</p>
      </div>
    </div>
  );
}
