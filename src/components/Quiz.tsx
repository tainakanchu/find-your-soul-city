import { useEffect, useState } from "react";
import { DEFAULT_IMPORTANCE, type Answer } from "../answers.ts";
import { knowledge } from "../data.ts";

const IMPORTANCE = [
  { label: "気にしない", value: 0, key: "q" },
  { label: "ふつう", value: 1, key: "w" },
  { label: "重要", value: 2, key: "e" },
];

/** Focus the i-th radio of a group (keyboard selection moves focus with it). */
function focusRadio(name: string, i: number) {
  const radios = document.querySelectorAll<HTMLInputElement>(`input[name="${name}"]`);
  radios[i]?.focus();
}

interface Props {
  answers: Record<string, Answer>;
  onAnswer: (id: string, a: Answer) => void;
  onDone: () => void;
  onExit: () => void;
}

export function Quiz({ answers, onAnswer, onDone, onExit }: Props) {
  const { questions } = knowledge;
  const [index, setIndex] = useState(0);
  const q = questions[index];
  const a = answers[q.id];
  const last = index === questions.length - 1;

  const set = (patch: Partial<Answer>) =>
    onAnswer(q.id, { choice: a?.choice, importance: a?.importance ?? DEFAULT_IMPORTANCE, ...patch });
  const next = () => (last ? onDone() : setIndex(index + 1));
  const back = () => (index === 0 ? onExit() : setIndex(index - 1));

  // Keyboard: 1–9 choose an option, Q/W/E set importance, Enter = next, Backspace = back.
  // Buttons and links keep their native Enter; arrow keys are left to the radio groups.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey || e.altKey || e.isComposing) return;
      const target = e.target as HTMLElement;
      const n = Number(e.key);
      if (Number.isInteger(n) && n >= 1 && n <= q.options.length) {
        e.preventDefault();
        set({ choice: q.options[n - 1].value });
        // Keep focus on the chosen option so the focus ring and the selection never point at different rows.
        focusRadio(q.id, n - 1);
        return;
      }
      const imp = q.importanceControl && IMPORTANCE.find((o) => o.key === e.key.toLowerCase());
      if (imp) {
        e.preventDefault();
        set({ importance: imp.value });
        focusRadio(`${q.id}-importance`, IMPORTANCE.indexOf(imp));
        return;
      }
      if (e.key === "Enter" && !target.closest("button, a") && a?.choice !== undefined) {
        e.preventDefault();
        next();
      } else if (e.key === "Backspace" && !target.closest("input[type=text], textarea")) {
        e.preventDefault();
        back();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });

  return (
    <section className="quiz" aria-labelledby="q-prompt">
      <div className="progress" aria-hidden="true">
        <div style={{ width: `${((index + 1) / questions.length) * 100}%` }} />
      </div>
      <p className="count">
        {index + 1} / {questions.length}
      </p>
      <fieldset key={q.id}>
        <legend id="q-prompt">{q.prompt}</legend>
        {q.options.map((o, i) => (
          <label key={o.value} className="option">
            <input type="radio" name={q.id} checked={a?.choice === o.value} onChange={() => set({ choice: o.value })} />
            <span>
              <kbd className="key" aria-hidden="true">
                {i + 1}
              </kbd>
              {o.label}
            </span>
          </label>
        ))}
      </fieldset>
      {q.importanceControl && (
        <fieldset className="importance">
          <legend>この条件はどれくらい大事？</legend>
          <div className="segments">
            {IMPORTANCE.map((o) => (
              <label key={o.value}>
                <input
                  type="radio"
                  name={`${q.id}-importance`}
                  checked={(a?.importance ?? DEFAULT_IMPORTANCE) === o.value}
                  onChange={() => set({ importance: o.value })}
                />
                <span>
                  <kbd className="key" aria-hidden="true">
                    {o.key.toUpperCase()}
                  </kbd>
                  {o.label}
                </span>
              </label>
            ))}
          </div>
        </fieldset>
      )}
      <div className="actions">
        <button type="button" className="primary" disabled={a?.choice === undefined} onClick={next}>
          {last ? "結果を見る" : "次へ"}
        </button>
        <button type="button" className="link" onClick={back}>
          {index === 0 ? "トップに戻る" : "前の質問"}
        </button>
      </div>
      <p className="keys-hint" aria-hidden="true">
        キーボード: <kbd>1</kbd>〜<kbd>{q.options.length}</kbd> で選択
        {q.importanceControl && (
          <>
            、<kbd>Q</kbd> <kbd>W</kbd> <kbd>E</kbd> で大事さ
          </>
        )}
        、<kbd>Enter</kbd> で次へ、<kbd>Backspace</kbd> で戻る
      </p>
    </section>
  );
}
