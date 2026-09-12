"use client";

import { PlaceholderPage } from "@/components/layout/PlaceholderPage";

export default function CitizenReportPage() {
  return (
    <PlaceholderPage
      roles={["CITIZEN"]}
      title="Report"
      description="Describe the problem in your own words — English, Urdu, or Roman Urdu."
      emptyTitle="The reporting conversation is not available yet"
      emptyDescription="Awwaz will read your message, ask for anything missing, and create a case only when it has enough detail."
      arrivesIn="slice 3"
    />
  );
}
