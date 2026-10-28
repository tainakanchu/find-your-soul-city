import raw from "./generated/knowledge.json";
import type { Knowledge, Quality } from "./model/types.ts";

export const knowledge = raw as Knowledge;

export const metricByKey = new Map(knowledge.metrics.map((m) => [m.key, m]));
export const cityById = new Map(knowledge.cities.map((c) => [c.id, c]));
export const sourceById = new Map(knowledge.sources.map((s) => [s.id, s]));

export const hasPlaceholder = knowledge.cities.some((c) =>
  Object.values(c.metrics).some((m) => m.quality === "placeholder"),
);

export const QUALITY_LABEL: Record<Quality, string> = {
  observed: "実測",
  estimated: "推定",
  imputed: "補完",
  placeholder: "仮値",
  missing: "欠損",
};

export const formatValue = (v: number | null | undefined, unit: string) =>
  v == null
    ? "—"
    : `${v.toLocaleString("ja-JP", { maximumFractionDigits: 1 })}${unit === "%" || unit === "℃" ? "" : " "}${unit}`;

export const formatCoord = (lat: number, lon: number) =>
  `${Math.abs(lat).toFixed(2)}°${lat >= 0 ? "N" : "S"} ${Math.abs(lon).toFixed(2)}°${lon >= 0 ? "E" : "W"}`;
