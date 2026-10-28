import { describe, expect, it } from "vitest";
import type { City, Knowledge, Metric, Quality } from "../model/types.ts";
import { buildScales, cdf, explain, fit, rank, referenceScales, stability, type Preference, type Scales } from "./score.ts";

const mv = (value: number | null, quality: Quality = "observed") =>
  value === null
    ? { value, quality: "missing" as const, sourceId: "s", year: null, reason: "no data" }
    : { value, quality, sourceId: "s", year: 2024 };

const city = (
  id: string,
  temp: number,
  walk: number | null,
  extra: { pm?: number; pop?: number; walkQuality?: Quality } = {},
): City => ({
  id,
  nameJa: id,
  nameEn: id,
  country: "XX",
  region: "R",
  lat: 0,
  lon: 0,
  boundary: { sourceId: "s", id: 1, areaKm2: 1 },
  metrics: {
    temp: mv(temp),
    walk: mv(walk, extra.walkQuality),
    pm: mv(extra.pm ?? 10),
    pop: mv(extra.pop ?? 1000),
  },
});

const metric = (m: Partial<Metric> & Pick<Metric, "key" | "kind">): Metric => ({
  label: m.key,
  unit: "",
  transform: "linear",
  tolerance: null,
  sourceId: "s",
  period: "",
  geography: "",
  method: "",
  caveat: "",
  ...m,
});

const metrics: Metric[] = [
  metric({ key: "temp", kind: "ideal", tolerance: 3 }),
  metric({ key: "walk", kind: "higher_better" }),
  metric({ key: "pm", kind: "lower_better" }),
  metric({ key: "pop", kind: "ideal", transform: "log10", tolerance: 0.2 }),
];

const k: Knowledge = {
  modelVersion: "test",
  minCoverage: 0.75,
  dataVersion: "test",
  sources: [],
  questions: [],
  metrics,
  reference: {
    set: "test",
    levels: [0, 0.5, 1],
    metrics: { walk: { n: 3, quantiles: [0, 50, 100] }, pm: { n: 3, quantiles: [0, 20, 40] } },
  },
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

  it("minCoverage option overrides the threshold and re-normalizes over used axes", () => {
    const r = rank(k, prefs, { minCoverage: 0.5 });
    expect(r.insufficient).toEqual([]);
    expect(r.ranked.find((x) => x.cityId === "c")?.total).toBeCloseTo(100); // only temp used, fit 1
    expect(rank(k, prefs, { minCoverage: 0.9 }).insufficient.map((x) => x.cityId)).toEqual(["c"]);
  });

  it("labels quality by the worst axis used (estimated vs observed)", () => {
    const kq: Knowledge = {
      ...k,
      cities: [city("a", 25, 90, { walkQuality: "estimated" }), city("b", 25, 50)],
    };
    const r = rank(kq, prefs).ranked;
    expect(r.find((x) => x.cityId === "a")?.quality).toBe("estimated");
    expect(r.find((x) => x.cityId === "b")?.quality).toBe("observed");
    expect(rank(kq, [prefs[0]]).ranked.find((x) => x.cityId === "a")?.quality).toBe("observed");
  });

  it("uses lower_better so the cleanest city wins", () => {
    const kp: Knowledge = {
      ...k,
      cities: [city("a", 25, 50, { pm: 40 }), city("b", 25, 50, { pm: 5 }), city("c", 25, 50, { pm: 20 })],
    };
    const r = rank(kp, [{ metric: "pm", weight: 1 }]).ranked;
    expect(r.map((x) => x.cityId)).toEqual(["b", "c", "a"]);
    expect(r[0].total).toBeCloseTo(87.5); // pm 5 -> cdf 0.125 -> 1 - 0.125
    expect(r[1].total).toBeCloseTo(50);
    expect(r[2].total).toBeCloseTo(0);
  });

  it("accepts custom scales (RankOptions.scales)", () => {
    const wide: Scales = new Map([["walk", { type: "range", lo: 0, hi: 200 }]]);
    const only = [{ metric: "walk", weight: 1 }];
    const base = rank(k, only).ranked.find((x) => x.cityId === "d")!.total;
    const custom = rank(k, only, { scales: wide }).ranked.find((x) => x.cityId === "d")!.total;
    expect(custom).toBeCloseTo(30); // 60 / 200
    expect(custom).not.toBeCloseTo(base);
  });
});

describe("buildScales / fit", () => {
  it("only builds scales for directional metrics, from cities with a value", () => {
    const s = buildScales(k);
    expect([...s.keys()].toSorted()).toEqual(["pm", "walk"]);
    // walk values 40, 60, 90 -> q10 = 44, q90 = 84
    expect(s.get("walk")).toMatchObject({ type: "range" });
    const w = s.get("walk") as { lo: number; hi: number };
    expect(w.lo).toBeCloseTo(44);
    expect(w.hi).toBeCloseTo(84);
  });

  it("builds scales over log10-transformed values", () => {
    const kl: Knowledge = {
      ...k,
      metrics: [metric({ key: "pop", kind: "higher_better", transform: "log10" })],
      cities: [city("a", 0, 0, { pop: 10 }), city("b", 0, 0, { pop: 1000 })],
    };
    const s = buildScales(kl).get("pop") as { lo: number; hi: number };
    expect(s.lo).toBeCloseTo(1.2); // log10: 1 + 0.1*(3-1)
    expect(s.hi).toBeCloseTo(2.8);
  });

  it("fit: ideal metric is Gaussian in log10 space for log10 transform", () => {
    const m = metrics[3];
    expect(fit(m, 1000, 1000, new Map())).toBeCloseTo(1);
    // one tolerance away (x10^0.2) -> exp(-0.5)
    expect(fit(m, 1000 * 10 ** 0.2, 1000, new Map())).toBeCloseTo(Math.exp(-0.5));
    // symmetric in ratio, not in difference
    expect(fit(m, 500, 1000, new Map())).toBeCloseTo(fit(m, 2000, 1000, new Map()));
  });

  it("fit: directional metrics clamp to [0, 1] and lower_better is reversed", () => {
    const scales: Scales = new Map([
      ["walk", { type: "range", lo: 10, hi: 20 }],
      ["pm", { type: "range", lo: 10, hi: 20 }],
    ]);
    expect(fit(metrics[1], 5, undefined, scales)).toBe(0);
    expect(fit(metrics[1], 25, undefined, scales)).toBe(1);
    expect(fit(metrics[1], 15, undefined, scales)).toBeCloseTo(0.5);
    expect(fit(metrics[2], 5, undefined, scales)).toBe(1);
    expect(fit(metrics[2], 25, undefined, scales)).toBe(0);
  });

  it("fit: throws without an ideal or scale", () => {
    expect(() => fit(metrics[0], 20, undefined, new Map())).toThrow("ideal");
    expect(() => fit(metrics[1], 20, undefined, new Map())).toThrow("scale");
  });
});

describe("reference distribution (default scales)", () => {
  it("cdf is linear between quantiles, clamped, and mid-rank on ties", () => {
    expect(cdf([0, 0.5, 1], [0, 50, 100], 25)).toBeCloseTo(0.25);
    expect(cdf([0, 0.5, 1], [0, 50, 100], -1)).toBe(0);
    expect(cdf([0, 0.5, 1], [0, 50, 100], 101)).toBe(1);
    expect(cdf([0, 0.5, 1], [0, 0, 10], 0)).toBeCloseTo(0.25);
  });

  it("referenceScales covers directional metrics present in the reference and applies log10", () => {
    const kr: Knowledge = {
      ...k,
      metrics: [metric({ key: "pop", kind: "higher_better", transform: "log10" })],
      reference: { set: "t", levels: [0, 1], metrics: { pop: { n: 2, quantiles: [10, 1000] } } },
    };
    const s = referenceScales(kr).get("pop")!;
    expect(s).toEqual({ type: "cdf", levels: [0, 1], quantiles: [1, 3] });
    expect(fit(kr.metrics[0], 100, undefined, referenceScales(kr))).toBeCloseTo(0.5);
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
