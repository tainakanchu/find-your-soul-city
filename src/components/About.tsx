import { KIND_LABEL, knowledge, sourceById } from "../data.ts";
import { SITE } from "../site.ts";

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
          万人以上の世界の都市圏（参照集合）での分布のうち、その値が下から何割に当たるかを求めます（少ないほど良い条件は反転）。
          そのうえで「十分な水準」に届いていれば 100
          点とし、届かない分だけ下げます。十分な水準は「あると嬉しい」なら参照集合の真ん中（上位
          50%）、「絶対にほしい」なら上位 20% です。それより多くても点は増えません。参照集合は、このアプリの{" "}
          {knowledge.cities.length} 都市とは別に固定したものです。
        </li>
      </ul>
      <p>
        よく似た傾向の条件（たとえば「徒歩圏の医療・教育」と「文化施設」、「降水量」と「雲量」）を両方重視すると、同じことを二重に数えてしまいます。
        世界の大都市圏で順位の相関が強い（0.5 以上）組を両方重視したときは、その条件どうしで重みを分け合います。
      </p>
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

      <h2>結果の偏りについて</h2>
      <p>
        徒歩・自転車・公共交通・木・空気・文化の指標は、どれも同じ一部の都市（欧州の首都級やシンガポール）が世界の上位にいます。
        「多いほど良い」で比べると、少し重視しただけでもこれらの都市が毎回 1
        位になってしまうため、「十分な水準」を超えた分は点を増やさない計算にしています。
        それでも「絶対にほしい」を多く選ぶほど、これらの都市が上位に来やすくなります。気候と街の規模だけで比べると、地域の偏りはほとんどありません。
        徒歩圏の医療・教育は、OpenStreetMap への施設の登録が少ない地域で低く出ている可能性があります。詳しい数字は{" "}
        <a href={`${SITE.repo}/blob/HEAD/knowledge/reports/validation.md`}>検証レポート</a>にあります。
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
      <p>
        回答はブラウザの中だけで計算し、どこにも送信・保存しません。ページを閉じると消えます。アクセス解析も入れていません。
        「誤りを報告する」のリンクは GitHub に移動し、都市・指標・値・データ版だけを書き込みます。回答は含みません。
        結果の共有ボタンを押したときだけ、1
        位の都市名と適合度を選んだ共有先に渡します（回答は含みません）。フライト検索のリンクは Google
        フライトに都市名だけを渡します（提携やおすすめではありません）。
      </p>

      <h2>つくっている人</h2>
      <p>
        運営者 {SITE.operator} が、AI（Anthropic の
        Claude）と一緒につくっています。データの取得と計算のプログラム、説明文は AI
        と一緒に書き、何を採用するかは運営者が決めて確認しています。数値は AI
        が書いたものではなく、公開統計からプログラムで計算したものです。
      </p>
      <p>
        公式サイトは <a href={SITE.url}>{SITE.url}</a> だけです。コードとデータは <a href={SITE.repo}>GitHub</a>{" "}
        で公開しています（コード MIT、データ ODbL 1.0）。
      </p>
      <p>
        数値の誤り・不具合・ご意見は <a href={`${SITE.repo}/issues/new/choose`}>GitHub の Issue</a>{" "}
        で受け付けています。根拠欄の「この数値の誤りを報告する」から開くと、どの数値かが自動で入ります。
      </p>
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
