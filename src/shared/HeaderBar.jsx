import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import AboutSheet from "./AboutSheet";

export default function HeaderBar({ backTo = null, backLabel = "Back to bench", title = null, catalogNumber = null }) {
  const [isAboutOpen, setIsAboutOpen] = useState(false);
  const location = useLocation();

  return (
    <>
      <header
        className="glass-surface"
        style={{
          position: "sticky",
          top: 0,
          zIndex: 100,
          borderRadius: 0,
          borderLeft: "none",
          borderRight: "none",
          borderTop: "none",
          padding: "var(--space-3) var(--space-6)",
        }}
      >
        <div
          style={{
            maxWidth: "1360px",
            margin: "0 auto",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "var(--space-5)" }}>
            {backTo ? (
              <Link
                to={backTo}
                className="glass-control"
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "6px",
                  padding: "6px 14px",
                  fontSize: "14px",
                  fontFamily: "var(--font-ui)",
                  color: "var(--paper-100)",
                }}
              >
                ← {backLabel}
              </Link>
            ) : (
              <Link
                to="/"
                style={{
                  display: "flex",
                  alignItems: "baseline",
                  gap: "10px",
                }}
              >
                <span
                  style={{
                    fontFamily: "var(--font-display)",
                    fontSize: "26px",
                    letterSpacing: "-0.5px",
                    color: "var(--paper-100)",
                  }}
                >
                  PrismEd
                </span>
                <span
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "11px",
                    color: "var(--amber)",
                    textTransform: "uppercase",
                    letterSpacing: "1px",
                  }}
                >
                  Bench v3.0
                </span>
              </Link>
            )}

            {title && (
              <div style={{ display: "flex", alignItems: "baseline", gap: "var(--space-3)" }}>
                {catalogNumber && (
                  <span
                    style={{
                      fontFamily: "var(--font-mono)",
                      fontSize: "13px",
                      color: "var(--amber)",
                    }}
                  >
                    [{catalogNumber}]
                  </span>
                )}
                <h2 style={{ fontSize: "20px", color: "var(--paper-100)" }}>{title}</h2>
              </div>
            )}
          </div>

          <nav style={{ display: "flex", alignItems: "center", gap: "var(--space-4)" }}>
            <Link
              to="/"
              style={{
                fontSize: "14px",
                color: location.pathname === "/" ? "var(--paper-100)" : "var(--paper-500)",
                fontWeight: location.pathname === "/" ? 600 : 400,
                transition: "color var(--transition-fast)",
              }}
            >
              Specimens
            </Link>

            <Link
              to="/showcase"
              style={{
                fontSize: "14px",
                color: location.pathname.startsWith("/showcase") ? "var(--amber)" : "var(--paper-500)",
                fontWeight: location.pathname.startsWith("/showcase") ? 600 : 400,
                display: "inline-flex",
                alignItems: "center",
                gap: "4px",
                transition: "color var(--transition-fast)",
              }}
            >
              <span>Showcase</span>
              <span
                style={{
                  fontSize: "10px",
                  padding: "1px 6px",
                  borderRadius: "var(--radius-pill)",
                  background: "rgba(232, 163, 61, 0.15)",
                  color: "var(--amber)",
                  fontFamily: "var(--font-mono)",
                }}
              >
                all 22
              </span>
            </Link>

            <Link
              to="/scan"
              style={{
                fontSize: "14px",
                color: location.pathname.startsWith("/scan") ? "var(--teal)" : "var(--paper-500)",
                fontWeight: location.pathname.startsWith("/scan") ? 600 : 400,
                display: "inline-flex",
                alignItems: "center",
                gap: "4px",
                transition: "color var(--transition-fast)",
              }}
            >
              <span>Scanner</span>
              <span
                style={{
                  fontSize: "10px",
                  padding: "1px 6px",
                  borderRadius: "var(--radius-pill)",
                  background: "rgba(63, 184, 166, 0.15)",
                  color: "var(--teal)",
                  fontFamily: "var(--font-mono)",
                }}
              >
                preview
              </span>
            </Link>

            <Link
              to="/progress"
              style={{
                fontSize: "14px",
                color: location.pathname.startsWith("/progress") ? "var(--paper-100)" : "var(--paper-500)",
                fontWeight: location.pathname.startsWith("/progress") ? 600 : 400,
                transition: "color var(--transition-fast)",
              }}
            >
              Progress
            </Link>

            <button
              onClick={() => setIsAboutOpen(true)}
              className="glass-control"
              style={{
                width: "32px",
                height: "32px",
                borderRadius: "50%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "13px",
                fontFamily: "var(--font-mono)",
                color: "var(--paper-300)",
              }}
              title="About the Models & Licences"
              aria-label="About the models and licenses"
            >
              ℹ
            </button>
          </nav>
        </div>
        <div className="spectrum-rule" style={{ marginTop: "var(--space-3)" }} />
      </header>

      <AboutSheet isOpen={isAboutOpen} onClose={() => setIsAboutOpen(false)} />
    </>
  );
}
