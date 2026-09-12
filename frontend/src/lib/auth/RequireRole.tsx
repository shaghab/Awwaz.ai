"use client";

import type { ReactNode } from "react";

import { useActor } from "@/lib/auth/useActor";
import type { Role } from "@/services/api/auth";
import { ErrorState } from "@/components/ui/ErrorState";
import { PermissionState } from "@/components/ui/PermissionState";
import { Skeleton } from "@/components/ui/Skeleton";

/**
 * Convenience only: the backend enforces authorisation independently
 * (PRD F-common "Permissions"). This just avoids showing a doomed page.
 */
export function RequireRole({
  roles,
  children,
}: {
  roles: Role[];
  children: ReactNode;
}) {
  const { data: actor, isPending, error } = useActor();

  if (isPending) return <Skeleton lines={4} label="Checking your access" />;
  if (error) return <ErrorState error={error} />;
  if (!actor) return <PermissionState reason="signed-out" />;
  if (!roles.includes(actor.role)) return <PermissionState reason="wrong-role" />;

  return <>{children}</>;
}
