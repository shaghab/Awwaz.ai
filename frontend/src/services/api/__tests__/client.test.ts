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
    expect(new Headers(init?.headers).get("X-Request-ID")).toMatch(
      /^req_[0-9a-f]{26}$/,
    );
  });

  it.each([
    ["a plain object", { "Idempotency-Key": "k1" } as HeadersInit],
    ["a Headers instance", new Headers({ "Idempotency-Key": "k1" })],
    ["an array of tuples", [["Idempotency-Key", "k1"]] as HeadersInit],
  ])("preserves caller headers given as %s", async (_label, callerHeaders) => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(mockResponse({ success: true, data: null }));
    await apiFetch("/thing", { headers: callerHeaders });

    const sent = new Headers(fetchMock.mock.calls[0][1]?.headers);
    expect(sent.get("Idempotency-Key")).toBe("k1");
    expect(sent.get("X-Request-ID")).toMatch(/^req_/);
  });

  it("lets a caller override the request id, and reports that one", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () =>
        mockResponse(
          { success: false, error: { code: "NOT_FOUND", message: "no" } },
          404,
        ),
      ),
    );
    const error = (await apiFetch("/thing", {
      headers: { "X-Request-ID": "req_caller_chose" },
    }).catch((e: unknown) => e)) as ApiError;
    expect(error.requestId).toBe("req_caller_chose");
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

  it("fails truthfully when the response is not JSON", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => new Response("<html>502</html>", { status: 502 })),
    );
    const error = (await apiFetch("/thing").catch((e: unknown) => e)) as ApiError;
    expect(error.code).toBe("INTERNAL_ERROR");
    expect(error.status).toBe(502);
  });

  it.each([
    ["a gateway's own JSON", { detail: "Bad Gateway" }],
    ["a failure envelope with no error object", { success: false }],
    ["an error object missing its code", { success: false, error: { message: "x" } }],
    ["a JSON literal", "nope"],
    ["null", null],
  ])("throws ApiError, not TypeError, for %s", async (_label, payload) => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () =>
        mockResponse(payload, 502),
      ),
    );
    const error = await apiFetch("/thing").catch((e: unknown) => e);
    expect(error).toBeInstanceOf(ApiError);
    expect((error as ApiError).code).toBe("INTERNAL_ERROR");
    expect((error as ApiError).status).toBe(502);
    // The status and a correlatable id survive, which is the whole point.
    expect((error as ApiError).requestId).toMatch(/^req_/);
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

describe("content type", () => {
  async function sentHeaders(init: RequestInit) {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(mockResponse({ success: true, data: null }));
    await apiFetch("/thing", init);
    return new Headers(fetchMock.mock.calls[0][1]?.headers);
  }

  it("labels a JSON string body", async () => {
    const sent = await sentHeaders({ method: "POST", body: JSON.stringify({ a: 1 }) });
    expect(sent.get("Content-Type")).toBe("application/json");
  });

  it("leaves FormData for the browser to type", async () => {
    // Setting it ourselves would strip the multipart boundary and make the
    // upload unparseable — this is the documented evidence flow.
    const form = new FormData();
    form.append("file", new Blob(["x"]), "photo.jpg");
    const sent = await sentHeaders({ method: "POST", body: form });
    expect(sent.get("Content-Type")).toBeNull();
  });

  it("leaves URLSearchParams for the browser to type", async () => {
    const sent = await sentHeaders({
      method: "POST",
      body: new URLSearchParams({ a: "1" }),
    });
    expect(sent.get("Content-Type")).toBeNull();
  });

  it("never overrides a caller's own content type", async () => {
    const sent = await sentHeaders({
      method: "POST",
      body: "<xml/>",
      headers: { "Content-Type": "application/xml" },
    });
    expect(sent.get("Content-Type")).toBe("application/xml");
  });
});
