"use client";

import { PlaceholderPage } from "@/components/layout/PlaceholderPage";

export default function OperatorCaseDetailPage() {
  return (
    <PlaceholderPage
      roles={["OPERATOR"]}
      title="Case detail"
      description="Summary, timeline, agent trace, recommendations, evidence, and related cases."
      emptyTitle="Case details are not available yet"
      emptyDescription="This page will carry the canonical case state and every action taken on it."
      arrivesIn="slice 2"
    />
  );
}
