export default function EmployeesPage() {
  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-semibold text-white">Employees</h1>
        <p className="text-sm text-[var(--color-text-muted)] mt-1">Track employee readiness, risk posture, and training milestones.</p>
      </header>

      <div className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)]/90 px-10 py-14 text-center shadow-[0_18px_40px_rgba(5,12,26,0.35)]">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-[var(--color-accent)]/15 text-[var(--color-accent)]">
          <svg className="h-7 w-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 11c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
          </svg>
        </div>
        <h2 className="mt-6 text-2xl font-semibold text-white">Employee analytics coming soon</h2>
        <p className="mt-3 text-sm text-[var(--color-text-muted)]">Benchmark departments, assign targeted training, and surface highest-risk users instantly.</p>
      </div>
    </div>
  );
}
