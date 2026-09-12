/** Typed fetch wrapper around the PRD §12 envelope. */

import { z } from "zod";

export class ApiError extends Error {
  constructor(
    readonly code: string,
    message: string,
    readonly status: number,
    readonly requestId: string | null,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * Validated rather than cast: a proxy or gateway can return parseable JSON that
 * is not an envelope at all, and reading `error.code` off that throws instead of
 * producing the ApiError callers rely on.
 */
const envelopeSchema = z.discriminatedUnion("success", [
  z.object({
    success: z.literal(true),
    data: z.unknown(),
    meta: z.object({ request_id: z.string().optional() }).optional(),
  }),
  z.object({
    success: z.literal(false),
    error: z.object({
      code: z.string(),
      message: z.string(),
      request_id: z.string().optional(),
    }),
  }),
]);

function newRequestId(): string {
  const bytes = new Uint8Array(13);
  crypto.getRandomValues(bytes);
  const hex = Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
  return `req_${hex}`;
}

export async function apiFetch<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const requestId = newRequestId();
  const response = await fetch(`/api/v1${path}`, {
    ...init,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-Request-ID": requestId,
      ...(init.headers ?? {}),
    },
  });

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    payload = undefined;
  }

  const parsed = envelopeSchema.safeParse(payload);

  if (parsed.success) {
    const body = parsed.data;
    if (body.success) return body.data as T;
    throw new ApiError(
      body.error.code,
      body.error.message,
      response.status,
      body.error.request_id ?? requestId,
    );
  }

  // Not an envelope at all — a proxy error page, a gateway's own JSON, an empty
  // body. Still fails truthfully, carrying the status and a request ID.
  throw new ApiError(
    "INTERNAL_ERROR",
    "Something went wrong. Please try again.",
    response.status,
    response.headers.get("X-Request-ID") ?? requestId,
  );
}
