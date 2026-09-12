import Link from "next/link";

import { TopBar } from "@/components/layout/TopBar";

export default function CitizenLanding() {
  return (
    <div className="flex min-h-screen flex-col bg-canvas">
      <TopBar actor={null} />
      <main className="mx-auto flex w-full max-w-3xl flex-1 flex-col justify-center px-6 py-20">
        <h1 className="text-4xl font-semibold tracking-tight text-ink">
          Tell Awwaz what happened.
        </h1>
        <p className="mt-4 max-w-xl text-lg text-muted">
          Awwaz helps turn your report into a case and keeps track of what
          happens next.
        </p>
        <div className="mt-8 flex gap-3">
          <Link
            href="/citizen"
            className="inline-flex items-center rounded-md bg-brand px-5 py-2.5 text-sm font-medium text-white hover:bg-teal-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand"
          >
            Report a Problem
          </Link>
          <Link
            href="/login"
            className="inline-flex items-center rounded-md bg-white px-5 py-2.5 text-sm font-medium text-ink ring-1 ring-line hover:bg-slate-50"
          >
            Sign in
          </Link>
        </div>
      </main>
    </div>
  );
}
