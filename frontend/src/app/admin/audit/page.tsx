"use client";

import { PlaceholderPage } from "@/components/layout/PlaceholderPage";

export default function AdminAuditPage() {
  return (
    <PlaceholderPage
      roles={["ADMIN"]}
      title="Audit"
      description="Every consequential action, who took it, and whether it succeeded."
      emptyTitle="The audit view is not available yet"
      emptyDescription="Audit records are already being written — sign-in and sign-out are recorded from this slice onward."
      arrivesIn="slice 6"
    />
  );
}
