// Sharing a result: fixed text, per-city share pages and card images. Pure (no data import), so vite.config.ts and
// scripts/og.ts can use it as well as the UI. Nothing here takes the user's answers: a share carries only the
// city and the rounded score, and the share page / card show only the city's own statistics.
import { formatValue, formatYear } from "./format.ts";
import type { City, Knowledge } from "./model/types.ts";
import { SITE } from "./site.ts";

export const SITE_TITLE = "あなたの魂の故郷は世界のどこ？";
export const HASHTAG = "#魂の故郷診断";
export const CREDIT = "データ: GHSL・ERA5・ESA WorldCover・ITDP・OpenStreetMap";
export const OG_WIDTH = 1200;
export const OG_HEIGHT = 630;

/** Facts shown on the share page and the card: always the same metrics, so no city is described selectively. */
const FACTS = [
  { metric: "temp_warmest", short: "最暖月" },
  { metric: "temp_coldest", short: "最寒月" },
  { metric: "density_weighted", short: "人口加重密度" },
] as const;

export interface Fact {
  short: string;
  label: string;
  value: string;
  source: string;
  period: string;
}

export function cityFacts(k: Knowledge, city: City): Fact[] {
  return FACTS.flatMap(({ metric, short }) => {
    const m = k.metrics.find((x) => x.key === metric);
    const mv = city.metrics[metric];
    if (!m || !mv || mv.value === null) return [];
    const source = k.sources.find((s) => s.id === mv.sourceId)?.title ?? mv.sourceId;
    return [{ short, label: m.label, value: formatValue(mv.value, m.unit), source, period: formatYear(mv.year) }];
  });
}

/** "最暖月 26.9℃・最寒月 4.9℃・人口加重密度 10,264 人/km²" */
export const factsLine = (facts: Fact[]) => facts.map((f) => `${f.short} ${f.value}`).join("・");

export const resultPath = (cityId: string) => `r/${cityId}/`;
export const shareUrl = (cityId: string) => `${SITE.url}${resultPath(cityId)}`;
export const ogImagePath = (cityId: string) => `og/${cityId}.png`;
export const ogImageUrl = (cityId: string) => `${SITE.url}${ogImagePath(cityId)}`;

/** The only text a share sends. Fixed template, no free text. `score` is already rounded (roundBounded). */
export const shareText = (city: Pick<City, "nameJa" | "countryName">, score: string) =>
  `私の魂の故郷は${city.nameJa}（${city.countryName}）でした。適合度 ${score}/100 ${HASHTAG}`;

export const xIntentUrl = (text: string, url: string) =>
  `https://x.com/intent/post?${new URLSearchParams({ text, url }).toString()}`;

/** X's weighted length (twitter-text v3): Latin and general punctuation count 1, everything else 2, a URL 23. */
export function xWeightedLength(text: string, urls = 0): number {
  let n = 0;
  for (const ch of text) {
    const c = ch.codePointAt(0)!;
    const light =
      c <= 0x10ff || (c >= 0x2000 && c <= 0x200d) || (c >= 0x2010 && c <= 0x201f) || (c >= 0x2032 && c <= 0x2037);
    n += light ? 1 : 2;
  }
  return n + urls * (23 + 1);
}
export const X_MAX_WEIGHTED = 280;

const ESC: Record<string, string> = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
export const escapeHtml = (s: string) => s.replace(/[&<>"']/g, (c) => ESC[c]);

/** Static share page for one city (dist/r/<id>/index.html). `base` is Vite's base, e.g. "/find-your-soul-city/". */
export function renderSharePage(k: Knowledge, city: City, base: string): string {
  const facts = cityFacts(k, city);
  const title = `魂の故郷診断の結果: ${city.nameJa}`;
  const description = `${city.nameJa}（${city.countryName}）: ${factsLine(facts)}。公開統計で世界の ${k.cities.length} 都市を比べる診断です。`;
  const image = ogImageUrl(city.id);
  const url = shareUrl(city.id);
  const alt = `あなたの魂の故郷は${city.nameJa}。${factsLine(facts)}`;
  const e = escapeHtml;
  const meta = [
    ["property", "og:type", "website"],
    ["property", "og:site_name", SITE_TITLE],
    ["property", "og:locale", "ja_JP"],
    ["property", "og:title", title],
    ["property", "og:description", description],
    ["property", "og:url", url],
    ["property", "og:image", image],
    ["property", "og:image:width", String(OG_WIDTH)],
    ["property", "og:image:height", String(OG_HEIGHT)],
    ["property", "og:image:alt", alt],
    ["name", "twitter:card", "summary_large_image"],
    ["name", "twitter:title", title],
    ["name", "twitter:description", description],
    ["name", "twitter:image", image],
    ["name", "twitter:image:alt", alt],
  ]
    .map(([attr, key, value]) => `    <meta ${attr}="${key}" content="${e(value)}" />`)
    .join("\n");
  const rows = facts
    .map(
      (f) =>
        `        <li><span>${e(f.label)}</span> <b>${e(f.value)}</b><small>${e(f.source)}、${e(f.period)}</small></li>`,
    )
    .join("\n");

  return `<!doctype html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
    <title>${e(title)}</title>
    <meta name="description" content="${e(description)}" />
    <link rel="canonical" href="${e(url)}" />
${meta}
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><circle cx='8' cy='8' r='5' fill='%23D99A2B'/></svg>" />
    <style>
      :root { --paper: #e8ede9; --ink: #1d2b36; --muted: #5a6971; --rule: #c2ccc7; --sea: #2b6e8c; color-scheme: light; }
      @media (prefers-color-scheme: dark) {
        :root { --paper: #13202a; --ink: #e2e9e5; --muted: #94a4ab; --rule: #2c3d47; --sea: #6cb4d2; color-scheme: dark; }
      }
      * { box-sizing: border-box; }
      body { margin: 0; background: var(--paper); color: var(--ink); line-height: 1.75;
        font-family: "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Noto Sans JP", "Yu Gothic UI", Meiryo, system-ui, sans-serif; }
      main { max-width: 38rem; margin: 0 auto; padding: 2rem 1rem 4rem; }
      img { display: block; width: 100%; height: auto; border-radius: 0.75rem; border: 1px solid var(--rule); }
      .kicker { margin: 1.5rem 0 0; color: var(--muted); }
      h1 { margin: 0; font-size: 2.25rem; line-height: 1.3; }
      .where { margin: 0.25rem 0 0; }
      ul { margin: 1.25rem 0 0; padding: 0; list-style: none; }
      li { padding: 0.5rem 0; border-bottom: 1px solid var(--rule); }
      li b { font-variant-numeric: tabular-nums; }
      li small { display: block; color: var(--muted); font-size: 0.8125rem; }
      .note { color: var(--muted); font-size: 0.8125rem; }
      .cta { display: inline-block; margin-top: 2rem; padding: 0.75rem 1.75rem; border-radius: 999px;
        background: var(--ink); color: var(--paper); font-weight: 700; text-decoration: none; }
      .cta:focus-visible { outline: 2px solid var(--sea); outline-offset: 3px; }
    </style>
  </head>
  <body>
    <main>
      <img src="${e(base + ogImagePath(city.id))}" width="${OG_WIDTH}" height="${OG_HEIGHT}" alt="${e(alt)}" />
      <p class="kicker">魂の故郷診断で選ばれた都市</p>
      <h1>${e(city.nameJa)}</h1>
      <p class="where">${e(city.nameEn)}（${e(city.countryName)}）</p>
      <ul>
${rows}
      </ul>
      <p class="note">
        都市の数字は公開統計から計算した値です。このページには、診断した人の回答も適合度も含まれていません。都市は行政区域ではなく
        GHS-UCDB の都市圏（連続して市街化した範囲）です。
      </p>
      <a class="cta" href="${e(base)}">自分も診断する</a>
      <p class="note">${e(CREDIT)}</p>
    </main>
  </body>
</html>
`;
}
