import type { Question } from "./model/types.ts";
import type { Preference } from "./scoring/score.ts";

/** `choice` is the selected option value; `importance` is 0/1/2 for ideal-type questions. */
export interface Answer {
  choice?: number;
  importance: number;
}

export const DEFAULT_IMPORTANCE = 1;

export function toPreferences(questions: Question[], answers: Record<string, Answer>): Preference[] {
  return questions.flatMap((q): Preference[] => {
    const a = answers[q.id] ?? { importance: 0 }; // unanswered = not weighted
    if (q.answerKind === "ideal") return [{ metric: q.metrics[0], ideal: a.choice, weight: a.importance }];
    // A question over several metrics splits its weight equally; the answer weight still picks the "enough" target.
    const w = a.choice ?? 0;
    return q.metrics.map((metric) =>
      q.metrics.length === 1 ? { metric, weight: w } : { metric, weight: w / q.metrics.length, answerWeight: w },
    );
  });
}
