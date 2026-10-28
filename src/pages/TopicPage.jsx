import React, { useState, useEffect, useCallback } from "react";
import { useParams, useSearchParams, Link } from "react-router-dom";
import HeaderBar from "../shared/HeaderBar";
import ModelViewer from "../features/viewer/ModelViewer";
import MarginNotes from "../features/viewer/MarginNotes";
import StateView from "../shared/StateView";
import { fetchTopicById } from "../api/topics";
import { getCatalogNumber } from "../shared/helpers";

export default function TopicPage() {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const fromScanner = searchParams.get("from") === "scanner";
  const initialHighlightPart = searchParams.get("highlight");

  const [topic, setTopic] = useState(null);
  const [selectedPartId, setSelectedPartId] = useState(null);
  const [hiddenPartIds, setHiddenPartIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadTopic = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchTopicById(id);
      setTopic(data);
      // Auto-select highlight part if specified from scanner, or default to first part
      if (data.parts && data.parts.length > 0) {
        if (initialHighlightPart && data.parts.some((p) => p.id === initialHighlightPart)) {
          setSelectedPartId(initialHighlightPart);
        } else {
          setSelectedPartId(data.parts[0].id);
        }
      }
      setHiddenPartIds([]);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [id, initialHighlightPart]);

  useEffect(() => {
    loadTopic();
  }, [loadTopic]);

  const handleToggleVisibility = useCallback((partId) => {
    setHiddenPartIds((prev) =>
      prev.includes(partId) ? prev.filter((id) => id !== partId) : [...prev, partId]
    );
  }, []);

  const handleIsolatePart = useCallback((partId) => {
    if (!topic || !topic.parts) return;
    const others = topic.parts.filter((p) => p.id !== partId).map((p) => p.id);
    setHiddenPartIds(others);
    setSelectedPartId(partId);
  }, [topic]);

  const handleShowAllParts = useCallback(() => {
    setHiddenPartIds([]);
  }, []);

  const selectedPart = topic?.parts?.find((p) => p.id === selectedPartId) || null;
  const selectedPartIndex = topic?.parts?.findIndex((p) => p.id === selectedPartId);
  const catalogNum = topic ? getCatalogNumber(topic.id, 0) : "";

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <HeaderBar
        backTo="/"
        backLabel="Specimens"
        title={topic?.name}
        catalogNumber={catalogNum}
      />

      <main style={{ maxWidth: "1360px", margin: "0 auto", padding: "var(--space-6)", width: "100%", flex: 1 }}>
        <StateView
          loading={loading}
          error={error}
          onRetry={loadTopic}
          emptyMessage="This topic is not on the bench."
          emptyAction={<Link to="/" style={{ color: "var(--amber)" }}>Return to Bench</Link>}
        >
          {topic && (
            <>
              {fromScanner && (
                <div
                  style={{
                    marginBottom: "var(--space-4)",
                    padding: "10px 18px",
                    borderRadius: "var(--radius-control)",
                    backgroundColor: "rgba(63, 184, 166, 0.12)",
                    border: "1px solid rgba(63, 184, 166, 0.35)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    flexWrap: "wrap",
                    gap: "8px",
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "14px", color: "var(--paper-100)" }}>
                    <span style={{ color: "var(--teal)" }}>⚡</span>
                    <span><strong>Opened from scanner match</strong></span>
                    {initialHighlightPart && (
                      <span style={{ fontFamily: "var(--font-mono)", fontSize: "12px", color: "var(--teal)" }}>
                        — focused part: <code style={{ color: "var(--amber)" }}>{initialHighlightPart}</code>
                      </span>
                    )}
                  </div>
                  <Link
                    to="/scan"
                    style={{
                      fontSize: "13px",
                      color: "var(--teal)",
                      textDecoration: "none",
                      fontWeight: 600,
                      display: "inline-flex",
                      alignItems: "center",
                      gap: "4px",
                    }}
                  >
                    ← Back to Scanner
                  </Link>
                </div>
              )}

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(360px, 1fr))",
                  gap: "var(--space-6)",
                  alignItems: "start",
                }}
              >
              {/* Left Column: 3D Viewer & Text Fallback List (§6.2, §6.7) */}
              <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-5)" }}>
                <ModelViewer
                  modelUrl={topic.modelUrl}
                  parts={topic.parts}
                  selectedPartId={selectedPartId}
                  onPartSelect={(pId) => setSelectedPartId(pId)}
                  discipline={topic.discipline}
                  autoRotate={topic.autoRotate}
                  animation={topic.animation}
                  hiddenPartIds={hiddenPartIds}
                  onToggleVisibility={handleToggleVisibility}
                  onIsolatePart={handleIsolatePart}
                  onShowAllParts={handleShowAllParts}
                />

                {/* Text Fallback & Part Visibility Index (§6.2, §6.7) */}
                <div
                  style={{
                    padding: "var(--space-4)",
                    borderRadius: "var(--radius-panel)",
                    backgroundColor: "rgba(30, 26, 23, 0.4)",
                    border: "1px solid rgba(244, 237, 225, 0.08)",
                  }}
                >
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
                        color: "var(--paper-500)",
                        textTransform: "uppercase",
                      }}
                    >
                      Specimen Component Hierarchy & Visibility (§6.2)
                    </span>

                    {hiddenPartIds.length > 0 && (
                      <button
                        onClick={handleShowAllParts}
                        className="glass-control"
                        style={{
                          padding: "3px 8px",
                          fontSize: "11px",
                          fontFamily: "var(--font-mono)",
                          color: "var(--amber)",
                        }}
                      >
                        Show All
                      </button>
                    )}
                  </div>

                  <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
                    {topic.parts.map((p, idx) => {
                      const isSel = p.id === selectedPartId;
                      const isHidden = hiddenPartIds.includes(p.id);

                      return (
                        <div
                          key={p.id}
                          style={{
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "space-between",
                            padding: "6px 12px",
                            borderRadius: "var(--radius-button)",
                            backgroundColor: isSel
                              ? "rgba(232, 163, 61, 0.15)"
                              : isHidden
                              ? "rgba(20, 17, 15, 0.3)"
                              : "rgba(244, 237, 225, 0.03)",
                            border: isSel
                              ? "1px solid var(--amber)"
                              : "1px solid rgba(244, 237, 225, 0.06)",
                            opacity: isHidden ? 0.45 : 1.0,
                            transition: "all var(--transition-fast)",
                          }}
                        >
                          {/* Part Name & Number Selector */}
                          <button
                            onClick={() => setSelectedPartId(p.id)}
                            style={{
                              background: "none",
                              border: "none",
                              color: isSel ? "var(--amber)" : "var(--paper-100)",
                              fontWeight: isSel ? 600 : 400,
                              fontSize: "13px",
                              fontFamily: "var(--font-ui)",
                              cursor: "pointer",
                              display: "flex",
                              alignItems: "center",
                              gap: "var(--space-2)",
                              textAlign: "left",
                              flex: 1,
                            }}
                          >
                            <span
                              style={{
                                fontFamily: "var(--font-mono)",
                                color: isSel ? "var(--amber)" : "var(--paper-500)",
                                fontSize: "12px",
                              }}
                            >
                              0{idx + 1}.
                            </span>
                            <span>{p.name}</span>
                          </button>

                          {/* Quick Actions: Visibility Toggle & Isolate (§6.2) */}
                          <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
                            <button
                              onClick={() => handleToggleVisibility(p.id)}
                              title={isHidden ? "Show part" : "Hide part"}
                              className="glass-control"
                              style={{
                                padding: "2px 8px",
                                fontSize: "12px",
                                background: "none",
                                border: "none",
                                color: isHidden ? "var(--paper-500)" : "var(--paper-100)",
                                cursor: "pointer",
                              }}
                            >
                              {isHidden ? "🙈 Hidden" : "👁 Visible"}
                            </button>

                            <button
                              onClick={() => handleIsolatePart(p.id)}
                              title="Isolate this part"
                              className="glass-control"
                              style={{
                                padding: "2px 8px",
                                fontSize: "11px",
                                fontFamily: "var(--font-mono)",
                                color: isSel ? "var(--amber)" : "var(--paper-500)",
                                borderColor: isSel ? "rgba(232, 163, 61, 0.3)" : "rgba(244, 237, 225, 0.1)",
                              }}
                            >
                              Isolate
                            </button>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>

              {/* Right Column: Margin Notes & Tutor Box */}
              <div>
                <MarginNotes
                  topicId={topic.id}
                  topicName={topic.name}
                  selectedPart={selectedPart}
                  partNumber={selectedPartIndex !== -1 ? selectedPartIndex + 1 : null}
                  totalParts={topic.parts.length}
                />
              </div>
            </div>
          </>
          )}
        </StateView>
      </main>
    </div>
  );
}
