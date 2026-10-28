import React from "react";
import GlassPanel from "./GlassPanel";

export default function StateView({
  loading = false,
  error = null,
  isEmpty = false,
  emptyMessage = "No items found on the bench.",
  emptyAction = null,
  onRetry = null,
  requestId = null,
  children,
}) {
  if (loading) {
    return (
      <GlassPanel style={{ padding: "var(--space-6)" }}>
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-4)" }}>
          <div
            style={{
              height: "28px",
              width: "45%",
              borderRadius: "var(--radius-control)",
              background: "linear-gradient(90deg, rgba(244,237,225,0.04) 25%, rgba(244,237,225,0.08) 50%, rgba(244,237,225,0.04) 75%)",
              backgroundSize: "200% 100%",
              animation: "shimmer 1.8s infinite ease-in-out",
            }}
          />
          <div
            style={{
              height: "16px",
              width: "80%",
              borderRadius: "var(--radius-control)",
              background: "rgba(244,237,225,0.04)",
            }}
          />
          <div
            style={{
              height: "16px",
              width: "60%",
              borderRadius: "var(--radius-control)",
              background: "rgba(244,237,225,0.04)",
            }}
          />
        </div>
        <style>
          {`
            @keyframes shimmer {
              0% { background-position: 200% 0; }
              100% { background-position: -200% 0; }
            }
          `}
        </style>
      </GlassPanel>
    );
  }

  if (error) {
    return (
      <GlassPanel
        style={{
          borderLeft: "3px solid var(--coral)",
          padding: "var(--space-5)",
          textAlign: "left",
        }}
      >
        <h3 style={{ color: "var(--coral)", fontSize: "20px", marginBottom: "var(--space-2)" }}>
          Cannot reach PrismEd right now
        </h3>
        <p style={{ color: "var(--paper-300)", marginBottom: "var(--space-4)", fontSize: "16px" }}>
          {error.message || String(error)}
        </p>
        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-4)" }}>
          {onRetry && (
            <button
              onClick={onRetry}
              className="glass-control"
              style={{
                padding: "8px 16px",
                background: "var(--amber)",
                color: "var(--bench-900)",
                fontWeight: 600,
                border: "none",
              }}
            >
              Try Again
            </button>
          )}
          {requestId && (
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "12px",
                color: "var(--paper-500)",
              }}
            >
              Request ID: {requestId}
            </span>
          )}
        </div>
      </GlassPanel>
    );
  }

  if (isEmpty) {
    return (
      <GlassPanel style={{ textAlign: "center", padding: "var(--space-7)" }}>
        <p style={{ fontSize: "18px", color: "var(--paper-300)", marginBottom: "var(--space-4)" }}>
          {emptyMessage}
        </p>
        {emptyAction}
      </GlassPanel>
    );
  }

  return children;
}
