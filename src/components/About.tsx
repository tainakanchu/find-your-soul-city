import { KIND_LABEL, knowledge, sourceById } from "../data.ts";

const KIND_TEXT = { ideal: "理想に近いほど良い", ...KIND_LABEL } as const;

export function About({ onBack }: { onBack: () => void }) {
  const pct = Math.round(knowledge.minCoverage * 100);
  return (
    <section className="about">
      <h1>データと計算方法</h1>
      <h2>計算のしかた</h2>
      <p>条件ごとに 0〜100 の点を付け、あなたが答えた重みで平均したものが適合度です。点の付け方は 2 通りあります。</p>
      <ul>
        <li>
          気温や密度のように「ちょうどいい値」がある条件（理想型）:
          あなたの理想値からの距離を、その指標ごとに決めた許容幅で割り、ガウス分布の形で点にします。理想と同じなら
          100、離れるほど 0 に近づきます。密度・降水量・人口は桁で比べるため、対数で距離を測ります。
        </li>
        <li>
          緑や交通のように「多いほど良い」「少ないほど良い」条件: 人口 100
          万人以上の世界の都市圏（参照集合）での分布のうち、その値が下から何割に当たるかを点にします（少ないほど良い条件は反転）。参照集合は、このアプリの
          {knowledge.cities.length} 都市とは別に固定したものです。
        </li>
      </ul>
      <p>
        データがない条件は 0
        点にせず、その条件を外して重みを再配分します。重みを付けた条件のうち、データがある条件の重みの割合が {pct}%
        に満たない都市は、順位から外します。
      </p>
      <p>
        データ品質の表示は、その都市の計算に使った値のうち最も低いものです（低い順に
        補完・推定・実測）。安定度は、重みを 1 項目ずつ ±10% 動かして計算し直し、1
        位が変わらなかった割合です。同じ回答・同じデータ版なら、結果は毎回同じになります。
      </p>
      <p>
        この適合度は、明示した好みのモデルに基づく独自の指標です。住みやすさや幸福度、移住の成功確率を表すものではありません。
      </p>

      <h2>都市の範囲</h2>
      <p>
        ここでの都市は行政区域ではなく、GHS-UCDB
        の都市圏（連続して市街化した範囲）です。たとえば「東京」には横浜・さいたま・千葉が、「大阪」には神戸・京都が含まれます。
      </p>

      <h2>指標</h2>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th scope="col">指標</th>
              <th scope="col">単位</th>
              <th scope="col">期間</th>
              <th scope="col">出典</th>
              <th scope="col">種類</th>
            </tr>
          </thead>
          <tbody>
            {knowledge.metrics.map((m) => (
              <tr key={m.key}>
                <td>{m.label}</td>
                <td>{m.unit}</td>
                <td>{m.period}</td>
                <td>{sourceById.get(m.sourceId)?.title ?? m.sourceId}</td>
                <td>{KIND_TEXT[m.kind]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h2>データ提供元</h2>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th scope="col">提供元</th>
              <th scope="col">版</th>
              <th scope="col">ライセンス</th>
            </tr>
          </thead>
          <tbody>
            {knowledge.sources.map((s) => (
              <tr key={s.id}>
                <td>
                  <a href={s.url}>{s.title}</a>
                </td>
                <td>{s.version}</td>
                <td>
                  <a href={s.licenseUrl}>{s.license}</a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <h3>帰属表示</h3>
      <ul className="attribution">
        {knowledge.sources.map((s) => (
          <li key={s.id}>
            {s.title}: {s.attribution}
          </li>
        ))}
      </ul>

      <h2>データのライセンス</h2>
      <p>
        都市ごとの指標データ一式は ODbL 1.0 で提供します（ITDP Atlas の share-alike 条件による）。Based on OpenStreetMap
        data © OpenStreetMap contributors.
      </p>

      <h2>プライバシー</h2>
      <p>回答はブラウザの中だけで計算し、どこにも送信・保存しません。ページを閉じると消えます。</p>
      <div className="actions">
        <button type="button" className="primary" onClick={onBack}>
          戻る
        </button>
      </div>
      <p className="version">
        model {knowledge.modelVersion} / data {knowledge.dataVersion}
      </p>
    </section>
  );
}
