import React from "react";
import { getDisciplineColor } from "../../shared/helpers";

export default function DisciplineChip({ label, isSelected, onClick }) {
  const color = label === "All" ? "var(--amber)" : getDisciplineColor(label);

  return (
    <button
      onClick={onClick}
      className="glass-control"
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "8px",
        padding: "6px 16px",
        borderRadius: "var(--radius-pill)",
        fontSize: "13px",
        fontFamily: "var(--font-ui)",
        color: isSelected ? "var(--paper-100)" : "var(--paper-300)",
        backgroundColor: isSelected ? "rgba(244, 237, 225, 0.12)" : "rgba(244, 237, 225, 0.03)",
        borderColor: isSelected ? color : "rgba(244, 237, 225, 0.10)",
        cursor: "pointer",
        transition: "all var(--transition-fast)",
      }}
    >
      <span
        style={{
          width: "8px",
          height: "8px",
          borderRadius: "50%",
          backgroundColor: color,
          boxShadow: isSelected ? `0 0 8px ${color}` : "none",
        }}
      />
      <span>{label}</span>
    </button>
  );
}
