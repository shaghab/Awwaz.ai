"use client";

import { PlaceholderPage } from "@/components/layout/PlaceholderPage";

export default function OperatorCasesPage() {
  return (
    <PlaceholderPage
      roles={["OPERATOR"]}
      title="Cases"
      description="The full queue, filterable by status, department, and priority."
      emptyTitle="No cases yet"
      emptyDescription="Cases created through the citizen conversation or the API will be listed here."
      arrivesIn="slice 2"
    />
  );
}
