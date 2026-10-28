import React, { useState } from "react";
import GlassPanel from "../../shared/GlassPanel";
import SpectrumBar from "../../shared/SpectrumBar";
import ScoreCard from "./ScoreCard";
import { submitQuizAnswers, generateAiQuiz } from "../../api/quiz";
import { recordQuizAttempt } from "../../api/progress";

export default function QuizRunner({ topicId, topicName, initialQuestions = [], isAiGenerated = false }) {
  const [questions, setQuestions] = useState(initialQuestions);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState({}); // questionId -> selectedIndex
  const [selectedOption, setSelectedOption] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [isAiMode, setIsAiMode] = useState(isAiGenerated);
  const [isGeneratingAi, setIsGeneratingAi] = useState(false);

  const totalQuestions = questions.length;
  const currentQuestion = questions[currentIndex];
  const progressPercent = totalQuestions > 0 ? (currentIndex / totalQuestions) * 100 : 0;
  const optionLetters = ["A", "B", "C", "D", "E"];

  const handleSelectOption = (idx) => {
    setSelectedOption(idx);
  };

  const handleNext = async () => {
    if (selectedOption === null) return;

    const updatedAnswers = {
      ...userAnswers,
      [currentQuestion.id]: selectedOption,
    };
    setUserAnswers(updatedAnswers);
    setSelectedOption(null);

    if (currentIndex + 1 < totalQuestions) {
      setCurrentIndex(currentIndex + 1);
    } else {
      // Final Question: Submit to Backend for Server-Side Grading
      setIsSubmitting(true);
      try {
        const res = await submitQuizAnswers(topicId, updatedAnswers);
        setResult(res);

        // Record attempt to session progress tracking
        try {
          await recordQuizAttempt(topicId, res.score, res.total);
        } catch (eProgress) {
          console.warn("Could not save progress:", eProgress);
        }
      } catch (err) {
        console.error("Grading failed:", err);
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  const handleGenerateAiQuiz = async () => {
    setIsGeneratingAi(true);
    try {
      const aiData = await generateAiQuiz(topicId);
      if (aiData && aiData.questions && aiData.questions.length > 0) {
        setQuestions(aiData.questions);
        setCurrentIndex(0);
        setUserAnswers({});
        setSelectedOption(null);
        setResult(null);
        setIsAiMode(true);
      }
    } catch {
      alert("AI quiz generation temporarily unavailable. Reverting to static quiz.");
    } finally {
      setIsGeneratingAi(false);
    }
  };

  const handleRetry = () => {
    setCurrentIndex(0);
    setUserAnswers({});
    setSelectedOption(null);
    setResult(null);
  };

  if (result) {
    return (
      <div style={{ maxWidth: "720px", margin: "0 auto", padding: "var(--space-6) var(--space-4)" }}>
        <ScoreCard
          topicId={topicId}
          score={result.score}
          total={result.total}
          percentage={result.percentage}
          passed={result.passed}
          onRetry={handleRetry}
        />

        {/* Detailed Feedback Review List */}
        <div style={{ marginTop: "var(--space-6)" }}>
          <h3 style={{ fontSize: "20px", marginBottom: "var(--space-4)", color: "var(--paper-100)" }}>
            Assessment Analysis & Review
          </h3>
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-4)" }}>
            {result.feedback.map((item, idx) => (
              <GlassPanel
                key={idx}
                style={{
                  borderLeft: item.isCorrect ? "3px solid var(--moss)" : "3px solid var(--coral)",
                  padding: "var(--space-4) var(--space-5)",
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "var(--space-2)" }}>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: "12px", color: "var(--paper-500)" }}>
                    Question {idx + 1}
                  </span>
                  <span
                    style={{
                      fontFamily: "var(--font-mono)",
                      fontSize: "12px",
                      fontWeight: 600,
                      color: item.isCorrect ? "var(--moss)" : "var(--coral)",
                    }}
                  >
                    {item.isCorrect ? "✓ Correct" : "✗ Incorrect"}
                  </span>
                </div>

                <h4 style={{ fontSize: "16px", color: "var(--paper-100)", marginBottom: "var(--space-3)" }}>
                  {item.question}
                </h4>

                {item.explanation && (
                  <div
                    style={{
                      padding: "var(--space-3)",
                      background: "rgba(244, 237, 225, 0.03)",
                      borderRadius: "var(--radius-control)",
                      fontFamily: "var(--font-body)",
                      fontSize: "15px",
                      color: "var(--paper-300)",
                      lineHeight: 1.5,
                    }}
                  >
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: "11px", color: "var(--amber)", display: "block", marginBottom: "4px" }}>
                      Engineering Explanation:
                    </span>
                    {item.explanation}
                  </div>
                )}
              </GlassPanel>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (!currentQuestion) return null;

  return (
    <div style={{ maxWidth: "680px", margin: "var(--space-6) auto", padding: "0 var(--space-4)" }}>
      {/* Header bar and AI status */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "var(--space-3)",
        }}
      >
        <div>
          <span
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "12px",
              color: "var(--paper-500)",
              textTransform: "uppercase",
              letterSpacing: "0.5px",
            }}
          >
            {topicName}
          </span>
          <div style={{ fontFamily: "var(--font-mono)", fontSize: "14px", color: "var(--amber)", marginTop: "2px" }}>
            Question {currentIndex + 1} of {totalQuestions}
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)" }}>
          {isAiMode ? (
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "11px",
                padding: "3px 8px",
                borderRadius: "var(--radius-pill)",
                backgroundColor: "rgba(156, 140, 208, 0.15)",
                color: "var(--violet-soft)",
              }}
            >
              Generated for this session
            </span>
          ) : (
            <button
              onClick={handleGenerateAiQuiz}
              disabled={isGeneratingAi}
              className="glass-control"
              style={{
                fontSize: "12px",
                fontFamily: "var(--font-mono)",
                padding: "4px 10px",
                color: "var(--violet-soft)",
              }}
            >
              {isGeneratingAi ? "Generating..." : "✨ Generate AI Quiz"}
            </button>
          )}
        </div>
      </div>

      {/* Spectrum Progress Bar */}
      <SpectrumBar progress={progressPercent} height="3px" style={{ marginBottom: "var(--space-5)" }} />

      {/* Question Card */}
      <GlassPanel strong style={{ padding: "var(--space-6)" }}>
        <h2
          style={{
            fontSize: "22px",
            lineHeight: 1.35,
            color: "var(--paper-100)",
            marginBottom: "var(--space-5)",
          }}
        >
          {currentQuestion.question}
        </h2>

        {/* Options */}
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)" }}>
          {currentQuestion.options.map((opt, oIdx) => {
            const isSelected = selectedOption === oIdx;
            const letter = optionLetters[oIdx] || String(oIdx + 1);

            return (
              <button
                key={oIdx}
                onClick={() => handleSelectOption(oIdx)}
                className="glass-control"
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "var(--space-3)",
                  padding: "var(--space-4)",
                  textAlign: "left",
                  width: "100%",
                  backgroundColor: isSelected ? "rgba(232, 163, 61, 0.14)" : "rgba(244, 237, 225, 0.03)",
                  borderColor: isSelected ? "var(--amber)" : "rgba(244, 237, 225, 0.10)",
                  cursor: "pointer",
                  transition: "all var(--transition-fast)",
                }}
              >
                <span
                  style={{
                    width: "28px",
                    height: "28px",
                    borderRadius: "6px",
                    backgroundColor: isSelected ? "var(--amber)" : "rgba(244, 237, 225, 0.08)",
                    color: isSelected ? "var(--bench-900)" : "var(--paper-300)",
                    fontFamily: "var(--font-mono)",
                    fontWeight: 700,
                    fontSize: "13px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    flexShrink: 0,
                  }}
                >
                  {letter}
                </span>

                <span
                  style={{
                    fontSize: "15px",
                    color: isSelected ? "var(--paper-100)" : "var(--paper-300)",
                    lineHeight: 1.4,
                  }}
                >
                  {opt}
                </span>
              </button>
            );
          })}
        </div>

        {/* Action Button */}
        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
            marginTop: "var(--space-6)",
            paddingTop: "var(--space-4)",
            borderTop: "1px solid rgba(244, 237, 225, 0.08)",
          }}
        >
          <button
            onClick={handleNext}
            disabled={selectedOption === null || isSubmitting}
            className="glass-control"
            style={{
              padding: "10px 28px",
              backgroundColor: "var(--amber)",
              color: "var(--bench-900)",
              fontWeight: 600,
              fontSize: "15px",
              borderRadius: "var(--radius-control)",
              opacity: selectedOption === null || isSubmitting ? 0.5 : 1,
            }}
          >
            {isSubmitting
              ? "Grading..."
              : currentIndex + 1 === totalQuestions
              ? "Submit Answers"
              : "Next Question →"}
          </button>
        </div>
      </GlassPanel>
    </div>
  );
}
