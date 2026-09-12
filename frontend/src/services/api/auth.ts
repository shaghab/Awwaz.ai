import { z } from "zod";

import { apiFetch } from "./client";

export const actorSchema = z.object({
  id: z.string(),
  role: z.enum(["CITIZEN", "OPERATOR", "ADMIN", "SERVICE"]),
  name: z.string(),
});

export type Actor = z.infer<typeof actorSchema>;
export type Role = Actor["role"];

const demoUserSchema = z.object({
  user_key: z.string(),
  name: z.string(),
  role: actorSchema.shape.role,
});

export type DemoUser = z.infer<typeof demoUserSchema>;

export async function fetchMe(): Promise<Actor> {
  const data = await apiFetch<unknown>("/auth/me");
  return actorSchema.parse(z.object({ actor: actorSchema }).parse(data).actor);
}

export async function fetchDemoUsers(): Promise<DemoUser[]> {
  const data = await apiFetch<unknown>("/auth/demo-users");
  return z.object({ users: z.array(demoUserSchema) }).parse(data).users;
}

export async function demoLogin(userKey: string): Promise<Actor> {
  const data = await apiFetch<unknown>("/auth/demo-login", {
    method: "POST",
    body: JSON.stringify({ user_key: userKey }),
  });
  return z.object({ actor: actorSchema }).parse(data).actor;
}

export async function logout(): Promise<void> {
  await apiFetch<unknown>("/auth/logout", { method: "POST" });
}
