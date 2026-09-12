"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";

import { ApiError } from "@/services/api/client";
import { type Actor, demoLogin, fetchMe, logout } from "@/services/api/auth";

export const ACTOR_QUERY_KEY = ["auth", "me"] as const;

export function useActor() {
  return useQuery<Actor | null>({
    queryKey: ACTOR_QUERY_KEY,
    queryFn: async () => {
      try {
        return await fetchMe();
      } catch (error) {
        // Signed out is a state, not a failure.
        if (error instanceof ApiError && error.status === 401) return null;
        throw error;
      }
    },
    retry: false,
    staleTime: 30_000,
  });
}

export function useDemoLogin() {
  const queryClient = useQueryClient();
  const router = useRouter();
  return useMutation({
    mutationFn: demoLogin,
    onSuccess: (actor) => {
      queryClient.setQueryData(ACTOR_QUERY_KEY, actor);
      router.push(landingPathFor(actor.role));
    },
  });
}

export function useLogout() {
  const queryClient = useQueryClient();
  const router = useRouter();
  return useMutation({
    mutationFn: logout,
    onSettled: () => {
      queryClient.setQueryData(ACTOR_QUERY_KEY, null);
      queryClient.clear();
      router.push("/login");
    },
  });
}

export function landingPathFor(role: Actor["role"]): string {
  switch (role) {
    case "OPERATOR":
      return "/dashboard";
    case "ADMIN":
      return "/admin";
    default:
      return "/citizen";
  }
}
