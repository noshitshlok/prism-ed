import React from "react";

export default function GlassPanel({ children, strong = false, className = "", style = {}, ...props }) {
  const surfaceClass = strong ? "glass-surface-strong" : "glass-surface";
  return (
    <div
      className={`${surfaceClass} ${className}`}
      style={{
        padding: "var(--space-5)",
        ...style,
      }}
      {...props}
    >
      {children}
    </div>
  );
}
