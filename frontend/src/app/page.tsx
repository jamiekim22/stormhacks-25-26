import PageTemplate from "@/components/PageTemplate";

const metricCards = [
  { title: 'Active Campaigns', value: '4' },
  { title: 'Vulnerability Score', value: '65' },
  { title: 'Voice Calls Today', value: '7' },
  { title: 'Training Completion', value: '82%' },
];

const recentActivities = [
  { time: '10:25 AM', description: 'New campaign launched', pairedTime: '9:02 AM', pairedDescription: 'Campaign paused' },
  { time: '9:50 AM', description: 'Employee marked as vulnerable', pairedTime: '8:45 AM', pairedDescription: 'Voice call recorded' },
  { time: '8:02 AM', description: 'Campaign paused', pairedTime: '8:30 AM', pairedDescription: 'Report exported' },
];

export default function HomePage() {
  return (
    <PageTemplate
      title="Dashboard"
      description="Stay on top of phishing simulations and employee readiness."
      bodyClassName="space-y-8"
    >
      <section className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        {metricCards.map((card) => (
          <div key={card.title} className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)]/90 px-6 py-6 shadow-[0_18px_40px_rgba(5,12,26,0.35)]">
            <p className="text-xs uppercase tracking-wide text-[var(--color-text-muted)]">{card.title}</p>
            <p className="mt-5 text-4xl font-semibold text-white">{card.value}</p>
            <div className="mt-6 h-1.5 rounded-full bg-[#1f2b40]">
              <div className="h-full rounded-full bg-[var(--color-accent)]/80" style={{ width: '65%' }} />
            </div>
          </div>
        ))}
      </section>

      <section className="grid gap-5 lg:grid-cols-2">
        <div className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)]/90 px-6 py-6 shadow-[0_18px_40px_rgba(5,12,26,0.35)]">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white">Campaign Status</h2>
            <span className="text-xs text-[var(--color-text-muted)]">This week</span>
          </div>
          <div className="mt-8 h-48 rounded-xl bg-[#0b1528] flex items-center justify-center text-sm text-[var(--color-text-muted)]">
            Line chart placeholder
          </div>
        </div>

        <div className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)]/90 px-6 py-6 shadow-[0_18px_40px_rgba(5,12,26,0.35)]">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white">Campaign Outcomes</h2>
            <span className="text-xs text-[var(--color-text-muted)]">Rolling 30 days</span>
          </div>
          <div className="mt-8 h-48 rounded-xl bg-[#0b1528] flex items-center justify-center text-sm text-[var(--color-text-muted)]">
            Donut chart placeholder
          </div>
        </div>
      </section>

      <section className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)]/90 px-6 py-6 shadow-[0_18px_40px_rgba(5,12,26,0.35)]">
        <h2 className="text-lg font-semibold text-white">Recent Activities</h2>
        <div className="mt-6 space-y-4 text-sm">
          {recentActivities.map((item) => (
            <div key={item.time} className="grid gap-4 md:grid-cols-2">
              <div className="flex gap-4">
                <span className="min-w-[70px] text-[var(--color-text-muted)]">{item.time}</span>
                <span className="text-white">{item.description}</span>
              </div>
              <div className="flex gap-4 text-left md:text-right md:justify-end">
                <span className="min-w-[70px] text-[var(--color-text-muted)]">{item.pairedTime}</span>
                <span className="text-white">{item.pairedDescription}</span>
              </div>
            </div>
          ))}
        </div>
      </section>
    </PageTemplate>
  );
}