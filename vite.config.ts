import { readFileSync } from "node:fs";
import react from "@vitejs/plugin-react";
import { defineConfig, type Plugin } from "vitest/config";
import { findPlaceholders } from "./src/model/guard.ts";
import type { Knowledge } from "./src/model/types.ts";
import { OG_HEIGHT, OG_WIDTH, SITE_TITLE, renderSharePage } from "./src/share.ts";
import { SITE } from "./src/site.ts";

const readKnowledge = (): Knowledge => JSON.parse(readFileSync("src/generated/knowledge.json", "utf8"));

/** Production builds fail if the bundled data contains placeholder values (defence in depth after knowledge:build). */
function placeholderGuard(): Plugin {
  return {
    name: "placeholder-guard",
    apply: "build",
    buildStart() {
      const problems = findPlaceholders(readKnowledge());
      if (problems.length) this.error(`placeholder data in production build:\n${problems.slice(0, 20).join("\n")}`);
    },
  };
}

/**
 * Link previews. Root page gets OGP meta for the default card; each city gets a static, JS-free share page at
 * r/<city_id>/index.html whose meta points to that city's card (public/og/<id>.png, made by `pnpm og`).
 * Share links carry only the city id, never the user's answers.
 */
function sharePages(): Plugin {
  let base = "/";
  return {
    name: "share-pages",
    configResolved(config) {
      base = config.base;
    },
    transformIndexHtml() {
      const image = `${SITE.url}og/default.png`;
      const description = "10 数問の回答から、世界の都市のうちあなたの好みに合う場所を、根拠つきで提案します。";
      const tags: [string, string, string][] = [
        ["property", "og:type", "website"],
        ["property", "og:site_name", SITE_TITLE],
        ["property", "og:locale", "ja_JP"],
        ["property", "og:title", SITE_TITLE],
        ["property", "og:description", description],
        ["property", "og:url", SITE.url],
        ["property", "og:image", image],
        ["property", "og:image:width", String(OG_WIDTH)],
        ["property", "og:image:height", String(OG_HEIGHT)],
        ["name", "twitter:card", "summary_large_image"],
        ["name", "twitter:title", SITE_TITLE],
        ["name", "twitter:description", description],
        ["name", "twitter:image", image],
      ];
      return [
        { tag: "link", attrs: { rel: "canonical", href: SITE.url }, injectTo: "head" },
        ...tags.map(([attr, key, content]) => ({
          tag: "meta",
          attrs: { [attr]: key, content },
          injectTo: "head" as const,
        })),
      ];
    },
    generateBundle() {
      const k = readKnowledge();
      for (const city of k.cities) {
        this.emitFile({ type: "asset", fileName: `r/${city.id}/index.html`, source: renderSharePage(k, city, base) });
      }
    },
  };
}

// GitHub Pages serves project sites under /<repo>/. The deploy workflow sets BASE_PATH.
export default defineConfig({
  base: process.env.BASE_PATH ?? "/",
  plugins: [react(), placeholderGuard(), sharePages()],
});
