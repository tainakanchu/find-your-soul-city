import {
  rankWords,
  refScales,
  KIND_LABEL,
  QUALITY_LABEL,
  formatValue,
  formatYear,
  knowledge,
  metricByKey,
  sourceById,
  roundBounded,
} from "../data.ts";
import type { City } from "../model/types.ts";
import { fit, type AxisScore } from "../scoring/score.ts";
import { reportUrl } from "../site.ts";

/** One axis: city value, your ideal or direction, distribution across all cities, and provenance. */
export function Evidence({ axis, city }: { axis: AxisScore; city: City }) {
  const m = metricByKey.get(axis.metric)!;
  const mv = city.metrics[axis.metric];
  const source = sourceById.get(mv.sourceId) ?? sourceById.get(m.sourceId);
  const t = (v: number) => (m.transform === "log10" ? Math.log10(v) : v);
  const all = knowledge.cities
    .map((c) => c.metrics[axis.metric]?.value)
    .filter((v): v is number => v != null)
    .map(t);
  const lo = Math.min(...all, ...(axis.ideal === undefined ? [] : [t(axis.ideal)]));
  const hi = Math.max(...all, ...(axis.ideal === undefined ? [] : [t(axis.ideal)]));
  const pos = (v: number) => `${((t(v) - lo) / (hi - lo || 1)) * 100}%`;
  const missing = mv.value === null;

  return (
    <details className="evidence">
      <summary>
        <span>{m.label}</span>
        <span className="fit">{axis.fit === null ? "対象外" : roundBounded(axis.fit * 100)}</span>
      </summary>
      <dl>
        <dt>{city.nameJa}</dt>
        <dd>
          {missing ? (
            <>
              <span className="missing">{QUALITY_LABEL.missing}</span>
              {mv.reason && <>（{mv.reason}）</>}
            </>
          ) : (
            formatValue(mv.value, m.unit)
          )}
        </dd>
        {m.kind === "ideal" ? (
          axis.ideal !== undefined && (
            <>
              <dt>あなたの理想</dt>
              <dd>{formatValue(axis.ideal, m.unit)}</dd>
            </>
          )
        ) : (
          <>
            <dt>向き</dt>
            <dd>{KIND_LABEL[m.kind]}</dd>
            {axis.fit !== null && (
              <>
                {!missing && (
                  <>
                    <dt>位置</dt>
                    <dd>{rankWords(m.kind, fit(m, mv.value!, undefined, refScales))}</dd>
                  </>
                )}
                <dt>十分な水準</dt>
                <dd>
                  {(knowledge.directionalTargets[String(axis.weight)] ?? 1) < 1
                    ? `参照集合の上位 ${Math.round((1 - knowledge.directionalTargets[String(axis.weight)]) * 100)}% 以内なら満点`
                    : "多いほど良い（上限なし）"}
                </dd>
              </>
            )}
          </>
        )}
        <dt>重み</dt>
        <dd>{axis.weight}</dd>
        <dt>出典</dt>
        <dd>{source?.title ?? mv.sourceId}</dd>
        <dt>データの種類</dt>
        <dd>{QUALITY_LABEL[mv.quality]}</dd>
        <dt>年・期間</dt>
        <dd>{mv.year === null ? m.period : formatYear(mv.year)}</dd>
        <dt>対象範囲</dt>
        <dd>{m.geography}</dd>
        <dt>算出方法</dt>
        <dd>{m.method}</dd>
      </dl>
      {m.caveat && <p className="caveat">注意: {m.caveat}</p>}
      <div
        className="strip"
        role="img"
        aria-label={`${all.length} 都市の分布${m.transform === "log10" ? "（対数目盛）" : ""}`}
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
        縦線は値のある {all.length} 都市、太線は{city.nameJa}
        {axis.ideal !== undefined && "、丸はあなたの理想"}
        {m.transform === "log10" && "（対数目盛）"}
      </p>
      <p className="report">
        <a
          href={reportUrl({
            cityId: city.id,
            metric: m.key,
            value: missing ? "missing" : formatValue(mv.value, m.unit),
            dataVersion: knowledge.dataVersion,
            modelVersion: knowledge.modelVersion,
          })}
          target="_blank"
          rel="noreferrer"
        >
          この数値の誤りを報告する
        </a>
        （GitHub。回答の内容は送られません）
      </p>
    </details>
  );
}
