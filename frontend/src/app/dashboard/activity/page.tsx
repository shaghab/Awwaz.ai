"use client";

import { PlaceholderPage } from "@/components/layout/PlaceholderPage";

export default function ActivityPage() {
  return (
    <PlaceholderPage
      roles={["OPERATOR"]}
      title="Activity"
      description="What the agent examined, proposed, and executed."
      emptyTitle="No agent activity yet"
      emptyDescription="Every agent step is recorded so a human can check what it looked at before it proposed anything."
      arrivesIn="slice 3"
    />
  );
}
