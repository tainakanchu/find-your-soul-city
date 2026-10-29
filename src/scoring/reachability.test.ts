import { describe, expect, it } from "vitest";
import raw from "../generated/knowledge.json";
import type { Knowledge } from "../model/types.ts";
import { reachability } from "./reachability.ts";

describe("reachability", () => {
  it("every city can be ranked #1 by some answer set", () => {
    const unreachable = reachability(raw as unknown as Knowledge)
      .filter((r) => r.bestRank > 1)
      .map((r) => `${r.cityId} (best ${r.bestRank})`);
    expect(unreachable).toEqual([]);
  });
});
