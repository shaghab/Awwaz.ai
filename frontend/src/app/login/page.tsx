"use client";

import { useQuery } from "@tanstack/react-query";

import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { ErrorState } from "@/components/ui/ErrorState";
import { PageHeader } from "@/components/ui/PageHeader";
import { Skeleton } from "@/components/ui/Skeleton";
import { TopBar } from "@/components/layout/TopBar";
import { useDemoLogin } from "@/lib/auth/useActor";
import { fetchDemoUsers } from "@/services/api/auth";

export default function LoginPage() {
  const personas = useQuery({
    queryKey: ["auth", "demo-users"],
    queryFn: fetchDemoUsers,
    retry: false,
  });
  const login = useDemoLogin();

  return (
    <div className="flex min-h-screen flex-col bg-canvas">
      <TopBar actor={null} />
      <main className="mx-auto w-full max-w-3xl space-y-6 p-6">
        <PageHeader
          title="Choose a demo persona"
          description="Demo sessions have no passwords. Each persona sees a different part of Awwaz."
        />

        {personas.isPending ? <Skeleton lines={3} label="Loading personas" /> : null}
        {personas.error ? (
          <ErrorState error={personas.error} onRetry={() => personas.refetch()} />
        ) : null}
        {login.error ? <ErrorState error={login.error} /> : null}

        <div className="grid gap-4 sm:grid-cols-3">
          {(personas.data ?? []).map((persona) => (
            <Card key={persona.user_key} title={persona.name}>
              <div className="space-y-4">
                <Badge tone="brand">{persona.role}</Badge>
                <button
                  onClick={() => login.mutate(persona.user_key)}
                  disabled={login.isPending}
                  className="w-full rounded-md bg-brand px-4 py-2 text-sm font-medium text-white hover:bg-teal-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand disabled:opacity-60"
                >
                  {login.isPending && login.variables === persona.user_key
                    ? "Signing in…"
                    : `Continue as ${persona.name.split(" ")[0]}`}
                </button>
              </div>
            </Card>
          ))}
        </div>
      </main>
    </div>
  );
}
