import { useMemo, useState } from "react";
import { toPreferences, type Answer } from "./answers.ts";
import { About } from "./components/About.tsx";
import { Intro } from "./components/Intro.tsx";
import { Quiz } from "./components/Quiz.tsx";
import { Result } from "./components/Result.tsx";
import { hasPlaceholder, knowledge } from "./data.ts";

type Screen = "intro" | "quiz" | "result" | "about";

export function App() {
  const [screen, setScreenState] = useState<Screen>("intro");
  const [back, setBack] = useState<Screen>("intro");
  const [answers, setAnswers] = useState<Record<string, Answer>>({});
  const prefs = useMemo(() => toPreferences(knowledge.questions, answers), [answers]);

  const setScreen = (next: Screen) => {
    setScreenState(next);
    window.scrollTo(0, 0);
  };

  const about = () => {
    setBack(screen);
    setScreen("about");
  };
  const restart = () => {
    setAnswers({});
    setScreen("quiz");
  };

  return (
    <>
      {hasPlaceholder && (
        <p className="banner" role="note">
          仮のデータで動いている試作版です。都市の数値は実測ではありません。
        </p>
      )}
      <main>
        {screen === "intro" && <Intro onStart={restart} onAbout={about} />}
        {screen === "quiz" && (
          <Quiz
            answers={answers}
            onAnswer={(id, a) => setAnswers((prev) => ({ ...prev, [id]: a }))}
            onDone={() => setScreen("result")}
            onExit={() => setScreen("intro")}
          />
        )}
        {screen === "result" && <Result prefs={prefs} onRetry={restart} onAbout={about} />}
        {screen === "about" && <About onBack={() => setScreen(back)} />}
      </main>
    </>
  );
}
