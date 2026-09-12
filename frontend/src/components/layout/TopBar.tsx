"use client";

import Link from "next/link";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { useLogout } from "@/lib/auth/useActor";
import type { Actor } from "@/services/api/auth";

export function TopBar({ actor }: { actor: Actor | null }) {
  const logout = useLogout();

  return (
    <header className="flex items-center justify-between border-b border-line bg-white px-6 py-3">
      <Link href="/" className="text-sm font-semibold tracking-tight text-ink">
        Awwaz
      </Link>
      <div className="flex items-center gap-3">
        {actor ? (
          <>
            <span className="text-sm text-ink">{actor.name}</span>
            <Badge tone="brand">{actor.role}</Badge>
            <Button
              variant="secondary"
              onClick={() => logout.mutate()}
              disabled={logout.isPending}
            >
              {logout.isPending ? "Signing out…" : "Sign out"}
            </Button>
          </>
        ) : (
          <Link
            href="/login"
            className="text-sm font-medium text-brand hover:underline"
          >
            Sign in
          </Link>
        )}
      </div>
    </header>
  );
}
