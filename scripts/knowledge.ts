// OKF v0.2 bundle (knowledge/) -> conformance check, index.md generation, app JSON.
// Usage: node scripts/knowledge.ts <build|check>
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { parse } from "yaml";
import { findPlaceholders } from "../src/model/guard.ts";
import type { City, Knowledge, Metric, MetricValue, Question, Source } from "../src/model/types.ts";

const ROOT = "knowledge";
const OUT = "src/generated/knowledge.json";
const RESERVED = new Set(["index.md", "log.md"]);
const QUALITIES = new Set(["observed", "estimated", "imputed", "missing"]);
const KINDS = new Set(["ideal", "higher_better", "lower_better"]);
const LICENSE_STATUSES = new Set(["verified", "restricted", "unverified"]);

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

const sourceDocs = ofType("Data Source");
const sources: Source[] = sourceDocs
  .filter((d) => d.fm.adoption === "adopted")
  .map((d) => {
    const status = str(d, "license_status");
    if (!LICENSE_STATUSES.has(status)) fail(d.path, `unknown license_status ${status}`);
    // A source the app shows numbers from must have a checked licence that allows publication.
    if (status !== "verified") fail(d.path, `adopted source must have license_status: verified (is ${status})`);
    return {
      id: str(d, "source_id"),
      title: str(d, "title"),
      provider: str(d, "provider"),
      url: str(d, "resource"),
      version: str(d, "version"),
      license: str(d, "license"),
      licenseUrl: str(d, "license_url"),
      attribution: str(d, "attribution"),
      licenseStatus: status as Source["licenseStatus"],
    };
  });
const sourceIds = new Set(sources.map((s) => s.id));
const allSourceIds = new Set(sourceDocs.map((d) => String(d.fm.source_id)));

const metricDocs = ofType("Metric");
for (const d of metricDocs) {
  const a = d.fm.adoption;
  if (a !== "adopted" && a !== "rejected") fail(d.path, "`adoption` must be adopted or rejected");
  if (a === "rejected") str(d, "rejection_reason");
  if (!allSourceIds.has(String(d.fm.source))) fail(d.path, `unknown source ${String(d.fm.source)}`);
}
const metrics: Metric[] = metricDocs
  .filter((d) => d.fm.adoption === "adopted")
  .map((d) => {
    const kind = str(d, "kind");
    const transform = str(d, "transform");
    if (!KINDS.has(kind)) fail(d.path, `unknown kind ${kind}`);
    if (transform !== "linear" && transform !== "log10") fail(d.path, `unknown transform ${transform}`);
    if (kind === "ideal") num(d, "tolerance");
    const sourceId = str(d, "source");
    if (!sourceIds.has(sourceId)) fail(d.path, `adopted metric uses non-adopted source ${sourceId}`);
    return {
      key: str(d, "metric_key"),
      label: str(d, "title"),
      unit: str(d, "unit"),
      kind: kind as Metric["kind"],
      transform: transform as Metric["transform"],
      tolerance: typeof d.fm.tolerance === "number" ? d.fm.tolerance : null,
      sourceId,
      period: str(d, "period"),
      geography: str(d, "geography"),
      method: str(d, "method"),
      caveat: str(d, "caveat"),
    };
  });
const metricKeys = new Set(metrics.map((m) => m.key));
const allMetricKeys = new Set(metricDocs.map((d) => String(d.fm.metric_key)));

const placeDoc = docs.find((d) => d.fm.type === "Decision Record" && d.fm.country_names);
const countryNames = (placeDoc?.fm.country_names ?? {}) as Record<string, string>;
if (!placeDoc) fail(ROOT, "no Decision Record with country_names (knowledge/decisions/place-names.md)");

const cities: City[] = ofType("City").map((d) => {
  const raw = (d.fm.metrics ?? {}) as Record<string, Record<string, unknown>>;
  const values: Record<string, MetricValue> = {};
  for (const m of metrics) {
    const e = raw[m.key];
    if (!e) {
      fail(d.path, `metric ${m.key} not recorded (use quality: missing instead of omitting); run pnpm etl`);
      continue;
    }
    const quality = String(e.quality);
    const value = e.value === null ? null : Number(e.value);
    if (!QUALITIES.has(quality))
      fail(d.path, `${m.key}: quality "${quality}" is not allowed (placeholder data is banned)`);
    if ((quality === "missing") !== (value === null))
      fail(d.path, `${m.key}: value must be null iff quality is missing`);
    if (quality === "missing" && typeof e.reason !== "string") fail(d.path, `${m.key}: missing value needs a reason`);
    if (String(e.source) !== m.sourceId)
      fail(d.path, `${m.key}: source ${String(e.source)} ≠ metric source ${m.sourceId}`);
    if (value !== null && !Number.isFinite(value)) fail(d.path, `${m.key}: value is not finite`);
    values[m.key] = {
      value,
      quality: quality as MetricValue["quality"],
      sourceId: String(e.source),
      year: e.year == null ? null : typeof e.year === "number" ? e.year : String(e.year),
      ...(quality === "missing" ? { reason: String(e.reason) } : {}),
    };
  }
  for (const key of Object.keys(raw)) if (!allMetricKeys.has(key)) fail(d.path, `unknown metric ${key}`);
  const b = (d.fm.boundary ?? {}) as Fm;
  if (typeof b.id !== "number" || typeof b.area_km2 !== "number")
    fail(d.path, "boundary.id / boundary.area_km2 required");
  return {
    id: str(d, "city_id"),
    nameJa: str(d, "name_ja"),
    nameEn: str(d, "title"),
    country: str(d, "country"),
    countryName: (() => {
      const n = countryNames[String(d.fm.country)];
      if (!n) fail(d.path, `country ${String(d.fm.country)} has no display name in place-names.md`);
      return String(n);
    })(),
    region: str(d, "region"),
    lat: num(d, "lat"),
    lon: num(d, "lon"),
    boundary: { sourceId: String(b.source), id: Number(b.id), areaKm2: Number(b.area_km2) },
    metrics: values,
  };
});

const questions: Question[] = ofType("Question")
  .map((d) => {
    const metric = str(d, "metric");
    if (!metricKeys.has(metric)) fail(d.path, `metric ${metric} is not an adopted metric`);
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

const refDocs = ofType("Reference Distribution");
if (refDocs.length !== 1) fail(ROOT, `expected exactly 1 Reference Distribution, found ${refDocs.length}`);
const refDoc = refDocs[0];
const refLevels = Array.isArray(refDoc?.fm.levels) ? (refDoc.fm.levels as number[]) : [];
const refMetrics = (refDoc?.fm.metrics ?? {}) as Record<string, { n: number; quantiles: number[] }>;
for (const m of metrics) {
  if (m.kind === "ideal") continue;
  const r = refMetrics[m.key];
  if (!r) fail(refDoc?.path ?? ROOT, `no reference distribution for directional metric ${m.key}; run pnpm etl`);
  else if (r.quantiles.length !== refLevels.length || r.quantiles.some((q, i) => i > 0 && q < r.quantiles[i - 1]))
    fail(refDoc.path, `${m.key}: quantiles must be non-decreasing and match levels`);
}
const reference: Knowledge["reference"] = {
  set: refDoc ? str(refDoc, "reference_set") : "",
  levels: refLevels,
  metrics: Object.fromEntries(
    metrics
      .filter((m) => refMetrics[m.key])
      .map((m) => [m.key, { n: refMetrics[m.key].n, quantiles: refMetrics[m.key].quantiles }]),
  ),
};

const models = ofType("Model Specification");
if (models.length !== 1) fail(ROOT, `expected exactly 1 Model Specification, found ${models.length}`);
const model = models[0];

for (const [label, ids] of [
  ["city_id", cities.map((c) => c.id)],
  ["question_id", questions.map((q) => q.id)],
  ["metric_key", metricDocs.map((d) => String(d.fm.metric_key))],
  ["source_id", sourceDocs.map((d) => String(d.fm.source_id))],
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

const directionalTargets: Record<string, number> = Object.fromEntries(
  Object.entries((model?.fm.directional_targets ?? {}) as Record<string, unknown>).map(([w, v]) => {
    if (typeof v !== "number" || v <= 0 || v > 1) fail(model.path, `directional_targets.${w} must be in (0, 1]`);
    return [w, Number(v)];
  }),
);

const body = { metrics, cities, questions, sources, reference };
for (const msg of findPlaceholders(body)) fail(ROOT, msg);

if (errors.length) {
  console.error(errors.map((e) => `✗ ${e}`).join("\n"));
  process.exit(1);
}

const knowledge: Knowledge = {
  modelVersion: str(model, "model_version"),
  minCoverage: num(model, "min_coverage"),
  directionalTargets,
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
