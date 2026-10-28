import { hasPlaceholder, knowledge } from "../data.ts";

const LICENSE_LABEL: Record<string, string> = {
  unverified: "利用条件 未確認",
  "not-applicable": "—",
};

export function About({ onBack }: { onBack: () => void }) {
  return (
    <section className="about">
      <h1>データと計算方法</h1>
      {hasPlaceholder && (
        <p className="callout">
          いまの都市データは、実データを取得する前に画面と計算を確かめるための仮の値です。実測ではないため、結果を実際の判断には使わないでください。
        </p>
      )}
      <h2>計算のしかた</h2>
      <p>
        気温や密度のように「ちょうどいい値」がある条件は、あなたの理想値との近さを 0〜100
        にします。徒歩圏の生活サービスや緑のように「多いほど良い」条件は、{knowledge.cities.length} 都市の中での位置を
        0〜100 にし、あなたが答えた重要度で重み付けします。
      </p>
      <p>
        データがない条件は 0 点にせず、その条件を外して計算します。重視した条件のデータが 4 分の 3
        に満たない都市は順位に入れません。同じ回答・同じデータ版なら、結果は毎回同じになります。
      </p>
      <p>この適合度は、明示した好みのモデルに基づく独自の指標です。幸福度や移住の成功確率を表すものではありません。</p>
      <h2>データ提供元</h2>
      <table>
        <thead>
          <tr>
            <th scope="col">提供元</th>
            <th scope="col">利用条件</th>
          </tr>
        </thead>
        <tbody>
          {knowledge.sources.map((s) => (
            <tr key={s.id}>
              <td>{s.url ? <a href={s.url}>{s.title}</a> : s.title}</td>
              <td>{LICENSE_LABEL[s.licenseStatus] ?? s.licenseStatus}</td>
            </tr>
          ))}
        </tbody>
      </table>
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
