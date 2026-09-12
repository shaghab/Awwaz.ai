import type { NextConfig } from "next";

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
