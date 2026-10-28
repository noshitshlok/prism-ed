import React from "react";

export default function SpectrumBar({ progress = 0, height = "4px", className = "" }) {
  const clampedProgress = Math.min(100, Math.max(0, progress));
  return (
    <div
      className={className}
      style={{
        width: "100%",
        height: height,
        backgroundColor: "rgba(244, 237, 225, 0.08)",
        borderRadius: "var(--radius-pill)",
        overflow: "hidden",
        position: "relative",
      }}
      role="progressbar"
      aria-valuenow={clampedProgress}
      aria-valuemin={0}
      aria-valuemax={100}
    >
      <div
        style={{
          width: `${clampedProgress}%`,
          height: "100%",
          background: "var(--spectrum-gradient)",
          borderRadius: "var(--radius-pill)",
          transition: "width 300ms ease-out",
        }}
      />
    </div>
  );
}
