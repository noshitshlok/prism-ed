import { useState } from "react";
import { askTutor } from "../../api/tutor";
import "./ConceptPanel.css";

export default function ConceptPanel({ part, topicId }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);

  if (!part) {
    return (
      <div className="concept-panel placeholder">
        <p>Click a hotspot on the model to learn about that part.</p>
      </div>
    );
  }

  async function handleAsk() {
    if (!question.trim()) return;
    setLoading(true);
    setAnswer(null);
    try {
      const result = await askTutor(topicId, part.id, question);
      setAnswer(result);
    } catch {
      setAnswer("Sorry, something went wrong asking the tutor.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="concept-panel">
      <h3>{part.name}</h3>
      <p>{part.explanation}</p>

      <div className="tutor-box">
        <input
          type="text"
          placeholder="Ask a follow-up question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
        />
        <button onClick={handleAsk} disabled={loading}>
          {loading ? "Asking..." : "Ask"}
        </button>
      </div>

      {answer && <p className="tutor-answer">{answer}</p>}
    </div>
  );
}