import { QUALITY_ORDER, type City, type Knowledge, type Metric, type Quality } from "../model/types.ts";

/** One preference per metric. `ideal` is required for `kind: ideal` metrics. */
export interface Preference {
  metric: string;
  weight: number;
  ideal?: number;
}

export interface AxisScore {
  metric: string;
  weight: number;
  value: number | null;
  ideal?: number;
  fit: number | null;
}

export interface CityResult {
  cityId: string;
  total: number;
  coverage: number;
  quality: Quality;
  axes: AxisScore[];
}

export interface Ranking {
  ranked: CityResult[];
  insufficient: CityResult[];
}

type Scales = Map<string, { lo: number; hi: number }>;

const qualityRank = (q: Quality) => QUALITY_ORDER.indexOf(q as (typeof QUALITY_ORDER)[number]);

const t = (m: Metric, v: number) => (m.transform === "log10" ? Math.log10(v) : v);

function quantile(sorted: number[], q: number): number {
  const pos = (sorted.length - 1) * q;
  const i = Math.floor(pos);
  return sorted[i] + (sorted[Math.min(i + 1, sorted.length - 1)] - sorted[i]) * (pos - i);
}

/** q10–q90 robust scale for higher_better metrics, over cities with a value. */
export function buildScales(k: Knowledge): Scales {
  const scales: Scales = new Map();
  for (const m of k.metrics) {
    if (m.kind !== "higher_better") continue;
    const vs = k.cities
      .map((c) => c.metrics[m.key]?.value)
      .filter((v): v is number => v != null)
      .toSorted((a, b) => a - b);
    scales.set(m.key, { lo: quantile(vs, 0.1), hi: quantile(vs, 0.9) });
  }
  return scales;
}

export function fit(m: Metric, value: number, ideal: number | undefined, scales: Scales): number {
  if (m.kind === "ideal") {
    if (ideal === undefined || m.tolerance === null) throw new Error(`ideal/tolerance missing for ${m.key}`);
    const d = (t(m, value) - t(m, ideal)) / m.tolerance;
    return Math.exp(-0.5 * d * d);
  }
  const { lo, hi } = scales.get(m.key)!;
  return hi === lo ? 1 : Math.min(1, Math.max(0, (value - lo) / (hi - lo)));
}

function scoreCity(k: Knowledge, c: City, prefs: Preference[], scales: Scales): CityResult {
  const metrics = new Map(k.metrics.map((m) => [m.key, m]));
  let sum = 0;
  let used = 0;
  let all = 0;
  let quality: Quality = "observed";
  const axes = prefs.map((p): AxisScore => {
    const mv = c.metrics[p.metric];
    const value = mv?.value ?? null;
    all += p.weight;
    if (value === null || p.weight === 0) return { ...p, value, fit: null };
    const f = fit(metrics.get(p.metric)!, value, p.ideal, scales);
    sum += p.weight * f;
    used += p.weight;
    if (qualityRank(mv.quality) < qualityRank(quality)) quality = mv.quality;
    return { ...p, value, fit: f };
  });
  return {
    cityId: c.id,
    total: used === 0 ? 0 : (100 * sum) / used,
    coverage: all === 0 ? 0 : used / all,
    quality,
    axes,
  };
}

export function rank(k: Knowledge, prefs: Preference[]): Ranking {
  const scales = buildScales(k);
  const results = k.cities
    .map((c) => scoreCity(k, c, prefs, scales))
    .toSorted((a, b) => b.total - a.total || a.cityId.localeCompare(b.cityId));
  return {
    ranked: results.filter((r) => r.coverage >= k.minCoverage),
    insufficient: results.filter((r) => r.coverage < k.minCoverage),
  };
}

/** Share of ±10% single-axis weight perturbations that keep the same #1. */
export function stability(k: Knowledge, prefs: Preference[]): number {
  const top = rank(k, prefs).ranked[0]?.cityId;
  const runs = prefs
    .filter((p) => p.weight > 0)
    .flatMap((p) => [0.9, 1.1].map((f) => prefs.map((q) => (q === p ? { ...q, weight: q.weight * f } : q))));
  if (!top || runs.length === 0) return 1;
  return runs.filter((r) => rank(k, r).ranked[0]?.cityId === top).length / runs.length;
}

export function explain(r: CityResult): { matches: AxisScore[]; mismatches: AxisScore[] } {
  const scored = r.axes.filter((a): a is AxisScore & { fit: number } => a.fit !== null && a.weight > 0);
  return {
    matches: scored
      .filter((a) => a.fit >= 0.6)
      .toSorted((a, b) => b.weight * b.fit - a.weight * a.fit)
      .slice(0, 3),
    mismatches: scored
      .filter((a) => a.fit < 0.5)
      .toSorted((a, b) => b.weight * (1 - b.fit) - a.weight * (1 - a.fit))
      .slice(0, 2),
  };
}
