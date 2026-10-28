import React from "react";
import { Link } from "react-router-dom";
import GlassPanel from "../../shared/GlassPanel";
import TutorBox from "../tutor/TutorBox";

export default function MarginNotes({
  topicId,
  topicName = null,
  selectedPart = null,
  partNumber = null,
  totalParts = 5,
}) {
  return (
    <GlassPanel
      strong
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        minHeight: "540px",
        height: "100%",
        padding: "var(--space-6)",
      }}
    >
      <div>
        {!selectedPart ? (
          <div>
            <div
              style={{
                padding: "var(--space-6) var(--space-4)",
                textAlign: "center",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: "var(--space-3)",
                backgroundColor: "rgba(244, 237, 225, 0.02)",
                borderRadius: "var(--radius-control)",
                border: "1px dashed rgba(244, 237, 225, 0.12)",
                marginBottom: "var(--space-4)",
              }}
            >
              <div
                style={{
                  width: "40px",
                  height: "40px",
                  borderRadius: "50%",
                  border: "1px dashed rgba(244, 237, 225, 0.2)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "var(--amber)",
                  fontFamily: "var(--font-mono)",
                  fontSize: "16px",
                }}
              >
                ◎
              </div>
              <h4 style={{ fontSize: "17px", color: "var(--paper-100)", margin: 0 }}>
                {topicName || "Specimen Bench"}
              </h4>
              <p style={{ color: "var(--paper-500)", fontSize: "14px", margin: 0, maxWidth: "300px" }}>
                Select a numbered point on the 3D model to inspect specific parts, or ask a general question below.
              </p>
            </div>

            {/* Model-Level Tutor Box (§4.2) */}
            <TutorBox topicId={topicId} partId={null} partName={null} topicName={topicName} />
          </div>
        ) : (
          <div>
            {/* Part Index in Mono */}
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
                  fontFamily: "var(--font-mono)",
                  fontSize: "12px",
                  color: "var(--amber)",
                  textTransform: "uppercase",
                  letterSpacing: "1px",
                }}
              >
                Point {partNumber || 1} of {totalParts}
              </span>
              <span
                style={{
                  fontFamily: "var(--font-mono)",
                  fontSize: "11px",
                  color: "var(--paper-500)",
                }}
              >
                {selectedPart.hotspotPosition}
              </span>
            </div>

            {/* Part Name in Fraunces */}
            <h3
              style={{
                fontSize: "24px",
                color: "var(--paper-100)",
                marginBottom: "var(--space-3)",
                lineHeight: 1.25,
              }}
            >
              {selectedPart.name}
            </h3>

            {/* Explanation in Newsreader */}
            <p
              style={{
                fontFamily: "var(--font-body)",
                fontSize: "17px",
                lineHeight: 1.6,
                color: "var(--paper-100)",
                marginBottom: "var(--space-4)",
              }}
            >
              {selectedPart.explanation}
            </p>

            {/* Formula block if exists */}
            {selectedPart.formulaOrLaw && (
              <div
                style={{
                  padding: "var(--space-3) var(--space-4)",
                  backgroundColor: "rgba(20, 17, 15, 0.6)",
                  borderLeft: "3px solid var(--teal)",
                  borderRadius: "0 var(--radius-control) var(--radius-control) 0",
                  fontFamily: "var(--font-mono)",
                  fontSize: "13px",
                  color: "var(--teal)",
                  marginBottom: "var(--space-4)",
                  overflowX: "auto",
                }}
              >
                <div
                  style={{
                    fontSize: "10px",
                    color: "var(--paper-500)",
                    textTransform: "uppercase",
                    marginBottom: "2px",
                  }}
                >
                  Governing Principle / Formula
                </div>
                {selectedPart.formulaOrLaw}
              </div>
            )}

            {/* Nested Part Tutor Box */}
            <TutorBox
              topicId={topicId}
              partId={selectedPart.id}
              partName={selectedPart.name}
              topicName={topicName}
            />
          </div>
        )}
      </div>

      {/* Footer Action: Take the quiz */}
      <div
        style={{
          marginTop: "var(--space-6)",
          paddingTop: "var(--space-4)",
          borderTop: "1px solid rgba(244, 237, 225, 0.08)",
        }}
      >
        <Link
          to={`/topics/${topicId}/quiz`}
          className="glass-control"
          style={{
            display: "block",
            textAlign: "center",
            padding: "12px",
            backgroundColor: "var(--amber)",
            color: "var(--bench-900)",
            fontWeight: 600,
            fontSize: "15px",
            borderRadius: "var(--radius-control)",
            transition: "all var(--transition-fast)",
            textDecoration: "none",
          }}
        >
          Take the Quiz →
        </Link>
      </div>
    </GlassPanel>
  );
}
