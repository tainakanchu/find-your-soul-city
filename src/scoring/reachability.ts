// Reachability: for each city, search for an answer set that ranks it #1.
// Greedy starts (answers closest to the city's own values; three variants for the importance questions)
// + hill climbing on (rank, margin to the best rival).
// A city that no answer can bring to #1 is effectively invisible in the quiz.
import { toPreferences, type Answer } from "../answers.ts";
import type { Knowledge } from "../model/types.ts";
import { fit, rank, referenceScales } from "./score.ts";

export interface Reach {
  cityId: string;
  bestRank: number;
  answers: Record<string, Answer>;
}

export function reachability(k: Knowledge, maxSteps = 60): Reach[] {
  const scales = referenceScales(k);
  const metricOf = new Map(k.metrics.map((m) => [m.key, m]));
  const t = (key: string, v: number) => (metricOf.get(key)!.transform === "log10" ? Math.log10(v) : v);
  type Answers = Record<string, Answer>;
  const result = (a: Answers, id: string) => {
    const r = rank(k, toPreferences(k.questions, a), { scales }).ranked;
    const i = r.findIndex((x) => x.cityId === id);
    const rival = r.find((x) => x.cityId !== id);
    return { pos: i < 0 ? Infinity : i + 1, margin: i < 0 ? -Infinity : r[i].total - (rival?.total ?? 0) };
  };

  // Directional answer for a city's percentile f: three start variants (bold / graded / climate-only).
  const SEEDS: ((f: number) => number)[] = [
    (f) => (f >= 0.5 ? 2 : 0),
    (f) => (f >= 0.8 ? 2 : f >= 0.5 ? 1 : 0),
    () => 0,
  ];

  function seed(id: string, directional: (f: number) => number): Answers {
    const c = k.cities.find((x) => x.id === id)!;
    const a: Answers = {};
    for (const q of k.questions) {
      const v = c.metrics[q.metrics[0]]?.value;
      if (q.answerKind === "ideal") {
        if (v == null) a[q.id] = { choice: q.options[0].value, importance: 0 };
        else {
          const best = q.options.reduce((b, o) =>
            Math.abs(t(q.metrics[0], o.value) - t(q.metrics[0], v)) <
            Math.abs(t(q.metrics[0], b.value) - t(q.metrics[0], v))
              ? o
              : b,
          );
          a[q.id] = { choice: best.value, importance: 2 };
        }
      } else {
        const fs = q.metrics.map((key) => {
          const x = c.metrics[key]?.value;
          return x == null ? 0 : fit(metricOf.get(key)!, x, undefined, scales);
        });
        const f = fs.reduce((s, x) => s + x, 0) / fs.length;
        a[q.id] = { choice: directional(f), importance: 1 };
      }
    }
    return a;
  }

  function neighbours(a: Answers): Answers[] {
    const out: Answers[] = [];
    for (const q of k.questions) {
      const cur = a[q.id];
      for (const o of q.options) if (o.value !== cur.choice) out.push({ ...a, [q.id]: { ...cur, choice: o.value } });
      if (q.importanceControl)
        for (const w of [0, 1, 2]) if (w !== cur.importance) out.push({ ...a, [q.id]: { ...cur, importance: w } });
    }
    return out;
  }

  const climb = (id: string, start: Answers) => {
    let a = start;
    let r = result(a, id);
    for (let step = 0; step < maxSteps && r.pos > 1; step++) {
      let best = { a, r };
      for (const n of neighbours(a)) {
        const rn = result(n, id);
        if (rn.pos < best.r.pos || (rn.pos === best.r.pos && rn.margin > best.r.margin)) best = { a: n, r: rn };
      }
      if (best.a === a) break;
      ({ a, r } = best);
    }
    return { a, r };
  };

  return k.cities.map((c) => {
    let best: { a: Answers; r: { pos: number; margin: number } } | undefined;
    for (const variant of SEEDS) {
      const got = climb(c.id, seed(c.id, variant));
      if (!best || got.r.pos < best.r.pos || (got.r.pos === best.r.pos && got.r.margin > best.r.margin)) best = got;
      if (best.r.pos === 1) break;
    }
    return { cityId: c.id, bestRank: best!.r.pos, answers: best!.a };
  });
}
