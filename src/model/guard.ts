/**
 * Release guard: the app must never score with placeholder (made-up) data.
 * Used by scripts/knowledge.ts (bundle build), the Vite production build, and tests.
 */
const ALLOWED_QUALITIES = new Set(["observed", "estimated", "imputed", "missing"]);

interface Loose {
  cities?: { id?: string; metrics?: Record<string, { quality?: string; sourceId?: string; value?: unknown }> }[];
  sources?: { id?: string; licenseStatus?: string }[];
}

/** Returns one message per offending value; empty when the data is releasable. */
export function findPlaceholders(k: Loose): string[] {
  const out: string[] = [];
  const sources = new Set((k.sources ?? []).map((s) => s.id));
  for (const c of k.cities ?? []) {
    for (const [key, v] of Object.entries(c.metrics ?? {})) {
      const where = `${c.id}.${key}`;
      if (!v.quality || !ALLOWED_QUALITIES.has(v.quality))
        out.push(`${where}: quality "${v.quality}" is not real data`);
      if (/placeholder|demo/i.test(v.sourceId ?? "")) out.push(`${where}: source "${v.sourceId}" is a placeholder`);
      if (v.value != null && !sources.has(v.sourceId)) out.push(`${where}: source "${v.sourceId}" is not registered`);
    }
  }
  return out;
}
