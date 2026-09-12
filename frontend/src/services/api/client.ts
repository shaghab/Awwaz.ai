/** Typed fetch wrapper around the PRD §12 envelope. */

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

type Envelope<T> =
  | { success: true; data: T; meta?: { request_id?: string } }
  | {
      success: false;
      error: { code: string; message: string; request_id?: string };
    };

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

  let body: Envelope<T> | null = null;
  try {
    body = (await response.json()) as Envelope<T>;
  } catch {
    body = null;
  }

  if (body && body.success) return body.data;

  if (body && !body.success) {
    throw new ApiError(
      body.error.code,
      body.error.message,
      response.status,
      body.error.request_id ?? requestId,
    );
  }

  // A non-enveloped response (proxy error, network edge) still fails truthfully.
  throw new ApiError(
    "INTERNAL_ERROR",
    "Something went wrong. Please try again.",
    response.status,
    response.headers.get("X-Request-ID"),
  );
}
