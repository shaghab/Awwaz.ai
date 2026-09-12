"use client";

import { PlaceholderPage } from "@/components/layout/PlaceholderPage";

export default function CitizenComplaintDetailPage() {
  return (
    <PlaceholderPage
      roles={["CITIZEN"]}
      title="Case"
      description="Status, timeline, and what Awwaz is doing next."
      emptyTitle="Case details are not available yet"
      emptyDescription="This page will show the case status, its timeline, and the evidence attached to it."
      arrivesIn="slice 2"
    />
  );
}
