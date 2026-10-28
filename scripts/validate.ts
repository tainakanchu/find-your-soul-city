// Validation of the scoring model on the real data: score distributions, reachability, normalisation
// sensitivity, weight / missing-data robustness, regional balance, and fixed persona patterns.
// Usage: node scripts/validate.ts   (after knowledge:build) -> knowledge/reports/validation.md
import { readFileSync, writeFileSync } from "node:fs";
import { toPreferences, type Answer } from "../src/answers.ts";
import type { City, Knowledge, Question } from "../src/model/types.ts";
import { buildScales, quantile, rank, type Preference, type RankOptions, type Scales } from "../src/scoring/score.ts";

const k = JSON.parse(readFileSync("src/generated/knowledge.json", "utf8")) as Knowledge;
const N = Number(process.env.VALIDATE_N ?? 3000);
const SEED = 20261029;

// Deterministic PRNG (mulberry32) so the report is reproducible.
function rng(seed: number) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let x = a;
    x = Math.imul(x ^ (x >>> 15), x | 1);
    x ^= x + Math.imul(x ^ (x >>> 7), x | 61);
    return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
  };
}
const rand = rng(SEED);
const pick = <T>(xs: T[]) => xs[Math.floor(rand() * xs.length)];

function randomAnswers(qs: Question[]): Record<string, Answer> {
  return Object.fromEntries(
    qs.map((q) => [q.id, { choice: pick(q.options).value, importance: q.importanceControl ? pick([0, 1, 2]) : 1 }]),
  );
}

const samples: Preference[][] = Array.from({ length: N }, () => toPreferences(k.questions, randomAnswers(k.questions)));
const nameOf = new Map(k.cities.map((c) => [c.id, c.nameJa]));
const regionOf = new Map(k.cities.map((c) => [c.id, c.region]));
const pct = (x: number) => `${(100 * x).toFixed(1)}%`;
const f1 = (x: number) => x.toFixed(1);
const top = (prefs: Preference[], opts?: RankOptions, kk: Knowledge = k) => rank(kk, prefs, opts).ranked;
const jaccard = (a: string[], b: string[]) => {
  const A = new Set(a);
  const inter = b.filter((x) => A.has(x)).length;
  return inter / (A.size + b.length - inter);
};

const out: string[] = [];
const h = (s: string) => out.push("", `## ${s}`, "");
const table = (head: string[], rows: (string | number)[][]) => {
  out.push(`| ${head.join(" | ")} |`, `| ${head.map(() => "---").join(" | ")} |`);
  for (const r of rows) out.push(`| ${r.join(" | ")} |`);
};

const base = samples.map((p) => top(p));
const baseTop1 = base.map((r) => r[0]?.cityId);
const baseTop3 = base.map((r) => r.slice(0, 3).map((x) => x.cityId));

// --- 1. Score distribution & reachability ---
h("1. スコア分布と到達可能性");
out.push(
  `無作為な回答 ${N} 件（各設問の選択肢と重要度を一様に抽出、seed ${SEED}）で全都市を採点した。` +
    `期待値は 1 都市あたり 1 位 ${pct(1 / k.cities.length)}・上位 3 位 ${pct(3 / k.cities.length)}。`,
  "",
);
const cnt1 = new Map<string, number>();
const cnt3 = new Map<string, number>();
const totals = new Map<string, number[]>();
for (const [i, r] of base.entries()) {
  if (baseTop1[i]) cnt1.set(baseTop1[i]!, (cnt1.get(baseTop1[i]!) ?? 0) + 1);
  for (const id of baseTop3[i]) cnt3.set(id, (cnt3.get(id) ?? 0) + 1);
  for (const x of r) totals.set(x.cityId, [...(totals.get(x.cityId) ?? []), x.total]);
}
const rows1 = k.cities
  .map((c) => {
    const ts = (totals.get(c.id) ?? []).toSorted((a, b) => a - b);
    return {
      c,
      p1: (cnt1.get(c.id) ?? 0) / N,
      p3: (cnt3.get(c.id) ?? 0) / N,
      med: ts.length ? quantile(ts, 0.5) : NaN,
      q10: ts.length ? quantile(ts, 0.1) : NaN,
      q90: ts.length ? quantile(ts, 0.9) : NaN,
      ranked: ts.length / N,
    };
  })
  .toSorted((a, b) => b.p1 - a.p1 || b.p3 - a.p3);
table(
  ["都市", "地域", "1 位率", "上位 3 位率", "スコア中央値", "q10–q90", "順位対象率"],
  rows1.map((r) => [
    r.c.nameJa,
    r.c.region,
    pct(r.p1),
    pct(r.p3),
    f1(r.med),
    `${f1(r.q10)}–${f1(r.q90)}`,
    pct(r.ranked),
  ]),
);
const never = rows1.filter((r) => r.p3 === 0).map((r) => r.c.nameJa);
const maxP1 = rows1[0];
const p1s = rows1.map((r) => r.p1).toSorted((a, b) => a - b);
const gini =
  p1s.reduce((acc, x, i) => acc + (2 * (i + 1) - p1s.length - 1) * x, 0) /
  (p1s.length * p1s.reduce((a, b) => a + b, 0));
out.push(
  "",
  `- 1 位率の最大: ${maxP1.c.nameJa} ${pct(maxP1.p1)}（期待値の ${f1(maxP1.p1 * k.cities.length)} 倍）。1 位率のジニ係数 ${gini.toFixed(2)}。`,
  `- 一度も上位 3 位に入らない都市（${never.length}）: ${never.join("、") || "なし"}`,
);
const gaps = base
  .filter((r) => r.length > 1)
  .map((r) => r[0].total - r[1].total)
  .toSorted((a, b) => a - b);
out.push(
  `- 1 位と 2 位の差: 中央値 ${f1(quantile(gaps, 0.5))} 点、差が 1 点未満の割合 ${pct(gaps.filter((g) => g < 1).length / gaps.length)}。`,
);

// --- 2. Regional balance ---
h("2. 地域ごとの偏り");
const regions = [...new Set(k.cities.map((c) => c.region))].toSorted();
table(
  ["地域", "都市数の割合", "1 位の割合", "比"],
  regions.map((rg) => {
    const share = k.cities.filter((c) => c.region === rg).length / k.cities.length;
    const won = baseTop1.filter((id) => id && regionOf.get(id) === rg).length / N;
    return [rg, pct(share), pct(won), f1(won / share)];
  }),
);

// --- 3. Normalisation sensitivity ---
h("3. 正規化の対象都市への依存");
out.push(
  "方向型（多いほど良い／少ないほど良い）の指標は、人口 100 万人以上の全都市圏（" +
    `${k.reference.set.match(/\((\d+)\)/)?.[1] ?? "?"}）での百分位を 0〜1 にしている（本番方式）。` +
    "対象都市だけで作るスケールと比べ、さらに対象都市の 20% を無作為に除いた集合でスケールを作り直したとき（ジャックナイフ、20 回）の変化を見た。" +
    "本番方式は対象都市に依存しないため、ジャックナイフでも結果は変わらない（下表の最終行で確認）。" +
    "比較は「本番方式の 1 位が変わらない割合」と「上位 3 都市の Jaccard 係数の平均」。",
  "",
);
const compare = (label: string, rankFn: (p: Preference[], i: number) => string[]) => {
  let same1 = 0;
  let jac = 0;
  for (const [i, p] of samples.entries()) {
    const r = rankFn(p, i);
    if (r[0] === baseTop1[i]) same1++;
    jac += jaccard(baseTop3[i], r.slice(0, 3));
  }
  return [label, pct(same1 / N), (jac / N).toFixed(2)];
};
const targetCdf = (cities: City[]): Scales =>
  new Map(
    [...buildScales(k, cities, [0, 1])].map(([key]) => {
      const m = k.metrics.find((x) => x.key === key)!;
      const vs = cities
        .map((c) => c.metrics[key]?.value)
        .filter((v): v is number => v != null)
        .map((v) => (m.transform === "log10" ? Math.log10(v) : v))
        .toSorted((a, b) => a - b);
      return [key, { type: "cdf" as const, levels: k.reference.levels, quantiles: k.reference.levels.map((q) => quantile(vs, q)) }];
    }),
  );
const rowsN: string[][] = [
  compare("対象都市の q10–q90 で線形（P1 方式）", (p) => top(p, { scales: buildScales(k) }).map((x) => x.cityId)),
  compare("対象都市の min–max で線形", (p) => top(p, { scales: buildScales(k, k.cities, [0, 1]) }).map((x) => x.cityId)),
  compare("対象都市の百分位", (p) => top(p, { scales: targetCdf(k.cities) }).map((x) => x.cityId)),
];
const jack = Array.from({ length: 20 }, () => k.cities.filter(() => rand() >= 0.2));
const jackTarget = jack.map((cs) => targetCdf(cs));
rowsN.push(
  compare("対象都市の百分位・20% 除外 ×20", (p, i) => top(p, { scales: jackTarget[i % 20] }).map((x) => x.cityId)),
);
table(["スケール", "1 位不変", "上位 3 の Jaccard"], rowsN);
// Production scales do not depend on the target set: removing cities must not reorder the remaining ones.
let invariant = 0;
for (const [i, p] of samples.entries()) {
  const sub = jack[i % 20];
  const keep = new Set(sub.map((c) => c.id));
  const r = top(p, {}, { ...k, cities: sub }).map((x) => x.cityId);
  const b = base[i].map((x) => x.cityId).filter((id) => keep.has(id));
  if (r.join() === b.join()) invariant++;
}
out.push(
  "",
  `- 本番方式で対象都市の 20% を除いたとき、残った都市の順位が完全に一致した割合: ${pct(invariant / N)}（スケールが対象都市に依存しないことの確認）。`,
);

// --- 4. Weight robustness ---
h("4. 重みの変更への頑健性");
const perturb = (p: Preference[], sd: number) => p.map((x) => ({ ...x, weight: x.weight * Math.exp(sd * gauss()) }));
function gauss() {
  const u = Math.max(rand(), 1e-12);
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * rand());
}
table(
  ["変更", "1 位不変", "上位 3 の Jaccard"],
  [
    compare("全重みに ±10% 程度の対数正規ノイズ", (p) => top(perturb(p, 0.1)).map((x) => x.cityId)),
    compare("全重みに ±25% 程度の対数正規ノイズ", (p) => top(perturb(p, 0.25)).map((x) => x.cityId)),
    compare("重要度を無視（重み 0 以外を 1 に）", (p) =>
      top(p.map((x) => ({ ...x, weight: x.weight > 0 ? 1 : 0 }))).map((x) => x.cityId),
    ),
  ],
);
out.push("", "指標を 1 つ除いたとき（その指標の重みを 0）:", "");
table(
  ["除いた指標", "1 位不変", "上位 3 の Jaccard"],
  k.metrics.map((m) =>
    compare(m.label, (p) => top(p.map((x) => (x.metric === m.key ? { ...x, weight: 0 } : x))).map((x) => x.cityId)),
  ),
);

// --- 5. Missing-data handling ---
h("5. 欠損の扱いへの頑健性");
const missingRate = (m: string) => k.cities.filter((c) => c.metrics[m]?.value == null).length / k.cities.length;
table(
  ["指標", "欠損率"],
  k.metrics.map((m) => [m.label, pct(missingRate(m.key))]),
);
out.push("");
const medianImputed: Knowledge = {
  ...k,
  cities: k.cities.map((c): City => ({
    ...c,
    metrics: Object.fromEntries(
      Object.entries(c.metrics).map(([key, v]) => {
        if (v.value != null) return [key, v];
        const vs = k.cities
          .map((x) => x.metrics[key]?.value)
          .filter((x): x is number => x != null)
          .toSorted((a, b) => a - b);
        return [key, { ...v, value: vs.length ? quantile(vs, 0.5) : null, quality: "imputed" as const }];
      }),
    ),
  })),
};
table(
  ["欠損の扱い", "1 位不変", "上位 3 の Jaccard"],
  [
    compare("充足率の下限なし（0）", (p) => top(p, { minCoverage: 0 }).map((x) => x.cityId)),
    compare("充足率の下限 1.0（欠損のある都市は除外）", (p) => top(p, { minCoverage: 1 }).map((x) => x.cityId)),
    compare("中央値で補完（比較用。本番では使わない）", (p) =>
      top(p, {}, medianImputed).map((x) => x.cityId),
    ),
  ],
);

// --- 6. Personas ---
h("6. 回答パターン別の結果");
out.push("典型的な好みを固定した回答で、上位 5 都市とスコアを確認した。回答は `scripts/personas.ts` に定義。", "");
const { PERSONAS } = await import("./personas.ts");
for (const persona of PERSONAS) {
  const prefs = toPreferences(k.questions, persona.answers);
  const r = top(prefs);
  out.push(
    `- **${persona.label}**: ` +
      r
        .slice(0, 5)
        .map((x) => `${nameOf.get(x.cityId)} ${f1(x.total)}`)
        .join(" / "),
  );
}

const header = [
  "---",
  "type: Validation Report",
  "title: スコアリングの検証（実データ）",
  `description: データ版 ${k.dataVersion}・モデル ${k.modelVersion} での分布・頑健性・偏りの検証結果。`,
  "status: generated",
  "tags: [report, validation]",
  `data_version: ${k.dataVersion}`,
  `model_version: ${k.modelVersion}`,
  `samples: ${N}`,
  `seed: ${SEED}`,
  "---",
  "",
  "# スコアリングの検証",
  "",
  `データ版 \`${k.dataVersion}\`、モデル \`${k.modelVersion}\`、${k.cities.length} 都市 × ${k.metrics.length} 指標、設問 ${k.questions.length}。` +
    "`pnpm validate` が生成する。手で編集しない。",
];
writeFileSync("knowledge/reports/validation.md", `${[...header, ...out].join("\n")}\n`);
console.log(`✓ knowledge/reports/validation.md (${N} samples)`);
