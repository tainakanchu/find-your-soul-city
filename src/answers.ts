import type { Question } from "./model/types.ts";
import type { Preference } from "./scoring/score.ts";

/** `choice` is the selected option value; `importance` is 0/1/2 for ideal-type questions. */
export interface Answer {
  choice?: number;
  importance: number;
}

export const DEFAULT_IMPORTANCE = 1;

export function toPreferences(questions: Question[], answers: Record<string, Answer>): Preference[] {
  return questions.map((q) => {
    const a = answers[q.id] ?? { importance: 0 }; // unanswered = not weighted
    return q.answerKind === "ideal"
      ? { metric: q.metric, ideal: a.choice, weight: a.importance }
      : { metric: q.metric, weight: a.choice ?? 0 };
  });
}
