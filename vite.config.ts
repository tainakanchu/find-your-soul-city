import { readFileSync } from "node:fs";
import react from "@vitejs/plugin-react";
import { defineConfig, type Plugin } from "vitest/config";
import { findPlaceholders } from "./src/model/guard.ts";

/** Production builds fail if the bundled data contains placeholder values (defence in depth after knowledge:build). */
function placeholderGuard(): Plugin {
  return {
    name: "placeholder-guard",
    apply: "build",
    buildStart() {
      const problems = findPlaceholders(JSON.parse(readFileSync("src/generated/knowledge.json", "utf8")));
      if (problems.length) this.error(`placeholder data in production build:\n${problems.slice(0, 20).join("\n")}`);
    },
  };
}

// GitHub Pages serves project sites under /<repo>/. The deploy workflow sets BASE_PATH.
export default defineConfig({
  base: process.env.BASE_PATH ?? "/",
  plugins: [react(), placeholderGuard()],
});
