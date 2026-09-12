"use client";

import { AppShell } from "@/components/layout/AppShell";
import { EmptyState } from "@/components/ui/EmptyState";
import { PageHeader } from "@/components/ui/PageHeader";
import type { Role } from "@/services/api/auth";

/**
 * Slice 1 ships the shell only. Loading, error, and permission states come from
 * `AppShell`; this is the empty state the page shows once there is no data yet.
 */
export function PlaceholderPage({
  roles,
  title,
  description,
  emptyTitle,
  emptyDescription,
  arrivesIn,
}: {
  roles: Role[];
  title: string;
  description: string;
  emptyTitle: string;
  emptyDescription: string;
  arrivesIn: string;
}) {
  return (
    <AppShell roles={roles}>
      <PageHeader title={title} description={description} />
      <EmptyState
        title={emptyTitle}
        description={emptyDescription}
        action={<p className="text-xs text-muted">Arrives in {arrivesIn}.</p>}
      />
    </AppShell>
  );
}
