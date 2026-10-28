import { useMemo } from "react";
import { cityById, formatCoord, formatValue, knowledge, metricByKey, QUALITY_LABEL } from "../data.ts";
import { explain, rank, stability, type AxisScore, type Preference } from "../scoring/score.ts";
import { Evidence } from "./Evidence.tsx";
import { WorldPlot } from "./WorldPlot.tsx";

function Reason({ axis }: { axis: AxisScore }) {
  const m = metricByKey.get(axis.metric)!;
  return (
    <li>
      {m.label} {formatValue(axis.value, m.unit)}
      {axis.ideal !== undefined && <span className="muted">（理想 {formatValue(axis.ideal, m.unit)}）</span>}
    </li>
  );
}

export function Result({ prefs, onRetry, onAbout }: { prefs: Preference[]; onRetry: () => void; onAbout: () => void }) {
  const { ranked, insufficient } = useMemo(() => rank(knowledge, prefs), [prefs]);
  const stable = useMemo(() => stability(knowledge, prefs), [prefs]);
  const first = ranked[0];

  if (!first) {
    return (
      <section className="result">
        <p>比べられる都市がありません。すべての条件が「気にしない」になっていないか確認してください。</p>
        <button type="button" className="primary" onClick={onRetry}>
          もう一度答える
        </button>
      </section>
    );
  }

  const city = cityById.get(first.cityId)!;
  const { matches, mismatches } = explain(first);
  const top3 = ranked.slice(0, 3);
  const used = first.axes.filter((a) => a.weight > 0).toSorted((a, b) => b.weight - a.weight);

  return (
    <section className="result">
      <p className="kicker">あなたの魂の故郷は</p>
      <h1 className="city">{city.nameEn}</h1>
      <p className="where">
        {city.nameJa}（{city.country}） {formatCoord(city.lat, city.lon)}
      </p>
      <p className="summary">
        適合度は {Math.round(first.total)} / 100。重みを 1 項目ずつ ±10% 動かしても、{Math.round(stable * 100)}%
        の条件で 1 位のままでした。データ品質は「{QUALITY_LABEL[first.quality]}」です。
      </p>

      <WorldPlot
        scores={new Map(ranked.map((r) => [r.cityId, r.total]))}
        pin={first.cityId}
        label={`適合度の地図。1 位 ${city.nameJa}`}
      />

      <div className="reasons">
        <div>
          <h2>合うところ</h2>
          {matches.length ? (
            <ul>
              {matches.map((a) => (
                <Reason key={a.metric} axis={a} />
              ))}
            </ul>
          ) : (
            <p className="muted">目立って合う条件はありません。</p>
          )}
        </div>
        <div>
          <h2>合わないところ</h2>
          {mismatches.length ? (
            <ul>
              {mismatches.map((a) => (
                <Reason key={a.metric} axis={a} />
              ))}
            </ul>
          ) : (
            <p className="muted">大きく外れる条件はありません。</p>
          )}
        </div>
      </div>

      <h2>上位の候補</h2>
      <ol className="ranking">
        {top3.map((r) => {
          const c = cityById.get(r.cityId)!;
          return (
            <li key={r.cityId}>
              <span className="name">{c.nameJa}</span>
              <span className="score">{Math.round(r.total)}</span>
            </li>
          );
        })}
      </ol>

      <h2>根拠</h2>
      <p className="muted">数字は{city.nameJa}のこの条件での適合度（0〜100）。重みの大きい順。</p>
      {used.map((a) => (
        <Evidence key={a.metric} axis={a} city={city} />
      ))}
      {insufficient.length > 0 && (
        <p className="muted">
          {insufficient.map((r) => cityById.get(r.cityId)!.nameJa).join("、")}
          は、あなたが重視した条件のデータが足りないため順位から外しています。
        </p>
      )}

      <div className="actions">
        <button type="button" className="primary" onClick={onRetry}>
          もう一度答える
        </button>
        <button type="button" className="link" onClick={onAbout}>
          データと計算方法
        </button>
      </div>
      <p className="version">
        model {knowledge.modelVersion} / data {knowledge.dataVersion}
      </p>
    </section>
  );
}
