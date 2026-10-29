import { describe, expect, it } from "vitest";
import raw from "../generated/knowledge.json";
import type { Knowledge } from "../model/types.ts";
import { concentration } from "./concentration.ts";

// Guard rails for "a few cities win everything" under seeded uniform-random answers.
// Thresholds sit a little beyond the current values. History:
// - model 0.3.0 / 130 cities: max 11.7x expected, 41 effective winners, Gini 0.63.
// - 2026-10-29, natural-hazard question added (model 0.4.0, 15 metrics): Singapore rose to ~15-19x because it is the
//   only tropical city that is high on infrastructure AND nearly flood/typhoon-free (Bangkok 75 %, Phnom Penh 58 %,
//   Ho Chi Minh 28 % flood exposure). That is the data, not a scoring artefact, so the bounds were relaxed to
//   max 20x, >= 26 effective winners, Gini <= 0.68. Look at knowledge/reports/validation.md before relaxing again.
describe("concentration of #1 under random answers", () => {
  const c = concentration(raw as unknown as Knowledge, 1000, 1);

  it("no single city takes more than 20x its fair share of #1", () => {
    expect(c.maxRatio, `${c.maxCity} ${(c.maxShare * 100).toFixed(1)}%`).toBeLessThanOrEqual(20);
  });

  it("at least 26 cities effectively share the #1 spot", () => {
    expect(c.effectiveWinners).toBeGreaterThanOrEqual(26);
  });

  it("Gini of #1 shares stays at or below 0.68", () => {
    expect(c.gini).toBeLessThanOrEqual(0.68);
  });
});
