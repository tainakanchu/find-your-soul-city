import { knowledge } from "../data.ts";
import { WorldPlot } from "./WorldPlot.tsx";

export function Intro({ onStart, onAbout }: { onStart: () => void; onAbout: () => void }) {
  return (
    <section className="intro">
      <h1>
        生まれた場所と、
        <br />
        心が帰る場所は、
        <br />
        同じとは限らない。
      </h1>
      <WorldPlot label={`対象の ${knowledge.cities.length} 都市の位置`} />
      <p className="lede">
        {knowledge.questions.length} の質問に答えると、世界の {knowledge.cities.length}{" "}
        都市から、気候・街の密度・移動のしやすさの好みに合う場所を探します。所要時間は 3 分ほど。
      </p>
      <p className="note">
        結果は都市の統計とあなたの回答の距離から計算した独自の適合度で、幸福度や移住の成功確率ではありません。回答はこの端末の外に送信しません。
      </p>
      <div className="actions">
        <button type="button" className="primary" onClick={onStart}>
          診断をはじめる
        </button>
        <button type="button" className="link" onClick={onAbout}>
          データと計算方法
        </button>
      </div>
    </section>
  );
}
