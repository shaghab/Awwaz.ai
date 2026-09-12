import { afterEach, describe, expect, it, vi } from "vitest";

import { ApiError, apiFetch } from "../client";
import { errorKind, errorMessage } from "@/lib/errors";

function mockResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

afterEach(() => vi.restoreAllMocks());

describe("apiFetch", () => {
  it("unwraps the success envelope", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () =>
        mockResponse({ success: true, data: { id: "1" }, meta: { request_id: "req_a" } }),
      ),
    );
    await expect(apiFetch("/thing")).resolves.toEqual({ id: "1" });
  });

  it("sends credentials and a client request id", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(mockResponse({ success: true, data: null }));
    await apiFetch("/thing");

    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe("/api/v1/thing");
    expect(init?.credentials).toBe("include");
    expect(
      (init?.headers as Record<string, string>)["X-Request-ID"],
    ).toMatch(/^req_[0-9a-f]{26}$/);
  });

  it("throws ApiError carrying the code and request id", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () =>
        mockResponse(
          {
            success: false,
            error: { code: "FORBIDDEN", message: "Nope.", request_id: "req_b" },
          },
          403,
        ),
      ),
    );

    const error = await apiFetch("/thing").catch((e: unknown) => e);
    expect(error).toBeInstanceOf(ApiError);
    expect(error).toMatchObject({
      code: "FORBIDDEN",
      status: 403,
      requestId: "req_b",
      message: "Nope.",
    });
  });

  it("fails truthfully when the response is not an envelope", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => new Response("<html>502</html>", { status: 502 })),
    );
    const error = (await apiFetch("/thing").catch((e: unknown) => e)) as ApiError;
    expect(error.code).toBe("INTERNAL_ERROR");
    expect(error.status).toBe(502);
  });
});

describe("error mapping (PRD §19)", () => {
  it.each([
    [401, "unauthenticated"],
    [403, "forbidden"],
    [404, "not-found"],
    [409, "conflict"],
    [429, "rate-limited"],
    [503, "unavailable"],
    [500, "generic"],
  ])("maps %i to %s", (status, kind) => {
    expect(errorKind(new ApiError("X", "m", status, null))).toBe(kind);
  });

  it("falls back to a generic message for non-API errors", () => {
    expect(errorMessage(new Error("boom"))).toBe(
      "Something went wrong. Please try again.",
    );
  });
});
