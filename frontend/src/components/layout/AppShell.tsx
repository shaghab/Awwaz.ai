"use client";

import { useRouter } from "next/navigation";
import { type ReactNode, useEffect } from "react";

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
  const router = useRouter();
  const { data: actor, isPending, error } = useActor();

  // A missing, expired, or revoked session sends the viewer to sign in (§19:
  // 401 -> authenticate). Wrong role is different: they are signed in, so they
  // get the permission state rather than a pointless trip to /login.
  const signedOut = !isPending && !error && !actor;
  useEffect(() => {
    if (signedOut) router.replace("/login");
  }, [signedOut, router]);

  let body: ReactNode;
  if (isPending) body = <Skeleton lines={5} label="Loading your workspace" />;
  else if (error) body = <ErrorState error={error} />;
  else if (signedOut) body = <Skeleton lines={3} label="Redirecting to sign in" />;
  else if (actor && !roles.includes(actor.role)) {
    body = <PermissionState reason="wrong-role" />;
  } else body = children;

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
