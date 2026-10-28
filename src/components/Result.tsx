import { useMemo } from "react";
import {
  cityById,
  formatCoord,
  formatValue,
  formatYear,
  placeLabel,
  knowledge,
  metricByKey,
  QUALITY_LABEL,
  roundBounded,
  sourceById,
  stabilityWords,
} from "../data.ts";
import { explain, rank, stability, type AxisScore, type Preference } from "../scoring/score.ts";
import { Evidence } from "./Evidence.tsx";
import { Share } from "./Share.tsx";
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
  const missingAxes = used.filter((a) => a.value === null);
  const gap = ranked[1] ? first.total - ranked[1].total : null;
  // Which observation years / periods this result rests on, per source (they differ, see each metric).
  const periods = [
    ...new Map(
      used
        .filter((a) => a.value !== null)
        .map((a) => {
          const mv = city.metrics[a.metric];
          const src = sourceById.get(mv.sourceId)?.title ?? mv.sourceId;
          return [src, `${src}: ${formatYear(mv.year)}`] as const;
        }),
    ).values(),
  ];

  return (
    <section className="result">
      <p className="kicker">あなたの魂の故郷は</p>
      <h1 className="city">{city.nameEn}</h1>
      <p className="where">
        {placeLabel(city)} {formatCoord(city.lat, city.lon)}
      </p>
      <p className="summary">
        適合度は {roundBounded(first.total)} / 100。{stabilityWords(stable)}（重みを 1 項目ずつ ±10% 動かしても、
        {roundBounded(stable * 100)}% の条件で 1 位のまま）。使ったデータの品質は、最も低いもので「
        {QUALITY_LABEL[first.quality]}」です。
        {gap !== null && gap < 2 && <> 2 位との差は {gap.toFixed(1)} 点で、僅差です。</>}
      </p>
      <p className="note">
        適合度は回答と統計の近さを表す独自の指標で、住みやすさや幸福度の評価ではありません。「魂の故郷」は遊びの呼び名で、占いや前世、あなたとこの街の実際の縁を示すものではありません。順位は都市の優劣ではなく、あなたの答えとの近さの順です。
      </p>
      {missingAxes.length > 0 && (
        <p className="note">
          {city.nameJa}は次の条件のデータがないため、これらを除いて計算しています:{" "}
          {missingAxes.map((a) => metricByKey.get(a.metric)!.label).join("、")}（理由は根拠欄に記載）。
          欠けた条件が最も合わなかった場合から最も合った場合まで、適合度は {roundBounded(first.bounds[0])}〜
          {roundBounded(first.bounds[1])} の幅があります。
          {ranked[1] && first.bounds[0] < ranked[1].total && <>この幅の中では 2 位以下と入れ替わる可能性があります。</>}
        </p>
      )}

      {periods.length > 0 && (
        <p className="note">
          使ったデータの時期はソースごとに違います。{periods.join("、")}。
          {used.some((a) => a.metric === "urban_pop" || a.metric === "density_weighted") &&
            "人口は国連の推計に合わせた 2025 年の推定値です。"}
        </p>
      )}

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
              <span className="score">
                {roundBounded(r.total)}
                {r.coverage < 1 && (
                  <span className="muted">
                    {" "}
                    （欠損あり {roundBounded(r.bounds[0])}〜{roundBounded(r.bounds[1])}）
                  </span>
                )}
              </span>
            </li>
          );
        })}
      </ol>

      <Share city={city} score={roundBounded(first.total)} />

      <h2>根拠</h2>
      <p className="muted">数字は{city.nameJa}のこの条件での適合度（0〜100）。重みの大きい順。</p>
      {used.map((a) => (
        <Evidence key={a.metric} axis={a} city={city} />
      ))}
      {insufficient.length > 0 && <p className="muted">データ不足で比較から外した都市: {insufficient.length}</p>}

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
