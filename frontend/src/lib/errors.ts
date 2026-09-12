import { ApiError } from "@/services/api/client";

/** PRD §19 frontend mapping: HTTP status -> what the user is told and can do. */
export type ErrorKind =
  | "validation"
  | "unauthenticated"
  | "forbidden"
  | "not-found"
  | "conflict"
  | "rate-limited"
  | "unavailable"
  | "generic";

const BY_STATUS: Record<number, ErrorKind> = {
  400: "validation",
  401: "unauthenticated",
  403: "forbidden",
  404: "not-found",
  409: "conflict",
  429: "rate-limited",
  502: "unavailable",
  503: "unavailable",
};

const MESSAGES: Record<ErrorKind, string> = {
  validation: "Please check the details and try again.",
  unauthenticated: "Your session ended. Sign in to continue.",
  forbidden: "You do not have permission to view this.",
  "not-found": "We could not find that.",
  conflict: "This changed elsewhere. Refresh to see the latest state.",
  "rate-limited": "Too many requests. Please wait a moment.",
  unavailable: "The service is unavailable right now. Nothing was changed.",
  generic: "Something went wrong. Please try again.",
};

export function errorKind(error: unknown): ErrorKind {
  if (error instanceof ApiError) return BY_STATUS[error.status] ?? "generic";
  return "generic";
}

/** Server-authored messages are preferred; the map is the fallback. */
export function errorMessage(error: unknown): string {
  if (error instanceof ApiError && error.message) return error.message;
  return MESSAGES[errorKind(error)];
}
