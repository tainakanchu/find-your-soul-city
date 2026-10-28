// Card images for link previews: public/og/<city_id>.png (one per city) and public/og/default.png, 1200x630.
// Rendered from an HTML template with Playwright and committed, so CI needs no browser.
// Usage: pnpm og [city_id ...]   (no ids: every city and the default card)
//
// Playwright is not a project dependency; it is resolved from the environment (global install / NODE_PATH).
// Fonts are the system's: the Japanese text needs a Japanese font installed (fc-list :lang=ja).
import { mkdirSync, readFileSync } from "node:fs";
import { createRequire } from "node:module";
import type { City, Knowledge } from "../src/model/types.ts";
import { CREDIT, OG_HEIGHT, OG_WIDTH, SITE_TITLE, cityFacts, escapeHtml as e } from "../src/share.ts";
import { SITE } from "../src/site.ts";

interface Page {
  setContent(html: string): Promise<void>;
  evaluate<T>(fn: () => T | Promise<T>): Promise<T>;
  screenshot(o: { path: string; type: "png" }): Promise<unknown>;
}
interface Browser {
  newPage(o: { viewport: { width: number; height: number }; deviceScaleFactor: number }): Promise<Page>;
  close(): Promise<void>;
}

const OUT = "public/og";
const k: Knowledge = JSON.parse(readFileSync("src/generated/knowledge.json", "utf8"));
const siteLabel = SITE.url.replace(/^https?:\/\//, "").replace(/\/$/, "");

// Same palette as src/styles.css (light).
const CSS = `
  * { box-sizing: border-box; margin: 0; }
  html, body { width: ${OG_WIDTH}px; height: ${OG_HEIGHT}px; overflow: hidden; }
  body { position: relative; background: #e8ede9; color: #1d2b36;
    font-family: "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Noto Sans JP", "IPAPGothic", "IPAGothic", sans-serif; }
  svg.map { position: absolute; right: 68px; top: 250px; width: 324px; height: 174px; }
  .card { position: absolute; inset: 0; padding: 64px 80px 56px; display: flex; flex-direction: column; }
  .kicker { font-size: 34px; color: #5a6971; letter-spacing: 0.04em; }
  .name { margin-top: 6px; font-size: 150px; line-height: 1.12; font-weight: 700; white-space: nowrap; letter-spacing: 0.02em; }
  .en { margin-top: 8px; font-size: 40px;
    font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, "Bitstream Charter", "DejaVu Serif", serif; }
  .en span { font-family: "Hiragino Sans", "Noto Sans JP", "IPAPGothic", "IPAGothic", sans-serif; font-size: 32px; color: #5a6971; margin-left: 18px; }
  .facts { margin-top: auto; display: flex; gap: 56px; padding-top: 22px; border-top: 2px solid #c2ccc7; }
  .facts div { display: flex; flex-direction: column; }
  .facts small { font-size: 24px; color: #5a6971; }
  .facts b { font-size: 40px; font-weight: 700; font-variant-numeric: tabular-nums; }
  .foot { margin-top: 22px; display: flex; justify-content: space-between; font-size: 22px; color: #5a6971; }
  .foot .url { color: #2b6e8c; }
  body.default svg.map { top: 340px; }
  .title { font-size: 96px; line-height: 1.25; font-weight: 700; letter-spacing: 0.02em; }
  .lede { margin-top: 28px; max-width: 640px; font-size: 34px; line-height: 1.5; color: #5a6971; }
  .spacer { margin-top: auto; }
`;

/** Small equirectangular locator map of all cities (same projection as the app's WorldPlot), optional pin. */
function map(pin?: City): string {
  const W = 300;
  const H = 150;
  const x = (lon: number) => (((lon + 180) / 360) * W).toFixed(1);
  const y = (lat: number) => (((90 - lat) / 180) * H).toFixed(1);
  const dots = k.cities
    .filter((c) => c.id !== pin?.id)
    .map((c) => `<circle cx="${x(c.lon)}" cy="${y(c.lat)}" r="2.6" fill="#2b6e8c" opacity="0.45" />`)
    .join("");
  const mark = pin
    ? `<circle cx="${x(pin.lon)}" cy="${y(pin.lat)}" r="3.2" fill="#1d2b36" />` +
      `<circle cx="${x(pin.lon)}" cy="${y(pin.lat)}" r="10" fill="none" stroke="#c98a1e" stroke-width="3" />`
    : "";
  return `<svg class="map" width="${W}" height="${H}" viewBox="-12 -12 ${W + 24} ${H + 24}" aria-hidden="true">
    <rect x="0" y="0" width="${W}" height="${H}" fill="none" stroke="#c2ccc7" stroke-width="1.5" rx="6" />
    <line x1="0" y1="${H / 2}" x2="${W}" y2="${H / 2}" stroke="#5a6971" stroke-width="1" stroke-dasharray="4 4" opacity="0.5" />
    ${dots}${mark}</svg>`;
}

const doc = (body: string, cls = "") =>
  `<!doctype html><html lang="ja"><head><meta charset="UTF-8"><style>${CSS}</style></head><body class="${cls}">${body}</body></html>`;

const foot = `<div class="foot"><span>${e(CREDIT)}</span><span class="url">${e(siteLabel)}</span></div>`;

function cityCard(city: City): string {
  const facts = cityFacts(k, city)
    .map((f) => `<div><small>${e(f.short)}</small><b>${e(f.value)}</b></div>`)
    .join("");
  return doc(`${map(city)}<div class="card">
    <p class="kicker">あなたの魂の故郷は</p>
    <p class="name">${e(city.nameJa)}</p>
    <p class="en">${e(city.nameEn)}<span>${e(city.countryName)}</span></p>
    <div class="facts">${facts}</div>
    ${foot}
  </div>`);
}

function defaultCard(): string {
  return doc(
    `${map()}<div class="card">
    <p class="title">${e(SITE_TITLE).replace("は", "は<br>")}</p>
    <p class="lede">公開統計で世界の ${k.cities.length} 都市を比べる、<br />根拠つきの診断</p>
    <div class="spacer"></div>
    ${foot}
  </div>`,
    "default",
  );
}

const require = createRequire(import.meta.url);
let chromium: { launch(): Promise<Browser> };
try {
  ({ chromium } = require("playwright"));
} catch {
  console.error("playwright not found. Install it globally (or set NODE_PATH) to generate cards; CI does not need it.");
  process.exit(1);
}

const only = new Set(process.argv.slice(2));
const unknown = [...only].filter((id) => !k.cities.some((c) => c.id === id));
if (unknown.length) {
  console.error(`unknown city id: ${unknown.join(", ")}`);
  process.exit(2);
}

mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch();
try {
  const page = await browser.newPage({ viewport: { width: OG_WIDTH, height: OG_HEIGHT }, deviceScaleFactor: 1 });
  const render = async (html: string, path: string) => {
    await page.setContent(html);
    await page.evaluate(async () => {
      await document.fonts.ready;
      // Shrink long names until they fit the card width.
      const el = document.querySelector<HTMLElement>(".name");
      if (!el) return;
      let size = parseFloat(getComputedStyle(el).fontSize);
      while (el.scrollWidth > el.clientWidth && size > 40) {
        size -= 4;
        el.style.fontSize = `${size}px`;
      }
    });
    await page.screenshot({ path, type: "png" });
  };
  const cities = only.size ? k.cities.filter((c) => only.has(c.id)) : k.cities;
  for (const city of cities) await render(cityCard(city), `${OUT}/${city.id}.png`);
  if (!only.size) await render(defaultCard(), `${OUT}/default.png`);
  console.log(`✓ ${cities.length} city card(s)${only.size ? "" : " + default"} → ${OUT}/`);
} finally {
  await browser.close();
}
