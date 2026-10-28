// OKF v0.2 bundle (knowledge/) -> conformance check, index.md generation, app JSON.
// Usage: node scripts/knowledge.ts <build|check>
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { parse } from "yaml";
import type { City, Knowledge, Metric, MetricValue, Question, Source } from "../src/model/types.ts";

const ROOT = "knowledge";
const OUT = "src/generated/knowledge.json";
const RESERVED = new Set(["index.md", "log.md"]);
const QUALITIES = new Set(["observed", "estimated", "imputed", "placeholder", "missing"]);

type Fm = Record<string, unknown>;
interface Doc {
  path: string;
  fm: Fm;
}

const mode = process.argv[2];
if (mode !== "build" && mode !== "check") {
  console.error("usage: node scripts/knowledge.ts <build|check>");
  process.exit(2);
}

const errors: string[] = [];
const fail = (path: string, msg: string) => errors.push(`${path}: ${msg}`);

function walk(dir: string): string[] {
  return readdirSync(dir)
    .toSorted()
    .flatMap((name) => {
      const p = join(dir, name);
      return statSync(p).isDirectory() ? walk(p) : p.endsWith(".md") ? [p] : [];
    });
}

function frontmatter(path: string): Fm | null {
  const m = /^---\n([\s\S]*?)\n---\n/.exec(readFileSync(path, "utf8"));
  if (!m) return null;
  try {
    const fm = parse(m[1]) as unknown;
    return fm && typeof fm === "object" ? (fm as Fm) : null;
  } catch (e) {
    fail(path, `YAML parse error: ${(e as Error).message}`);
    return null;
  }
}

// --- 1. Conformance (OKF §11) ---
const files = walk(ROOT);
const docs: Doc[] = [];
for (const path of files) {
  const base = path.split("/").at(-1)!;
  if (RESERVED.has(base)) continue;
  const fm = frontmatter(path);
  if (!fm) fail(path, "missing or unparseable frontmatter");
  else if (typeof fm.type !== "string" || fm.type === "") fail(path, "missing non-empty `type`");
  else docs.push({ path, fm });
}
const rootIndex = frontmatter(join(ROOT, "index.md"));
if (rootIndex?.okf_version !== "0.2") fail(`${ROOT}/index.md`, 'expected okf_version: "0.2"');

// --- 2. App schema ---
const ofType = (t: string) => docs.filter((d) => d.fm.type === t);
const str = (d: Doc, k: string): string => {
  const v = d.fm[k];
  if (typeof v !== "string" || v === "") fail(d.path, `\`${k}\` must be a non-empty string`);
  return String(v);
};
const num = (d: Doc, k: string): number => {
  const v = d.fm[k];
  if (typeof v !== "number") fail(d.path, `\`${k}\` must be a number`);
  return Number(v);
};

const sources: Source[] = ofType("Data Source").map((d) => ({
  id: str(d, "source_id"),
  title: str(d, "title"),
  provider: str(d, "provider"),
  url: typeof d.fm.resource === "string" ? d.fm.resource : null,
  licenseStatus: str(d, "license_status"),
}));
const sourceIds = new Set(sources.map((s) => s.id));

const metricDocs = ofType("Metric");
const derived = new Map<string, string[]>();
const metrics: Metric[] = metricDocs.map((d) => {
  const key = str(d, "metric_key");
  const kind = str(d, "kind");
  const transform = str(d, "transform");
  if (kind !== "ideal" && kind !== "higher_better") fail(d.path, `unknown kind ${kind}`);
  if (transform !== "linear" && transform !== "log10") fail(d.path, `unknown transform ${transform}`);
  if (kind === "ideal") num(d, "tolerance");
  const sourceId = str(d, "planned_source");
  if (!sourceIds.has(sourceId)) fail(d.path, `unknown planned_source ${sourceId}`);
  if (Array.isArray(d.fm.derived_from)) derived.set(key, d.fm.derived_from.map(String));
  return {
    key,
    label: str(d, "title"),
    unit: str(d, "unit"),
    kind: kind as Metric["kind"],
    transform: transform as Metric["transform"],
    tolerance: typeof d.fm.tolerance === "number" ? d.fm.tolerance : null,
    sourceId,
  };
});
const metricKeys = new Set(metrics.map((m) => m.key));
const rawKeys = metrics.map((m) => m.key).filter((k) => !derived.has(k));

const worst = (vs: MetricValue[]): MetricValue["quality"] => {
  const order = ["missing", "placeholder", "imputed", "estimated", "observed"];
  return vs.map((v) => v.quality).toSorted((a, b) => order.indexOf(a) - order.indexOf(b))[0];
};

const cities: City[] = ofType("City").map((d) => {
  const raw = (d.fm.metrics ?? {}) as Record<string, Record<string, unknown>>;
  const values: Record<string, MetricValue> = {};
  for (const key of rawKeys) {
    const e = raw[key];
    if (!e) {
      fail(d.path, `metric ${key} not recorded (use quality: missing instead of omitting)`);
      continue;
    }
    const quality = String(e.quality);
    const value = e.value === null ? null : Number(e.value);
    if (!QUALITIES.has(quality)) fail(d.path, `${key}: unknown quality ${quality}`);
    if ((quality === "missing") !== (value === null)) fail(d.path, `${key}: value must be null iff quality is missing`);
    if (!sourceIds.has(String(e.source))) fail(d.path, `${key}: unknown source ${String(e.source)}`);
    values[key] = {
      value,
      quality: quality as MetricValue["quality"],
      sourceId: String(e.source),
      year: e.year == null ? null : Number(e.year),
    };
  }
  for (const key of Object.keys(raw)) if (!metricKeys.has(key)) fail(d.path, `unknown metric ${key}`);
  for (const [key, from] of derived) {
    const parts = from.map((k) => values[k]).filter(Boolean);
    const [a, b] = parts;
    const missing = parts.length !== 2 || a.value === null || b.value === null;
    values[key] = {
      value: missing ? null : Math.round((a.value! - b.value!) * 10) / 10,
      quality: missing ? "missing" : worst(parts),
      sourceId: a?.sourceId ?? "",
      year: a?.year ?? null,
    };
  }
  return {
    id: str(d, "city_id"),
    nameJa: str(d, "name_ja"),
    nameEn: str(d, "title"),
    country: str(d, "country"),
    lat: num(d, "lat"),
    lon: num(d, "lon"),
    metrics: values,
  };
});

const questions: Question[] = ofType("Question")
  .map((d) => {
    const metric = str(d, "metric");
    if (!metricKeys.has(metric)) fail(d.path, `unknown metric ${metric}`);
    const answerKind = str(d, "answer_kind");
    if (answerKind !== "ideal" && answerKind !== "importance") fail(d.path, `unknown answer_kind ${answerKind}`);
    const options = Array.isArray(d.fm.options) ? (d.fm.options as Fm[]) : [];
    if (options.length < 2) fail(d.path, "needs at least 2 options");
    return {
      id: str(d, "question_id"),
      order: num(d, "order"),
      metric,
      prompt: str(d, "title"),
      answerKind: answerKind as Question["answerKind"],
      importanceControl: d.fm.importance_control === true,
      options: options.map((o) => ({ label: String(o.label), value: Number(o.value) })),
    };
  })
  .toSorted((a, b) => a.order - b.order);

const models = ofType("Model Specification");
if (models.length !== 1) fail(ROOT, `expected exactly 1 Model Specification, found ${models.length}`);
const model = models[0];

for (const [label, ids] of [
  ["city_id", cities.map((c) => c.id)],
  ["question_id", questions.map((q) => q.id)],
  ["metric_key", [...metricKeys]],
  ["source_id", [...sourceIds]],
] as const) {
  const dup = ids.filter((id, i) => ids.indexOf(id) !== i);
  if (dup.length) fail(ROOT, `duplicate ${label}: ${dup.join(", ")}`);
}

// --- 3. index.md per subdirectory (OKF §8) ---
const indexes = new Map<string, string>();
for (const dir of new Set(docs.map((d) => dirname(d.path)))) {
  if (dir === ROOT) continue;
  const items = docs
    .filter((d) => dirname(d.path) === dir)
    .map((d) => `* [${String(d.fm.title ?? d.path)}](${relative(dir, d.path)}) - ${String(d.fm.description ?? "")}`);
  indexes.set(join(dir, "index.md"), `# ${dir.slice(ROOT.length + 1)}\n\n${items.join("\n")}\n`);
}

if (errors.length) {
  console.error(errors.map((e) => `✗ ${e}`).join("\n"));
  process.exit(1);
}

const body = { metrics, cities, questions, sources };
const knowledge: Knowledge = {
  modelVersion: str(model, "model_version"),
  minCoverage: num(model, "min_coverage"),
  dataVersion: createHash("sha256").update(JSON.stringify(body)).digest("hex").slice(0, 12),
  ...body,
};

if (mode === "check") {
  const stale = [...indexes].filter(([p, c]) => {
    try {
      return readFileSync(p, "utf8") !== c;
    } catch {
      return true;
    }
  });
  if (stale.length) {
    console.error(`✗ index.md is stale: ${stale.map(([p]) => p).join(", ")}\n  run: pnpm knowledge:build`);
    process.exit(1);
  }
} else {
  for (const [p, c] of indexes) writeFileSync(p, c);
  mkdirSync(dirname(OUT), { recursive: true });
  writeFileSync(OUT, `${JSON.stringify(knowledge, null, 2)}\n`);
}

console.log(
  `✓ ${docs.length} concepts (${cities.length} cities, ${metrics.length} metrics, ${questions.length} questions) data=${knowledge.dataVersion}`,
);
