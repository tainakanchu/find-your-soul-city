// How concentrated the #1 city is under random answers (seeded, reproducible).
// Uniform random answers are not real users; this is a smoke indicator for "a few cities win everything".
import { toPreferences, type Answer } from "../answers.ts";
import type { Knowledge } from "../model/types.ts";
import { rank, referenceScales } from "./score.ts";

/** mulberry32: small deterministic PRNG. */
export function rng(seed: number) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let x = a;
    x = Math.imul(x ^ (x >>> 15), x | 1);
    x ^= x + Math.imul(x ^ (x >>> 7), x | 61);
    return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
  };
}

export interface Concentration {
  samples: number;
  /** cityId -> share of samples where it is #1 */
  shares: Map<string, number>;
  maxShare: number;
  maxCity: string;
  /** maxShare ÷ (1 / number of cities) */
  maxRatio: number;
  /** 1 / Σ p² — how many cities effectively share the #1 spot (= city count if perfectly even) */
  effectiveWinners: number;
  /** Gini coefficient of the #1 shares (0 even … 1 one city wins all) */
  gini: number;
  /** cities that were never #1 */
  neverFirst: string[];
}

export function concentration(k: Knowledge, samples = 1000, seed = 20261029): Concentration {
  const rand = rng(seed);
  const pick = <T>(xs: T[]) => xs[Math.floor(rand() * xs.length)];
  const scales = referenceScales(k);
  const wins = new Map(k.cities.map((c) => [c.id, 0]));
  for (let i = 0; i < samples; i++) {
    const answers: Record<string, Answer> = Object.fromEntries(
      k.questions.map((q) => [
        q.id,
        { choice: pick(q.options).value, importance: q.importanceControl ? pick([0, 1, 2]) : 1 },
      ]),
    );
    const top = rank(k, toPreferences(k.questions, answers), { scales }).ranked[0]?.cityId;
    if (top) wins.set(top, wins.get(top)! + 1);
  }
  const shares = new Map([...wins].map(([id, w]) => [id, w / samples]));
  const ps = [...shares.values()].toSorted((a, b) => a - b);
  const [maxCity, maxShare] = [...shares].reduce((best, x) => (x[1] > best[1] ? x : best));
  const sum = ps.reduce((a, b) => a + b, 0);
  const gini = ps.reduce((acc, x, i) => acc + (2 * (i + 1) - ps.length - 1) * x, 0) / (ps.length * sum);
  return {
    samples,
    shares,
    maxShare,
    maxCity,
    maxRatio: maxShare * k.cities.length,
    effectiveWinners: 1 / ps.reduce((a, p) => a + p * p, 0),
    gini,
    neverFirst: [...shares].filter(([, p]) => p === 0).map(([id]) => id),
  };
}
