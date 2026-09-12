"use client";

import { PlaceholderPage } from "@/components/layout/PlaceholderPage";

export default function AdminConfigurationPage() {
  return (
    <PlaceholderPage
      roles={["ADMIN"]}
      title="Configuration"
      description="Departments, routing rules, escalation chain, and stall thresholds."
      emptyTitle="Configuration is not editable yet"
      emptyDescription="Routing and thresholds live in the database, seeded from YAML, so they are never hard-coded in a prompt."
      arrivesIn="slice 6"
    />
  );
}
