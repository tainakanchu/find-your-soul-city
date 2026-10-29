// Pure formatting helpers. No data imports, so Node scripts (scripts/og.ts) and vite.config.ts can use them too.

const num = (v: number, digits: number) => v.toLocaleString("ja-JP", { maximumFractionDigits: digits });

export const formatValue = (v: number | null | undefined, unit: string) => {
  if (v == null) return "—";
  switch (unit) {
    case "人":
      return v >= 10_000 ? `${num(v / 10_000, 0)} 万人` : `${num(v, 0)} 人`;
    case "人/km²":
    case "mm":
      return `${num(v, 0)} ${unit}`;
    case "時刻": {
      // Decimal hours on a 24 h clock; >= 24 is after midnight (Reykjavik 24.03 -> 翌 0:02).
      const min = Math.round(v * 60);
      const h = Math.floor(min / 60);
      const time = `${h % 24}:${String(min % 60).padStart(2, "0")}`;
      return h >= 24 ? `翌 ${time}` : time;
    }
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

/**
 * Round a 0–max quantity without overstating the ends: 99.6 → "99", 0.3 → "1 未満", only exact values give max / 0.
 */
export function roundBounded(x: number, max = 100): string {
  const r = Math.round(x);
  if (r >= max && x < max) return String(max - 1);
  if (r <= 0 && x > 0) return "1 未満";
  return String(r);
}

/** "東京（日本）", or just the name when the city and the country/region share it (香港, シンガポール). */
export const placeLabel = (c: { nameJa: string; countryName: string }) =>
  c.nameJa === c.countryName ? c.nameJa : `${c.nameJa}（${c.countryName}）`;
