import raw from "./generated/knowledge.json";
import type { Knowledge, Quality } from "./model/types.ts";

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

const num = (v: number, digits: number) => v.toLocaleString("ja-JP", { maximumFractionDigits: digits });

export const formatValue = (v: number | null | undefined, unit: string) => {
  if (v == null) return "—";
  switch (unit) {
    case "人":
      return v >= 10_000 ? `${num(v / 10_000, 0)} 万人` : `${num(v, 0)} 人`;
    case "人/km²":
    case "mm":
      return `${num(v, 0)} ${unit}`;
    case "%":
    case "℃":
      return `${num(v, 1)}${unit}`;
    default:
      return `${num(v, 1)} ${unit}`;
  }
};

/** 2024 -> "2024 年", "1990-2019" -> "1990–2019 年平均". */
export const formatYear = (year: number | string | null) => {
  if (year === null) return "年不明";
  if (typeof year === "number") return `${year} 年`;
  return /^\d{4}-\d{4}$/.test(year) ? `${year.replace("-", "–")} 年平均` : year;
};

export const KIND_LABEL = { higher_better: "多いほど良い", lower_better: "少ないほど良い" } as const;

export const formatCoord = (lat: number, lon: number) =>
  `${Math.abs(lat).toFixed(2)}°${lat >= 0 ? "N" : "S"} ${Math.abs(lon).toFixed(2)}°${lon >= 0 ? "E" : "W"}`;

/**
 * Round a 0–max quantity without overstating the ends: 99.6 → "99", 0.3 → "1 未満", only exact values give max / 0.
 */
export function roundBounded(x: number, max = 100): string {
  const r = Math.round(x);
  if (r >= max && x < max) return String(max - 1);
  if (r <= 0 && x > 0) return "1 未満";
  return String(r);
}
