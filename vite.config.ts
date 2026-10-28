import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

// GitHub Pages serves project sites under /<repo>/. The deploy workflow sets BASE_PATH.
export default defineConfig({
  base: process.env.BASE_PATH ?? "/",
  plugins: [react()],
});
