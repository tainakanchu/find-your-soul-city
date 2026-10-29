import { describe, expect, it } from "vitest";
import raw from "../generated/knowledge.json";
import type { Knowledge } from "./types.ts";
import { findPlaceholders } from "./guard.ts";

const clean = {
  sources: [{ id: "era5" }],
  cities: [
    {
      id: "a",
      metrics: {
        x: { value: 1, quality: "observed", sourceId: "era5" },
        y: { value: null, quality: "missing", sourceId: "era5" },
      },
    },
  ],
};

const withMetric = (m: object) => ({ ...clean, cities: [{ id: "a", metrics: { x: m } }] });

describe("findPlaceholders", () => {
  it("returns [] for clean data", () => {
    expect(findPlaceholders(clean)).toEqual([]);
  });

  it("flags quality placeholder", () => {
    const out = findPlaceholders(withMetric({ value: 1, quality: "placeholder", sourceId: "era5" }));
    expect(out).toHaveLength(1);
    expect(out[0]).toContain("a.x");
  });

  it("flags a source id containing placeholder or demo", () => {
    expect(findPlaceholders(withMetric({ value: null, quality: "missing", sourceId: "placeholder-1" }))).toHaveLength(
      1,
    );
    expect(findPlaceholders(withMetric({ value: null, quality: "missing", sourceId: "Demo-set" }))).toHaveLength(1);
  });

  it("flags an unregistered source for a non-null value only", () => {
    expect(findPlaceholders(withMetric({ value: 3, quality: "observed", sourceId: "nope" }))).toHaveLength(1);
    expect(findPlaceholders(withMetric({ value: null, quality: "missing", sourceId: "nope" }))).toEqual([]);
  });
});

describe("generated knowledge.json", () => {
  const k = raw as Knowledge;

  it("has no placeholders", () => {
    expect(findPlaceholders(k)).toEqual([]);
  });

  it("explains every missing value with a reason", () => {
    const bad = k.cities.flatMap((c) =>
      Object.entries(c.metrics)
        .filter(([, v]) => v.value === null && !v.reason)
        .map(([key]) => `${c.id}.${key}`),
    );
    expect(bad).toEqual([]);
  });
});
