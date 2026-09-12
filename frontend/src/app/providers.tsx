"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { type ReactNode, useState } from "react";

import { ApiError } from "@/services/api/client";

export function Providers({ children }: { children: ReactNode }) {
  const [client] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            // The server owns truth (A14): refetch rather than trust a cache.
            refetchOnWindowFocus: true,
            staleTime: 15_000,
            retry: (failureCount, error) => {
              if (error instanceof ApiError && error.status < 500) return false;
              return failureCount < 2;
            },
          },
        },
      }),
  );

  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
}
