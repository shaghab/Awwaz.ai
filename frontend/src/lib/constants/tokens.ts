/**
 * Design tokens (PRD §10: trustworthy, calm, modern, serious, operational).
 * Tailwind's theme extends from these so later slices stay consistent.
 */
export const colors = {
  ink: "#0f172a",
  muted: "#64748b",
  line: "#e2e8f0",
  surface: "#ffffff",
  canvas: "#f8fafc",
  brand: "#0f766e",
  brandSoft: "#ccfbf1",
  info: "#1d4ed8",
  warn: "#b45309",
  danger: "#b91c1c",
  ok: "#15803d",
} as const;

export const radii = { sm: "4px", md: "8px", lg: "12px" } as const;

/**
 * Status is never conveyed by colour alone (PRD §10 accessibility rule): every
 * tone here is rendered with its label text by `Badge`.
 */
export type Tone = "neutral" | "info" | "ok" | "warn" | "danger" | "brand";

export const toneClasses: Record<Tone, string> = {
  neutral: "bg-slate-100 text-slate-700 ring-slate-200",
  info: "bg-blue-50 text-blue-800 ring-blue-200",
  ok: "bg-green-50 text-green-800 ring-green-200",
  warn: "bg-amber-50 text-amber-900 ring-amber-200",
  danger: "bg-red-50 text-red-800 ring-red-200",
  brand: "bg-teal-50 text-teal-800 ring-teal-200",
};
