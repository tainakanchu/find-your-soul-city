import { useState } from "react";
import { DEFAULT_IMPORTANCE, type Answer } from "../answers.ts";
import { knowledge } from "../data.ts";

const IMPORTANCE = [
  { label: "気にしない", value: 0 },
  { label: "ふつう", value: 1 },
  { label: "重要", value: 2 },
];

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
        {q.options.map((o) => (
          <label key={o.value} className="option">
            <input type="radio" name={q.id} checked={a?.choice === o.value} onChange={() => set({ choice: o.value })} />
            <span>{o.label}</span>
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
                <span>{o.label}</span>
              </label>
            ))}
          </div>
        </fieldset>
      )}
      <div className="actions">
        <button
          type="button"
          className="primary"
          disabled={a?.choice === undefined}
          onClick={() => (last ? onDone() : setIndex(index + 1))}
        >
          {last ? "結果を見る" : "次へ"}
        </button>
        <button type="button" className="link" onClick={() => (index === 0 ? onExit() : setIndex(index - 1))}>
          {index === 0 ? "トップに戻る" : "前の質問"}
        </button>
      </div>
    </section>
  );
}
