import type { Role } from "@/services/api/auth";

export type NavItem = { label: string; href: string };

/** Exactly the primary navigation in PRD §10. */
export const NAV_BY_ROLE: Record<Role, NavItem[]> = {
  CITIZEN: [
    { label: "Report", href: "/citizen" },
    { label: "My Complaints", href: "/citizen/complaints" },
  ],
  OPERATOR: [
    { label: "Overview", href: "/dashboard" },
    { label: "Cases", href: "/dashboard/complaints" },
    { label: "Approvals", href: "/dashboard/approvals" },
    { label: "Recurring Issues", href: "/dashboard/recurring" },
    { label: "Activity", href: "/dashboard/activity" },
  ],
  ADMIN: [
    { label: "Configuration", href: "/admin" },
    { label: "Users", href: "/admin/users" },
    { label: "Audit", href: "/admin/audit" },
  ],
  SERVICE: [],
};
