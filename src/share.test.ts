import { existsSync, readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import raw from "./generated/knowledge.json";
import type { Knowledge } from "./model/types.ts";
import {
  OG_HEIGHT,
  OG_WIDTH,
  X_MAX_WEIGHTED,
  cityFacts,
  renderSharePage,
  shareText,
  shareUrl,
  xIntentUrl,
  xWeightedLength,
} from "./share.ts";
import { SITE } from "./site.ts";

const k = raw as Knowledge;

/** Width and height from a PNG's IHDR chunk. */
function pngSize(path: string): [number, number] {
  const b = readFileSync(path);
  expect(b.subarray(1, 4).toString("latin1")).toBe("PNG");
  return [b.readUInt32BE(16), b.readUInt32BE(20)];
}

describe("share cards", () => {
  it.each(["default", ...k.cities.map((c) => c.id)])("public/og/%s.png exists at 1200x630 (run `pnpm og`)", (id) => {
    const path = `public/og/${id}.png`;
    expect(existsSync(path), `${path} missing: run \`pnpm og ${id === "default" ? "" : id}\``).toBe(true);
    expect(pngSize(path)).toEqual([OG_WIDTH, OG_HEIGHT]);
  });
});

describe("share text", () => {
  it("fits X's limit for every city at the longest score", () => {
    const tooLong = k.cities.filter((c) => xWeightedLength(shareText(c, "1 未満"), 1) > X_MAX_WEIGHTED);
    expect(tooLong.map((c) => c.id)).toEqual([]);
  });

  it("is the fixed template and carries no answers", () => {
    const tokyo = k.cities.find((c) => c.id === "tokyo")!;
    expect(shareText(tokyo, "87")).toBe("私の魂の故郷は東京（日本）でした。適合度 87/100 #魂の故郷診断");
    expect(shareUrl("tokyo")).toBe(`${SITE.url}r/tokyo/`);
    const intent = new URL(xIntentUrl(shareText(tokyo, "87"), shareUrl("tokyo")));
    expect(intent.origin + intent.pathname).toBe("https://x.com/intent/post");
    expect([...intent.searchParams.keys()]).toEqual(["text", "url"]);
    expect(intent.searchParams.get("url")).toBe(`${SITE.url}r/tokyo/`);
  });
});

describe("share page", () => {
  it("has the city's meta and facts from the data", () => {
    const tokyo = k.cities.find((c) => c.id === "tokyo")!;
    const html = renderSharePage(k, tokyo, "/find-your-soul-city/");
    expect(html).toContain('<meta property="og:title" content="魂の故郷診断の結果: 東京" />');
    expect(html).toContain(`<meta property="og:image" content="${SITE.url}og/tokyo.png" />`);
    expect(html).toContain(`<link rel="canonical" href="${SITE.url}r/tokyo/" />`);
    expect(html).toContain('<meta name="twitter:card" content="summary_large_image" />');
    expect(html).toContain('src="/find-your-soul-city/og/tokyo.png"');
    expect(html).toContain('href="/find-your-soul-city/">自分も診断する</a>');
    expect(html).not.toContain("<script");
    for (const f of cityFacts(k, tokyo)) expect(html).toContain(f.value);
  });

  it("every city has at least two facts", () => {
    expect(k.cities.filter((c) => cityFacts(k, c).length < 2).map((c) => c.id)).toEqual([]);
  });
});
