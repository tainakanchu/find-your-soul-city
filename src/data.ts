import raw from "./generated/knowledge.json";
import type { Knowledge, Quality } from "./model/types.ts";

export { formatValue, formatYear, roundBounded, placeLabel } from "./format.ts";

export const knowledge = raw as Knowledge;

export const metricByKey = new Map(knowledge.metrics.map((m) => [m.key, m]));
export const cityById = new Map(knowledge.cities.map((c) => [c.id, c]));
export const sourceById = new Map(knowledge.sources.map((s) => [s.id, s]));

export const QUALITY_LABEL: Record<Quality, string> = {
  observed: "実測",
  estimated: "推定",
  imputed: "補完",
  missing: "欠損",
};

export const KIND_LABEL = { higher_better: "多いほど良い", lower_better: "少ないほど良い" } as const;

export const formatCoord = (lat: number, lon: number) =>
  `${Math.abs(lat).toFixed(2)}°${lat >= 0 ? "N" : "S"} ${Math.abs(lon).toFixed(2)}°${lon >= 0 ? "E" : "W"}`;

const REF_COUNT = /\((\d+)\)/.exec(knowledge.reference.set)?.[1] ?? "";

/** Plain-language position of a directional value in the reference distribution (fit = percentile, reversed for lower_better). */
export function rankWords(kind: "higher_better" | "lower_better", fit: number): string {
  const top = Math.max(1, Math.round((1 - fit) * 100));
  const side = kind === "higher_better" ? "多いほうから" : "少ないほうから";
  return `世界の人口 100 万人以上の都市圏 ${REF_COUNT} の中で、${side}およそ ${top}% の位置`;
}

/** Words for the ±10% weight-perturbation stability. */
export const stabilityWords = (s: number) =>
  s >= 0.9
    ? "はっきりした 1 位です"
    : s >= 0.6
      ? "おおむね安定した 1 位です"
      : "僅差で、条件が少し変わると入れ替わりやすい 1 位です";
