"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { NAV_BY_ROLE } from "@/lib/auth/navigation";
import type { Role } from "@/services/api/auth";

export function Sidebar({ role }: { role: Role }) {
  const pathname = usePathname();
  const items = NAV_BY_ROLE[role];

  if (items.length === 0) return null;

  return (
    <nav aria-label="Primary" className="w-56 shrink-0 border-r border-line bg-white">
      <ul className="space-y-1 p-3">
        {items.map((item) => {
          const active =
            pathname === item.href || pathname.startsWith(`${item.href}/`);
          return (
            <li key={item.href}>
              <Link
                href={item.href}
                aria-current={active ? "page" : undefined}
                className={`block rounded-md px-3 py-2 text-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand ${
                  active
                    ? "bg-brand-soft font-medium text-teal-900"
                    : "text-ink hover:bg-slate-100"
                }`}
              >
                {item.label}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
