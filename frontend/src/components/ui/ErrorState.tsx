import { errorMessage } from "@/lib/errors";
import { ApiError } from "@/services/api/client";

export function ErrorState({
  error,
  onRetry,
}: {
  error: unknown;
  onRetry?: () => void;
}) {
  const requestId = error instanceof ApiError ? error.requestId : null;
  return (
    <div
      role="alert"
      className="rounded-lg border border-red-200 bg-red-50 p-6 text-sm text-red-900"
    >
      <p className="font-semibold">Something went wrong</p>
      <p className="mt-1">{errorMessage(error)}</p>
      {requestId ? (
        <p className="mt-2 font-mono text-xs text-red-700">Reference: {requestId}</p>
      ) : null}
      {onRetry ? (
        <button
          onClick={onRetry}
          className="mt-3 rounded-md bg-white px-3 py-1.5 text-xs font-medium text-red-900 ring-1 ring-red-200 hover:bg-red-100"
        >
          Try again
        </button>
      ) : null}
    </div>
  );
}
