import Link from "next/link";

export default function NotFound() {
  return (
    <main className="mx-auto flex min-h-screen max-w-lg flex-col justify-center px-6 text-center">
      <h1 className="text-2xl font-semibold text-ink">Page not found</h1>
      <p className="mt-2 text-sm text-muted">
        The page you are looking for does not exist.
      </p>
      <Link href="/" className="mt-4 text-sm font-medium text-brand hover:underline">
        Back to Awwaz
      </Link>
    </main>
  );
}
