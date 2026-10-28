import { describe, expect, it } from "vitest";
import raw from "../generated/knowledge.json";
import type { Knowledge } from "../model/types.ts";
import { concentration } from "./concentration.ts";

// Guard rails for "a few cities win everything" under seeded uniform-random answers.
// Thresholds sit a little beyond the current values (model 0.2.0: max 14% = 12.3x expected,
// 22 effective winners, Gini 0.64). If a data/model change crosses them, look at
// knowledge/reports/validation.md before relaxing anything.
describe("concentration of #1 under random answers", () => {
  const c = concentration(raw as unknown as Knowledge, 1000, 1);

  it("no single city takes more than 15x its fair share of #1", () => {
    expect(c.maxRatio, `${c.maxCity} ${(c.maxShare * 100).toFixed(1)}%`).toBeLessThanOrEqual(15);
  });

  it("at least 18 cities effectively share the #1 spot", () => {
    expect(c.effectiveWinners).toBeGreaterThanOrEqual(18);
  });

  it("Gini of #1 shares stays at or below 0.70", () => {
    expect(c.gini).toBeLessThanOrEqual(0.7);
  });
});
