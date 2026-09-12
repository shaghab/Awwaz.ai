import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import type { NextConfig } from "next";

/**
 * The documented quick start puts `.env` at the repository root, but Next only
 * loads env files from its own directory, so `BACKEND_BASE_URL` set there was
 * silently ignored and the proxy always fell back to localhost:8000. The backend
 * anchors to the same root file; this is the frontend half.
 *
 * A real environment variable always wins over the file, so deployments and CI
 * are unaffected.
 */
const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");

if (!process.env.BACKEND_BASE_URL) {
  try {
    process.loadEnvFile(resolve(repoRoot, ".env"));
  } catch {
    // No root .env — defaults below apply.
  }
}

const backendBaseUrl = process.env.BACKEND_BASE_URL ?? "http://localhost:8000";

/**
 * The session cookie stays same-origin in development by proxying /api/* to the
 * backend (D4). A split deployment relies on the backend's CORS config instead.
 */
const nextConfig: NextConfig = {
  async rewrites() {
    return [
      { source: "/api/:path*", destination: `${backendBaseUrl}/api/:path*` },
      { source: "/ready", destination: `${backendBaseUrl}/ready` },
    ];
  },
};

export default nextConfig;
