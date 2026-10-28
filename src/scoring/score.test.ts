import { describe, expect, it } from "vitest";
import type { City, Knowledge } from "../model/types.ts";
import { explain, rank, stability, type Preference } from "./score.ts";

const city = (id: string, temp: number, walk: number | null): City => ({
  id,
  nameJa: id,
  nameEn: id,
  country: "XX",
  lat: 0,
  lon: 0,
  metrics: {
    temp: { value: temp, quality: "observed", sourceId: "s", year: 2024 },
    walk:
      walk === null
        ? { value: null, quality: "missing", sourceId: "s", year: null }
        : { value: walk, quality: "placeholder", sourceId: "s", year: null },
  },
});

const k: Knowledge = {
  modelVersion: "test",
  minCoverage: 0.75,
  dataVersion: "test",
  sources: [],
  questions: [],
  metrics: [
    { key: "temp", label: "temp", unit: "℃", kind: "ideal", transform: "linear", tolerance: 3, sourceId: "s" },
    {
      key: "walk",
      label: "walk",
      unit: "%",
      kind: "higher_better",
      transform: "linear",
      tolerance: null,
      sourceId: "s",
    },
  ],
  cities: [city("a", 25, 90), city("b", 20, 40), city("c", 25, null), city("d", 30, 60)],
};

const prefs: Preference[] = [
  { metric: "temp", weight: 1, ideal: 25 },
  { metric: "walk", weight: 1 },
];

describe("rank", () => {
  it("is deterministic", () => {
    expect(rank(k, prefs)).toEqual(rank(k, prefs));
  });

  it("puts the city closest to the ideal on top", () => {
    expect(rank(k, prefs).ranked[0].cityId).toBe("a");
  });

  it("does not treat missing as zero: excludes the city when coverage is too low", () => {
    const { ranked, insufficient } = rank(k, prefs);
    expect(ranked.map((r) => r.cityId)).not.toContain("c");
    expect(insufficient[0]).toMatchObject({ cityId: "c", coverage: 0.5 });
  });

  it("re-normalizes weights when the missing axis has zero weight", () => {
    const r = rank(k, [prefs[0], { metric: "walk", weight: 0 }]);
    expect(r.ranked.find((x) => x.cityId === "c")?.total).toBeCloseTo(100);
  });

  it("labels quality by the worst axis used", () => {
    expect(rank(k, prefs).ranked[0].quality).toBe("placeholder");
    expect(rank(k, [prefs[0]]).ranked[0].quality).toBe("observed");
  });
});

describe("explain / stability", () => {
  it("separates matches and mismatches", () => {
    const b = rank(k, prefs).ranked.find((r) => r.cityId === "b")!;
    const { matches, mismatches } = explain(b);
    expect(matches).toEqual([]);
    expect(mismatches.map((a) => a.metric).toSorted()).toEqual(["temp", "walk"]);
  });

  it("is 1 when #1 is robust", () => {
    expect(stability(k, prefs)).toBe(1);
  });
});
