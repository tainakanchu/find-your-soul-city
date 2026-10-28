import { QUALITY_LABEL, formatValue, knowledge, metricByKey, sourceById } from "../data.ts";
import type { City } from "../model/types.ts";
import type { AxisScore } from "../scoring/score.ts";

/** One axis: city value, your ideal, distribution across all cities, and provenance. */
export function Evidence({ axis, city }: { axis: AxisScore; city: City }) {
  const m = metricByKey.get(axis.metric)!;
  const mv = city.metrics[axis.metric];
  const source = sourceById.get(mv.sourceId);
  const planned = sourceById.get(m.sourceId);
  const t = (v: number) => (m.transform === "log10" ? Math.log10(v) : v);
  const all = knowledge.cities
    .map((c) => c.metrics[axis.metric]?.value)
    .filter((v): v is number => v != null)
    .map(t);
  const lo = Math.min(...all, ...(axis.ideal === undefined ? [] : [t(axis.ideal)]));
  const hi = Math.max(...all, ...(axis.ideal === undefined ? [] : [t(axis.ideal)]));
  const pos = (v: number) => `${((t(v) - lo) / (hi - lo || 1)) * 100}%`;

  return (
    <details className="evidence">
      <summary>
        <span>{m.label}</span>
        <span className="fit">{axis.fit === null ? "対象外" : `${Math.round(axis.fit * 100)}`}</span>
      </summary>
      <dl>
        <dt>{city.nameJa}</dt>
        <dd>{formatValue(mv.value, m.unit)}</dd>
        {axis.ideal !== undefined && (
          <>
            <dt>あなたの理想</dt>
            <dd>{formatValue(axis.ideal, m.unit)}</dd>
          </>
        )}
        <dt>重み</dt>
        <dd>{axis.weight}</dd>
        <dt>出典</dt>
        <dd>
          {source?.title ?? mv.sourceId}（{QUALITY_LABEL[mv.quality]}
          {mv.year === null ? "" : `、${mv.year}年`}）
          {planned && planned.id !== mv.sourceId && <>。実データの予定: {planned.title}</>}
        </dd>
      </dl>
      <div
        className="strip"
        role="img"
        aria-label={`${knowledge.cities.length} 都市の分布${m.transform === "log10" ? "（対数目盛）" : ""}`}
      >
        {knowledge.cities.map((c) => {
          const v = c.metrics[axis.metric]?.value;
          return v == null ? null : (
            <span key={c.id} className={c.id === city.id ? "tick self" : "tick"} style={{ left: pos(v) }} />
          );
        })}
        {axis.ideal !== undefined && <span className="ideal" style={{ left: pos(axis.ideal) }} />}
      </div>
      <p className="legend">
        縦線は各都市、太線は{city.nameJa}
        {axis.ideal !== undefined && "、丸はあなたの理想"}
        {m.transform === "log10" && "（対数目盛）"}
      </p>
    </details>
  );
}
