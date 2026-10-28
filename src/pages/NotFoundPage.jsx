import React from "react";
import { Link } from "react-router-dom";
import HeaderBar from "../shared/HeaderBar";
import GlassPanel from "../shared/GlassPanel";

export default function NotFoundPage() {
  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <HeaderBar backTo="/" backLabel="Specimens" />
      <main style={{ maxWidth: "600px", margin: "var(--space-8) auto", padding: "0 var(--space-4)", width: "100%", flex: 1, textAlign: "center" }}>
        <GlassPanel strong style={{ padding: "var(--space-7)" }}>
          <div style={{ fontFamily: "var(--font-mono)", fontSize: "14px", color: "var(--coral)", marginBottom: "var(--space-2)" }}>
            [404 — NOT FOUND]
          </div>
          <h1 style={{ fontSize: "32px", color: "var(--paper-100)", marginBottom: "var(--space-3)" }}>
            This specimen is not on the bench.
          </h1>
          <p style={{ color: "var(--paper-300)", marginBottom: "var(--space-5)" }}>
            The requested topic or route does not exist in the current engineering registry.
          </p>
          <Link
            to="/"
            className="glass-control"
            style={{
              display: "inline-block",
              padding: "10px 24px",
              backgroundColor: "var(--amber)",
              color: "var(--bench-900)",
              fontWeight: 600,
              fontSize: "14px",
            }}
          >
            Return to Bench
          </Link>
        </GlassPanel>
      </main>
    </div>
  );
}
