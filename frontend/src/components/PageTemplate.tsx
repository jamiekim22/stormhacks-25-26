import { ReactNode } from "react";

interface PageTemplateProps {
  title: string;
  description: string;
  children: ReactNode;
  bodyClassName?: string;
}

export default function PageTemplate({
  title,
  description,
  children,
  bodyClassName,
}: PageTemplateProps) {
  const baseBodyClassName =
    "rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)]/90 px-8 py-8 shadow-[0_18px_40px_rgba(5,12,26,0.35)]";
  const mergedBodyClassName = bodyClassName
    ? `${baseBodyClassName} ${bodyClassName}`
    : baseBodyClassName;

  return (
    <div className="space-y-8 paddingClass">
      <div className="paddingClass">
        <h1 className="text-3xl font-semibold text-white">{title}</h1>
        <p className="mt-1 text-sm text-[var(--color-text-muted)]">{description}</p>
      </div>

      <div className={mergedBodyClassName}>
        {children}
      </div>
    </div>
  );
}
