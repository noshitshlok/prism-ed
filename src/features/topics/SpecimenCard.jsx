import React from "react";
import { Link } from "react-router-dom";
import GlassPanel from "../../shared/GlassPanel";
import { getDisciplineColor, getCatalogNumber } from "../../shared/helpers";

export default function SpecimenCard({ topic, index = 0 }) {
  const disciplineColor = getDisciplineColor(topic.discipline);
  const catalogNum = getCatalogNumber(topic.id, index);
  const isScannerMarker = ["circuit-board", "differential-gearbox", "four-stroke-engine"].includes(topic.id);

  return (
    <Link
      to={`/topics/${topic.id}`}
      style={{
        display: "block",
        textDecoration: "none",
        color: "inherit",
        outline: "none",
      }}
    >
      <GlassPanel
        className="specimen-card"
        style={{
          position: "relative",
          overflow: "hidden",
          transition: "transform var(--transition-fast), border-color var(--transition-fast), box-shadow var(--transition-fast)",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          padding: "var(--space-5)",
        }}
      >
        {/* Top 2px discipline-coloured line inside edge */}
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            height: "2px",
            backgroundColor: disciplineColor,
          }}
        />

        <div>
          {/* Header row: catalog number & parts count */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "var(--space-3)",
            }}
          >
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "12px",
                color: "var(--amber)",
                letterSpacing: "0.5px",
              }}
            >
              {catalogNum}
            </span>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              {isScannerMarker && (
                <span
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "11px",
                    padding: "2px 7px",
                    borderRadius: "var(--radius-pill)",
                    backgroundColor: "rgba(63, 184, 166, 0.15)",
                    color: "var(--teal)",
                    border: "1px solid rgba(63, 184, 166, 0.3)",
                    display: "inline-flex",
                    alignItems: "center",
                    gap: "4px",
                  }}
                  title="Supported by Diagram Scanner preview"
                >
                  <span>📷</span>
                  <span>Scanner</span>
                </span>
              )}
              <span
                style={{
                  fontFamily: "var(--font-mono)",
                  fontSize: "12px",
                  color: "var(--paper-500)",
                }}
              >
                {topic.partsCount || 5} parts
              </span>
            </div>
          </div>

          {/* Title in Fraunces */}
          <h3
            style={{
              fontSize: "22px",
              lineHeight: 1.25,
              marginBottom: "var(--space-2)",
              color: "var(--paper-100)",
            }}
          >
            {topic.name}
          </h3>

          {/* Description */}
          <p
            style={{
              fontSize: "15px",
              color: "var(--paper-300)",
              lineHeight: 1.5,
              marginBottom: "var(--space-4)",
            }}
          >
            {topic.description}
          </p>
        </div>

        {/* Footer row: Discipline & Action hint */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            paddingTop: "var(--space-3)",
            borderTop: "1px solid rgba(244, 237, 225, 0.06)",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <span
              style={{
                width: "6px",
                height: "6px",
                borderRadius: "50%",
                backgroundColor: disciplineColor,
              }}
            />
            <span
              style={{
                fontSize: "13px",
                color: "var(--paper-300)",
                fontFamily: "var(--font-ui)",
              }}
            >
              {topic.discipline}
            </span>
          </div>

          <span
            style={{
              fontSize: "13px",
              color: "var(--amber)",
              fontFamily: "var(--font-ui)",
              fontWeight: 500,
            }}
          >
            Open specimen →
          </span>
        </div>
      </GlassPanel>

      <style>
        {`
          .specimen-card:hover {
            transform: translateY(-2px);
            border-color: rgba(244, 237, 225, 0.22);
            box-shadow: var(--glass-shadow), 0 0 20px rgba(232, 163, 61, 0.10);
          }
        `}
      </style>
    </Link>
  );
}
