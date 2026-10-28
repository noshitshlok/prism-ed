import React, { useState, useEffect } from "react";
import { askTutor, streamTutor } from "../../api/tutor";

export default function TutorBox({ topicId, partId = null, partName = null, topicName = null }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [lastQuestion, setLastQuestion] = useState("");

  // Tutor state resets cleanly when the selected part changes
  useEffect(() => {
    setQuestion("");
    setAnswer("");
    setError(null);
    setHistory([]);
    setLastQuestion("");
  }, [partId]);

  const handleSubmit = async (e, retryQ = null) => {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }

    const currentQ = (retryQ || question).trim();
    if (!currentQ || currentQ.length < 2 || isLoading) return;

    setLastQuestion(currentQ);
    setAnswer("");
    setError(null);
    setIsLoading(true);

    let streamedAccumulator = "";

    await streamTutor(
      topicId,
      partId,
      currentQ,
      history,
      (token) => {
        streamedAccumulator += token;
        setAnswer(streamedAccumulator);
      },
      () => {
        setIsLoading(false);
        if (streamedAccumulator) {
          setHistory((prev) => [
            ...prev,
            { role: "user", content: currentQ },
            { role: "assistant", content: streamedAccumulator },
          ]);
        }
        setQuestion("");
      },
      async (_err) => {
        // Fallback to standard HTTP /ask if streaming encounters an issue
        try {
          const fallbackAns = await askTutor(topicId, partId, currentQ, history);
          setAnswer(fallbackAns);
          setHistory((prev) => [
            ...prev,
            { role: "user", content: currentQ },
            { role: "assistant", content: fallbackAns },
          ]);
          setQuestion("");
          setIsLoading(false);
        } catch {
          setError("The tutor is unavailable right now. Try again.");
          setIsLoading(false);
        }
      }
    );
  };

  const titleText = partName
    ? `Ask about this part (${partName})`
    : `Ask about this model (${topicName || "Specimen"})`;

  const placeholderText = partName
    ? `Why does ${partName} work this way?`
    : `What does this ${topicName || "model"} do in engineering?`;

  return (
    <div
      onClick={(e) => e.stopPropagation()}
      style={{
        marginTop: "var(--space-5)",
        paddingTop: "var(--space-4)",
        borderTop: "1px solid rgba(244, 237, 225, 0.08)",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "var(--space-2)",
        }}
      >
        <span
          style={{
            fontFamily: "var(--font-ui)",
            fontSize: "13px",
            color: "var(--paper-300)",
            fontWeight: 500,
          }}
        >
          {titleText}
        </span>
        <span
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "11px",
            color: "var(--paper-500)",
          }}
        >
          Grounded AI Tutor
        </span>
      </div>

      <form onSubmit={(e) => handleSubmit(e)} style={{ display: "flex", gap: "var(--space-2)" }}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder={placeholderText}
          maxLength={500}
          className="glass-control"
          style={{
            flex: 1,
            padding: "8px 12px",
            fontSize: "14px",
            fontFamily: "var(--font-ui)",
          }}
          disabled={isLoading}
        />
        <button
          type="submit"
          className="glass-control"
          disabled={isLoading || question.trim().length < 2}
          style={{
            padding: "8px 16px",
            background: "var(--amber)",
            color: "var(--bench-900)",
            fontWeight: 600,
            fontSize: "13px",
            opacity: isLoading || question.trim().length < 2 ? 0.6 : 1,
          }}
        >
          {isLoading ? "..." : "Ask"}
        </button>
      </form>

      {/* Loading state indicator */}
      {isLoading && !answer && (
        <div
          style={{
            marginTop: "var(--space-3)",
            padding: "var(--space-2) var(--space-3)",
            display: "flex",
            alignItems: "center",
            gap: "8px",
            fontFamily: "var(--font-mono)",
            fontSize: "12px",
            color: "var(--amber)",
          }}
        >
          <span style={{ display: "inline-block", animation: "pulse 1.5s infinite" }}>⚡</span>
          <span>Consulting engineering curriculum tutor...</span>
        </div>
      )}

      {/* Answer Output */}
      {answer && (
        <div
          style={{
            marginTop: "var(--space-3)",
            padding: "var(--space-3)",
            backgroundColor: "rgba(244, 237, 225, 0.04)",
            borderRadius: "var(--radius-control)",
            borderLeft: "2px solid var(--amber)",
          }}
        >
          <div
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "11px",
              color: "var(--amber)",
              marginBottom: "var(--space-1)",
              display: "flex",
              justifyContent: "space-between",
            }}
          >
            <span>Tutor Response</span>
            {isLoading && <span style={{ color: "var(--teal)" }}>streaming...</span>}
          </div>
          <p style={{ fontSize: "15px", color: "var(--paper-100)", lineHeight: 1.5, margin: 0 }}>
            {answer}
          </p>
        </div>
      )}

      {/* Error state with Retry button */}
      {error && (
        <div
          style={{
            marginTop: "var(--space-3)",
            padding: "var(--space-3)",
            borderRadius: "var(--radius-control)",
            backgroundColor: "rgba(228, 103, 91, 0.08)",
            borderLeft: "3px solid var(--coral)",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            gap: "8px",
          }}
        >
          <span style={{ fontSize: "13px", color: "var(--coral)", fontFamily: "var(--font-ui)" }}>
            {error}
          </span>
          {lastQuestion && (
            <button
              type="button"
              onClick={() => handleSubmit(null, lastQuestion)}
              className="glass-control"
              style={{
                padding: "3px 10px",
                fontSize: "12px",
                color: "var(--paper-100)",
                borderColor: "rgba(228, 103, 91, 0.3)",
              }}
            >
              Retry
            </button>
          )}
        </div>
      )}
    </div>
  );
}
