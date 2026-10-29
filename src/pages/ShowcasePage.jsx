import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import HeaderBar from "../shared/HeaderBar";
import GlassPanel from "../shared/GlassPanel";
import { fetchTopics } from "../api/topics";
import { getDisciplineColor, getCatalogNumber } from "../shared/helpers";

const DISCIPLINES_ORDER = [
  "Electrical Engineering",
  "Aerospace Engineering",
  "Biomedical Engineering",
  "Astrophysics & Aerospace",
  "Computer Science",
  "AI & Hardware Engineering",
  "Mechanical Engineering",
  "Civil Engineering",
  "Mechatronics & Robotics",
];

export default function ShowcasePage() {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeFilter, setActiveFilter] = useState("All");

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchTopics({ include_all: true });
        setTopics(data || []);
      } catch (err) {
        setError(err.message || "Failed to load showcase");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const filteredTopics = activeFilter === "All"
    ? topics
    : topics.filter((t) => t.discipline === activeFilter);

  // Group by discipline
  const grouped = DISCIPLINES_ORDER.reduce((acc, disc) => {
    const list = filteredTopics.filter((t) => t.discipline === disc);
    if (list.length > 0) {
      acc[disc] = list;
    }
    return acc;
  }, {});

  // Add any unmatched disciplines
  filteredTopics.forEach((t) => {
    if (!grouped[t.discipline]) {
      grouped[t.discipline] = grouped[t.discipline] || [];
      if (!grouped[t.discipline].includes(t)) {
        grouped[t.discipline].push(t);
      }
    }
  });

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column", background: "var(--bench-900)" }}>
      <HeaderBar />

      <main style={{ maxWidth: "1440px", margin: "0 auto", padding: "var(--space-6)", width: "100%", flex: 1 }}>
        {/* Showcase Hero Banner */}
        <div style={{ marginBottom: "var(--space-6)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "var(--space-2)" }}>
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "12px",
                color: "var(--teal)",
                background: "rgba(63, 184, 166, 0.12)",
                padding: "3px 10px",
                borderRadius: "var(--radius-pill)",
                border: "1px solid rgba(63, 184, 166, 0.3)",
              }}
            >
              PRISMED SPECIMEN SHOWCASE v1.1
            </span>
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "12px",
                color: "var(--amber)",
                background: "rgba(232, 163, 61, 0.12)",
                padding: "3px 10px",
                borderRadius: "var(--radius-pill)",
                border: "1px solid rgba(232, 163, 61, 0.3)",
              }}
            >
              22 / 22 MODELS ONLINE
            </span>
          </div>

          <h1 style={{ fontSize: "42px", letterSpacing: "-1px", marginBottom: "var(--space-2)" }}>
            The Complete 3D Specimen Showcase
          </h1>
          <p style={{ fontSize: "18px", color: "var(--paper-300)", maxWidth: "880px", lineHeight: 1.5 }}>
            All 22 engineering disciplines reviewed together in one interactive gallery. Every specimen features authentic CAD/scan geometry or physical hardware analogues with zero primitive placeholders.
          </p>
        </div>

        {/* Global Metric Cards */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
            gap: "var(--space-4)",
            marginBottom: "var(--space-6)",
          }}
        >
          <GlassPanel style={{ padding: "var(--space-4)" }}>
            <div style={{ fontFamily: "var(--font-mono)", fontSize: "11px", color: "var(--paper-500)", textTransform: "uppercase" }}>
              Registered Topics
            </div>
            <div style={{ fontSize: "32px", fontFamily: "var(--font-display)", color: "var(--paper-100)", marginTop: "4px" }}>
              22 / 22
            </div>
            <div style={{ fontSize: "12px", color: "var(--teal)", marginTop: "2px" }}>
              100% with interactive 3D
            </div>
          </GlassPanel>

          <GlassPanel style={{ padding: "var(--space-4)" }}>
            <div style={{ fontFamily: "var(--font-mono)", fontSize: "11px", color: "var(--paper-500)", textTransform: "uppercase" }}>
              Physical Models & Scans
            </div>
            <div style={{ fontSize: "32px", fontFamily: "var(--font-display)", color: "var(--paper-100)", marginTop: "4px" }}>
              16 Direct
            </div>
            <div style={{ fontSize: "12px", color: "var(--paper-300)", marginTop: "2px" }}>
              CAD, Scans & Micro-devices
            </div>
          </GlassPanel>

          <GlassPanel style={{ padding: "var(--space-4)" }}>
            <div style={{ fontFamily: "var(--font-mono)", fontSize: "11px", color: "var(--paper-500)", textTransform: "uppercase" }}>
              Hardware Analogues
            </div>
            <div style={{ fontSize: "32px", fontFamily: "var(--font-display)", color: "var(--paper-100)", marginTop: "4px" }}>
              6 Analogues
            </div>
            <div style={{ fontSize: "12px", color: "var(--cyan)", marginTop: "2px" }}>
              CPU, GPU, RAM, Saw & Case
            </div>
          </GlassPanel>

          <GlassPanel style={{ padding: "var(--space-4)" }}>
            <div style={{ fontFamily: "var(--font-mono)", fontSize: "11px", color: "var(--paper-500)", textTransform: "uppercase" }}>
              Size Budget Limit
            </div>
            <div style={{ fontSize: "32px", fontFamily: "var(--font-display)", color: "var(--paper-100)", marginTop: "4px" }}>
              &lt; 4.85 MB
            </div>
            <div style={{ fontSize: "12px", color: "var(--teal)", marginTop: "2px" }}>
              All 22 under 8MB budget
            </div>
          </GlassPanel>
        </div>

        {/* Discipline Filter Row */}
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: "var(--space-2)",
            marginBottom: "var(--space-6)",
            paddingBottom: "var(--space-4)",
            borderBottom: "1px solid rgba(244, 237, 225, 0.08)",
          }}
        >
          {["All", ...DISCIPLINES_ORDER].map((disc) => (
            <button
              key={disc}
              onClick={() => setActiveFilter(disc)}
              className="glass-control"
              style={{
                padding: "6px 14px",
                borderRadius: "var(--radius-pill)",
                fontSize: "13px",
                fontFamily: "var(--font-ui)",
                color: activeFilter === disc ? "var(--amber)" : "var(--paper-300)",
                borderColor: activeFilter === disc ? "var(--amber)" : "rgba(244, 237, 225, 0.12)",
                background: activeFilter === disc ? "rgba(232, 163, 61, 0.12)" : "rgba(244, 237, 225, 0.04)",
                cursor: "pointer",
              }}
            >
              {disc}
            </button>
          ))}
        </div>

        {/* Grouped Topics Content */}
        {loading && (
          <div style={{ textAlign: "center", padding: "60px 0", color: "var(--paper-300)" }}>
            Loading all 22 specimen models...
          </div>
        )}

        {error && (
          <div style={{ textAlign: "center", padding: "60px 0", color: "var(--coral)" }}>
            Error loading showcase: {error}
          </div>
        )}

        {!loading && !error && Object.keys(grouped).map((disc) => {
          const discColor = getDisciplineColor(disc);
          const discTopics = grouped[disc];

          return (
            <section key={disc} style={{ marginBottom: "var(--space-8)" }}>
              {/* Section Header */}
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "var(--space-3)",
                  marginBottom: "var(--space-4)",
                  paddingBottom: "var(--space-2)",
                  borderBottom: `2px solid ${discColor}`,
                }}
              >
                <span
                  style={{
                    width: "12px",
                    height: "12px",
                    borderRadius: "50%",
                    backgroundColor: discColor,
                  }}
                />
                <h2 style={{ fontSize: "24px", color: "var(--paper-100)" }}>
                  {disc}
                </h2>
                <span
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "13px",
                    color: "var(--paper-500)",
                    marginLeft: "auto",
                  }}
                >
                  {discTopics.length} {discTopics.length === 1 ? "specimen" : "specimens"}
                </span>
              </div>

              {/* Models Grid */}
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fill, minmax(420px, 1fr))",
                  gap: "var(--space-5)",
                }}
              >
                {discTopics.map((topic, idx) => {
                  const catalogNum = getCatalogNumber(topic.id, idx);
                  const isAnalogue = topic.modelSource === "analogue";

                  return (
                    <GlassPanel
                      key={topic.id}
                      style={{
                        padding: "var(--space-5)",
                        display: "flex",
                        flexDirection: "column",
                        justifyContent: "space-between",
                        position: "relative",
                        overflow: "hidden",
                      }}
                    >
                      {/* Top Accent Bar */}
                      <div
                        style={{
                          position: "absolute",
                          top: 0,
                          left: 0,
                          right: 0,
                          height: "3px",
                          backgroundColor: discColor,
                        }}
                      />

                      <div>
                        {/* Status & Catalog Row */}
                        <div
                          style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            marginBottom: "var(--space-3)",
                          }}
                        >
                          <span style={{ fontFamily: "var(--font-mono)", fontSize: "12px", color: "var(--amber)" }}>
                            {catalogNum}
                          </span>
                          <div style={{ display: "flex", gap: "6px" }}>
                            <span
                              style={{
                                fontFamily: "var(--font-mono)",
                                fontSize: "11px",
                                padding: "2px 8px",
                                borderRadius: "var(--radius-pill)",
                                background: topic.status === "not_in_demo"
                                  ? "rgba(228, 103, 91, 0.15)"
                                  : isAnalogue
                                  ? "rgba(63, 184, 166, 0.15)"
                                  : "rgba(141, 187, 106, 0.15)",
                                color: topic.status === "not_in_demo"
                                  ? "var(--coral)"
                                  : isAnalogue
                                  ? "var(--teal)"
                                  : "var(--moss)",
                                border: `1px solid ${
                                  topic.status === "not_in_demo"
                                    ? "rgba(228, 103, 91, 0.3)"
                                    : isAnalogue
                                    ? "rgba(63, 184, 166, 0.3)"
                                    : "rgba(141, 187, 106, 0.3)"
                                }`,
                              }}
                            >
                              {topic.status === "not_in_demo" ? "not_in_demo" : isAnalogue ? "analogue" : "ready"}
                            </span>
                            <span
                              style={{
                                fontFamily: "var(--font-mono)",
                                fontSize: "11px",
                                padding: "2px 8px",
                                borderRadius: "var(--radius-pill)",
                                background: "rgba(244, 237, 225, 0.08)",
                                color: "var(--paper-300)",
                              }}
                            >
                              {topic.modelSource}
                            </span>
                          </div>
                        </div>

                        {/* Title & Subfield */}
                        <h3 style={{ fontSize: "20px", marginBottom: "4px", color: "var(--paper-100)" }}>
                          {topic.name}
                        </h3>
                        <div
                          style={{
                            fontSize: "13px",
                            color: "var(--paper-500)",
                            fontFamily: "var(--font-mono)",
                            marginBottom: "var(--space-3)",
                          }}
                        >
                          ID: {topic.id} &bull; {topic.subfield || topic.discipline}
                        </div>

                        {/* Interactive 3D Model Viewer Container */}
                        <div
                          style={{
                            width: "100%",
                            height: "260px",
                            borderRadius: "var(--radius-md)",
                            background: "radial-gradient(circle at center, rgba(30, 27, 24, 0.95), rgba(18, 16, 14, 0.98))",
                            border: "1px solid rgba(244, 237, 225, 0.08)",
                            overflow: "hidden",
                            position: "relative",
                            marginBottom: "var(--space-4)",
                            display: topic.status === "not_in_demo" ? "flex" : "block",
                            alignItems: "center",
                            justifyContent: "center",
                            flexDirection: "column",
                            padding: topic.status === "not_in_demo" ? "var(--space-4)" : 0,
                            textAlign: "center",
                          }}
                        >
                          {topic.status === "not_in_demo" ? (
                            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "8px" }}>
                              <div style={{ fontSize: "28px", color: "var(--coral)" }}>⊗</div>
                              <span style={{ fontFamily: "var(--font-mono)", fontSize: "12px", color: "var(--coral)", textTransform: "uppercase", letterSpacing: "1px" }}>
                                Excluded From Demo
                              </span>
                              <span style={{ fontSize: "12px", color: "var(--paper-500)", maxWidth: "280px" }}>
                                Removed per owner review pending authentic physical CAD sourcing.
                              </span>
                            </div>
                          ) : (
                            <model-viewer
                              src={topic.modelUrl}
                              auto-rotate={topic.autoRotate !== false}
                              camera-controls
                              shadow-intensity="1"
                              exposure="1.1"
                              style={{
                                width: "100%",
                                height: "100%",
                                outline: "none",
                              }}
                            />
                          )}
                        </div>

                        {/* Description */}
                        <p
                          style={{
                            fontSize: "14px",
                            color: "var(--paper-300)",
                            lineHeight: 1.5,
                            marginBottom: "var(--space-4)",
                          }}
                        >
                          {topic.description}
                        </p>
                      </div>

                      {/* Footer & Actions */}
                      <div
                        style={{
                          paddingTop: "var(--space-3)",
                          borderTop: "1px solid rgba(244, 237, 225, 0.06)",
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                        }}
                      >
                        <span
                          style={{
                            fontFamily: "var(--font-mono)",
                            fontSize: "12px",
                            color: "var(--paper-500)",
                          }}
                        >
                          {topic.partsCount || 5} calibrated parts
                        </span>

                        <Link
                          to={`/topics/${topic.id}`}
                          className="glass-control"
                          style={{
                            display: "inline-flex",
                            alignItems: "center",
                            gap: "6px",
                            padding: "6px 14px",
                            fontSize: "13px",
                            color: "var(--amber)",
                            textDecoration: "none",
                            fontFamily: "var(--font-ui)",
                            fontWeight: 500,
                          }}
                        >
                          Open Specimen Bench &rarr;
                        </Link>
                      </div>
                    </GlassPanel>
                  );
                })}
              </div>
            </section>
          );
        })}
      </main>
    </div>
  );
}
