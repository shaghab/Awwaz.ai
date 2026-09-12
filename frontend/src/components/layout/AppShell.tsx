"use client";

import type { ReactNode } from "react";

import { Sidebar } from "@/components/layout/Sidebar";
import { TopBar } from "@/components/layout/TopBar";
import { ErrorState } from "@/components/ui/ErrorState";
import { PermissionState } from "@/components/ui/PermissionState";
import { Skeleton } from "@/components/ui/Skeleton";
import { useActor } from "@/lib/auth/useActor";
import type { Role } from "@/services/api/auth";

/**
 * Shell for authenticated areas. `roles` is a UI convenience; the backend
 * refuses the data regardless of what the shell renders.
 */
export function AppShell({
  roles,
  children,
}: {
  roles: Role[];
  children: ReactNode;
}) {
  const { data: actor, isPending, error } = useActor();

  let body: ReactNode;
  if (isPending) body = <Skeleton lines={5} label="Loading your workspace" />;
  else if (error) body = <ErrorState error={error} />;
  else if (!actor) body = <PermissionState reason="signed-out" />;
  else if (!roles.includes(actor.role)) body = <PermissionState reason="wrong-role" />;
  else body = children;

  return (
    <div className="flex min-h-screen flex-col bg-canvas">
      <TopBar actor={actor ?? null} />
      <div className="flex flex-1">
        {actor && roles.includes(actor.role) ? <Sidebar role={actor.role} /> : null}
        <main className="flex-1 space-y-6 p-6">{body}</main>
      </div>
    </div>
  );
}
