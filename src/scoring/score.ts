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

/**
 * How a directional metric value becomes 0–1 (reversed for lower_better):
 * - `cdf`: percentile within a reference distribution (piecewise-linear between quantiles, mid-rank on ties). Default.
 * - `range`: linear between `lo` and `hi`, clamped (validation alternative).
 * Values are in transformed space (log10 where the metric says so).
 */
export type Scale = { type: "cdf"; levels: number[]; quantiles: number[] } | { type: "range"; lo: number; hi: number };
export type Scales = Map<string, Scale>;

export interface RankOptions {
  /** Override the directional scales (validation: normalisation sensitivity). */
  scales?: Scales;
  /** Override the coverage threshold (validation: missing-data handling). */
  minCoverage?: number;
}

const qualityRank = (q: Quality) => QUALITY_ORDER.indexOf(q as (typeof QUALITY_ORDER)[number]);

const t = (m: Metric, v: number) => (m.transform === "log10" ? Math.log10(v) : v);

export function quantile(sorted: number[], q: number): number {
  const pos = (sorted.length - 1) * q;
  const i = Math.floor(pos);
  return sorted[i] + (sorted[Math.min(i + 1, sorted.length - 1)] - sorted[i]) * (pos - i);
}

/** q10–q90 robust scale for directional metrics, over the given cities (default: all) that have a value. */
export function buildScales(k: Knowledge, cities: City[] = k.cities, q: [number, number] = [0.1, 0.9]): Scales {
  const scales: Scales = new Map();
  for (const m of k.metrics) {
    if (m.kind === "ideal") continue;
    const vs = cities
      .map((c) => c.metrics[m.key]?.value)
      .filter((v): v is number => v != null)
      .map((v) => t(m, v))
      .toSorted((a, b) => a - b);
    if (vs.length) scales.set(m.key, { type: "range", lo: quantile(vs, q[0]), hi: quantile(vs, q[1]) });
  }
  return scales;
}

/** Percentile scales from the knowledge bundle's reference distribution (all urban centres >= 1M). */
export function referenceScales(k: Knowledge): Scales {
  const scales: Scales = new Map();
  for (const m of k.metrics) {
    const r = k.reference.metrics[m.key];
    if (m.kind === "ideal" || !r) continue;
    scales.set(m.key, { type: "cdf", levels: k.reference.levels, quantiles: r.quantiles.map((v) => t(m, v)) });
  }
  return scales;
}

/** Empirical CDF from quantiles: linear between quantile points; a run of equal quantiles gets its middle level. */
export function cdf(levels: number[], qs: number[], x: number): number {
  if (x < qs[0]) return 0;
  if (x > qs[qs.length - 1]) return 1;
  const eq = qs.flatMap((q, i) => (q === x ? [levels[i]] : []));
  if (eq.length) return (eq[0] + eq[eq.length - 1]) / 2;
  const i = qs.findIndex((q) => q > x);
  return levels[i - 1] + ((levels[i] - levels[i - 1]) * (x - qs[i - 1])) / (qs[i] - qs[i - 1]);
}

export function fit(m: Metric, value: number, ideal: number | undefined, scales: Scales): number {
  if (m.kind === "ideal") {
    if (ideal === undefined || m.tolerance === null) throw new Error(`ideal/tolerance missing for ${m.key}`);
    const d = (t(m, value) - t(m, ideal)) / m.tolerance;
    return Math.exp(-0.5 * d * d);
  }
  const s = scales.get(m.key);
  if (!s) throw new Error(`no scale for ${m.key}`);
  const v = t(m, value);
  const x =
    s.type === "cdf"
      ? cdf(s.levels, s.quantiles, v)
      : s.hi === s.lo
        ? 1
        : Math.min(1, Math.max(0, (v - s.lo) / (s.hi - s.lo)));
  return m.kind === "lower_better" ? 1 - x : x;
}

function scoreCity(metrics: Map<string, Metric>, c: City, prefs: Preference[], scales: Scales): CityResult {
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

export function rank(k: Knowledge, prefs: Preference[], opts: RankOptions = {}): Ranking {
  const scales = opts.scales ?? referenceScales(k);
  const minCoverage = opts.minCoverage ?? k.minCoverage;
  const metrics = new Map(k.metrics.map((m) => [m.key, m]));
  const results = k.cities
    .map((c) => scoreCity(metrics, c, prefs, scales))
    .toSorted((a, b) => b.total - a.total || a.cityId.localeCompare(b.cityId));
  return {
    ranked: results.filter((r) => r.coverage >= minCoverage),
    insufficient: results.filter((r) => r.coverage < minCoverage),
  };
}

/** Share of ±10% single-axis weight perturbations that keep the same #1. */
export function stability(k: Knowledge, prefs: Preference[], opts: RankOptions = {}): number {
  const scales = opts.scales ?? referenceScales(k);
  const top = rank(k, prefs, { ...opts, scales }).ranked[0]?.cityId;
  const runs = prefs
    .filter((p) => p.weight > 0)
    .flatMap((p) => [0.9, 1.1].map((f) => prefs.map((q) => (q === p ? { ...q, weight: q.weight * f } : q))));
  if (!top || runs.length === 0) return 1;
  return runs.filter((r) => rank(k, r, { ...opts, scales }).ranked[0]?.cityId === top).length / runs.length;
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
