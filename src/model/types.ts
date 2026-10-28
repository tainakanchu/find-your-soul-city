/** Worst → best. `missing` is not a quality of a value but its absence. */
export const QUALITY_ORDER = ["imputed", "estimated", "observed"] as const;
export type Quality = (typeof QUALITY_ORDER)[number] | "missing";

export interface MetricValue {
  value: number | null;
  quality: Quality;
  sourceId: string;
  /** Observation year, or "YYYY-YYYY" for a climatological period. */
  year: number | string | null;
  /** Why the value is missing (only when quality is missing). */
  reason?: string;
}

export interface City {
  id: string;
  nameJa: string;
  nameEn: string;
  country: string;
  region: string;
  lat: number;
  lon: number;
  boundary: { sourceId: string; id: number; areaKm2: number };
  metrics: Record<string, MetricValue>;
}

export interface Metric {
  key: string;
  label: string;
  unit: string;
  /** ideal: distance to the user's ideal. higher_better / lower_better: position in the reference distribution. */
  kind: "ideal" | "higher_better" | "lower_better";
  transform: "linear" | "log10";
  tolerance: number | null;
  sourceId: string;
  period: string;
  geography: string;
  method: string;
  caveat: string;
}

export interface QuestionOption {
  label: string;
  value: number;
}

export interface Question {
  id: string;
  order: number;
  metric: string;
  prompt: string;
  answerKind: "ideal" | "importance";
  importanceControl: boolean;
  options: QuestionOption[];
}

export interface Source {
  id: string;
  title: string;
  provider: string;
  url: string;
  version: string;
  license: string;
  licenseUrl: string;
  attribution: string;
  licenseStatus: "verified" | "restricted" | "unverified";
}

/** Quantiles of directional metrics over a fixed reference set of urban centres (not the target cities). */
export interface ReferenceDistribution {
  set: string;
  levels: number[];
  metrics: Record<string, { n: number; quantiles: number[] }>;
}

export interface Knowledge {
  modelVersion: string;
  minCoverage: number;
  dataVersion: string;
  metrics: Metric[];
  cities: City[];
  questions: Question[];
  sources: Source[];
  reference: ReferenceDistribution;
}
