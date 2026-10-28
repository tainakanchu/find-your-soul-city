export const QUALITY_ORDER = ["placeholder", "imputed", "estimated", "observed"] as const;
export type Quality = (typeof QUALITY_ORDER)[number] | "missing";

export interface MetricValue {
  value: number | null;
  quality: Quality;
  sourceId: string;
  year: number | null;
}

export interface City {
  id: string;
  nameJa: string;
  nameEn: string;
  country: string;
  lat: number;
  lon: number;
  metrics: Record<string, MetricValue>;
}

export interface Metric {
  key: string;
  label: string;
  unit: string;
  kind: "ideal" | "higher_better";
  transform: "linear" | "log10";
  tolerance: number | null;
  sourceId: string;
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
  url: string | null;
  licenseStatus: string;
}

export interface Knowledge {
  modelVersion: string;
  minCoverage: number;
  dataVersion: string;
  metrics: Metric[];
  cities: City[];
  questions: Question[];
  sources: Source[];
}
