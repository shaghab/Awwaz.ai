"use client";

import { PlaceholderPage } from "@/components/layout/PlaceholderPage";

export default function CitizenComplaintsPage() {
  return (
    <PlaceholderPage
      roles={["CITIZEN"]}
      title="My Complaints"
      description="Every case you have reported and what has happened since."
      emptyTitle="You have not reported anything yet"
      emptyDescription="Cases you report will appear here with their current status and the last action taken."
      arrivesIn="slice 2"
    />
  );
}
