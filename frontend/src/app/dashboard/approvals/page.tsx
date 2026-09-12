"use client";

import { PlaceholderPage } from "@/components/layout/PlaceholderPage";

export default function ApprovalsPage() {
  return (
    <PlaceholderPage
      roles={["OPERATOR"]}
      title="Approvals"
      description="Agent recommendations waiting on a human decision."
      emptyTitle="Nothing is waiting for approval"
      emptyDescription="Awwaz never acts externally on its own. Recommended escalations and follow-ups will queue here for approval."
      arrivesIn="slice 4"
    />
  );
}
