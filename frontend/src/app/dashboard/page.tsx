"use client";

import { PlaceholderPage } from "@/components/layout/PlaceholderPage";

export default function OperatorOverviewPage() {
  return (
    <PlaceholderPage
      roles={["OPERATOR"]}
      title="Overview"
      description="Open, stalled, pending approval, high priority, and recurring at a glance."
      emptyTitle="No cases yet"
      emptyDescription="Once complaints exist, this view leads with what needs a decision: approvals first, then stalled and high-priority work."
      arrivesIn="slice 2"
    />
  );
}
