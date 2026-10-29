import { useState } from "react";
import type { City } from "../model/types.ts";
import { ogImagePath, shareText, shareUrl, xIntentUrl } from "../share.ts";

/** Share the result city and rounded score. Fixed text; the link is the city's share page and carries no answers. */
export function Share({ city, score }: { city: City; score: string }) {
  const [status, setStatus] = useState("");
  const text = shareText(city, score);
  const url = shareUrl(city.id);
  const canShare = typeof navigator !== "undefined" && typeof navigator.share === "function";

  const share = async () => {
    try {
      await navigator.share({ text, url });
    } catch {
      // Cancelled or refused by the browser: nothing was sent.
    }
  };
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(`${text}\n${url}`);
      setStatus("コピーしました");
      window.setTimeout(() => setStatus(""), 4000);
    } catch {
      setStatus("コピーできませんでした。上の文をそのまま選んでコピーしてください。");
    }
  };

  return (
    <section className="share" aria-labelledby="share-title">
      <h2 id="share-title">結果を共有する</h2>
      <p className="share-preview">
        {text}
        <br />
        <span className="muted">{url}</span>
      </p>
      <div className="share-buttons">
        {canShare && (
          <button type="button" onClick={share}>
            共有
          </button>
        )}
        <a href={xIntentUrl(text, url)} target="_blank" rel="noopener noreferrer">
          X に投稿
        </a>
        <button type="button" onClick={copy}>
          テキストとリンクをコピー
        </button>
        <a href={`${import.meta.env.BASE_URL}${ogImagePath(city.id)}`} download={`soul-city-${city.id}.png`}>
          画像を保存
        </a>
      </div>
      <p className="share-status" role="status" aria-live="polite">
        {status}
      </p>
      <p className="note">共有されるのは都市名と適合度だけで、回答は含まれません。</p>
    </section>
  );
}
