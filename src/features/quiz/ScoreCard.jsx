import React from "react";
import { Link } from "react-router-dom";
import GlassPanel from "../../shared/GlassPanel";

export default function ScoreCard({
  topicId,
  score,
  total,
  percentage,
  passed,
  onRetry,
}) {
  return (
    <GlassPanel
      strong
      style={{
        maxWidth: "560px",
        margin: "var(--space-7) auto",
        textAlign: "center",
        padding: "var(--space-7)",
      }}
    >
      <span
        style={{
          fontFamily: "var(--font-mono)",
          fontSize: "12px",
          color: passed ? "var(--moss)" : "var(--coral)",
          textTransform: "uppercase",
          letterSpacing: "1px",
        }}
      >
        {passed ? "Assessment Passed" : "Needs Review"}
      </span>

      <div
        style={{
          fontFamily: "var(--font-display)",
          fontSize: "64px",
          color: "var(--paper-100)",
          margin: "var(--space-3) 0",
          lineHeight: 1,
        }}
      >
        {score} / {total}
      </div>

      <p
        style={{
          fontSize: "18px",
          color: "var(--paper-300)",
          marginBottom: "var(--space-6)",
        }}
      >
        {passed
          ? `Mastery achieved with a score of ${percentage}%. You have demonstrated a solid understanding of the governing principles.`
          : `You scored ${percentage}%. Inspect the model's margin notes and governing equations before attempting again.`}
      </p>

      <div
        style={{
          display: "flex",
          gap: "var(--space-4)",
          justifyContent: "center",
        }}
      >
        <button
          onClick={onRetry}
          className="glass-control"
          style={{
            padding: "10px 24px",
            background: "rgba(244, 237, 225, 0.08)",
            color: "var(--paper-100)",
            fontSize: "14px",
            fontWeight: 600,
          }}
        >
          Try Again
        </button>

        <Link
          to={`/topics/${topicId}`}
          className="glass-control"
          style={{
            padding: "10px 24px",
            background: "var(--amber)",
            color: "var(--bench-900)",
            fontSize: "14px",
            fontWeight: 600,
          }}
        >
          Back to Topic
        </Link>
      </div>
    </GlassPanel>
  );
}
