/** Public identity of the site, shown on the About page and used for report links. */
export const SITE = {
  operator: "tainakanchu",
  url: "https://tainakanchu.github.io/find-your-soul-city/",
  repo: "https://github.com/tainakanchu/find-your-soul-city",
} as const;

/** Prefilled GitHub issue (form `data-error.yml`) for a suspected data error. Never includes the user's answers. */
export function reportUrl(p: {
  cityId: string;
  metric: string;
  value: string;
  dataVersion: string;
  modelVersion: string;
}) {
  const q = new URLSearchParams({
    template: "data-error.yml",
    title: `[data] ${p.cityId} / ${p.metric}`,
    city: p.cityId,
    metric: p.metric,
    value: p.value,
    version: `data ${p.dataVersion} / model ${p.modelVersion}`,
  });
  return `${SITE.repo}/issues/new?${q.toString()}`;
}
