import type { ReactNode } from "react";

export function Card({
  title,
  description,
  children,
  footer,
}: {
  title?: ReactNode;
  description?: ReactNode;
  children?: ReactNode;
  footer?: ReactNode;
}) {
  return (
    <section className="rounded-lg bg-white p-6 ring-1 ring-line">
      {title ? (
        <h2 className="text-base font-semibold text-ink">{title}</h2>
      ) : null}
      {description ? (
        <p className="mt-1 text-sm text-muted">{description}</p>
      ) : null}
      {children ? <div className="mt-4">{children}</div> : null}
      {footer ? <div className="mt-4 border-t border-line pt-4">{footer}</div> : null}
    </section>
  );
}
