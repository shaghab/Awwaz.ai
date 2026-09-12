"use client";

import { PlaceholderPage } from "@/components/layout/PlaceholderPage";

export default function RecurringPage() {
  return (
    <PlaceholderPage
      roles={["OPERATOR"]}
      title="Recurring Issues"
      description="Locations and categories that keep coming back."
      emptyTitle="No recurring issues detected"
      emptyDescription="When the same problem is reported repeatedly at one location, it will surface here with its prior cases."
      arrivesIn="slice 5"
    />
  );
}
