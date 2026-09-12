import Link from "next/link";

export function PermissionState({
  reason = "wrong-role",
}: {
  reason?: "wrong-role" | "signed-out";
}) {
  const signedOut = reason === "signed-out";
  return (
    <div
      role="status"
      className="rounded-lg border border-amber-200 bg-amber-50 p-6 text-sm text-amber-900"
    >
      <p className="font-semibold">
        {signedOut ? "Sign in to continue" : "You do not have access to this area"}
      </p>
      <p className="mt-1">
        {signedOut
          ? "Your session ended or you have not signed in yet."
          : "This area is limited to a different role. Switching personas changes what you can see."}
      </p>
      <Link
        href="/login"
        className="mt-3 inline-block rounded-md bg-white px-3 py-1.5 text-xs font-medium text-amber-900 ring-1 ring-amber-200 hover:bg-amber-100"
      >
        Go to sign in
      </Link>
    </div>
  );
}
