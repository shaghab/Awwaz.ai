"use client";

import { PlaceholderPage } from "@/components/layout/PlaceholderPage";

export default function AdminUsersPage() {
  return (
    <PlaceholderPage
      roles={["ADMIN"]}
      title="Users"
      description="Operators, administrators, and service accounts."
      emptyTitle="User management is not available yet"
      emptyDescription="Demo personas are seeded by `make seed`. Managing real users is out of scope for the MVP."
      arrivesIn="slice 6"
    />
  );
}
