import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import HeaderBar from "../shared/HeaderBar";
import GlassPanel from "../shared/GlassPanel";
import SpectrumBar from "../shared/SpectrumBar";
import StateView from "../shared/StateView";
import { fetchProgressSummary } from "../api/progress";
import { fetchTopics } from "../api/topics";

export default function ProgressPage() {
  const [summary, setSummary] = useState(null);
  const [topicsMap, setTopicsMap] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadProgress = async () => {
    setLoading(true);
    setError(null);
    try {
      const [prog, topicsList] = await Promise.all([
        fetchProgressSummary(),
        fetchTopics(),
      ]);
      setSummary(prog);

      const map = {};
      (topicsList || []).forEach((t) => {
        map[t.id] = t.name;
      });
      setTopicsMap(map);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProgress();
  }, []);

  const masteryItems = summary?.mastery || [];

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <HeaderBar backTo="/" backLabel="Specimens" title="Student Progress" />

      <main style={{ maxWidth: "900px", margin: "0 auto", padding: "var(--space-6) var(--space-4)", width: "100%", flex: 1 }}>
        <GlassPanel strong style={{ padding: "var(--space-6)", marginBottom: "var(--space-6)" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: "var(--space-4)" }}>
            <div>
              <h1 style={{ fontSize: "32px", color: "var(--paper-100)", marginBottom: "var(--space-1)" }}>
                Learning Progress
              </h1>
              <p style={{ fontSize: "15px", color: "var(--paper-500)", fontFamily: "var(--font-mono)" }}>
                Progress is stored on this browser only (Session: {summary?.sessionId?.slice(0, 8)}...).
              </p>
            </div>

            <div style={{ textAlign: "right" }}>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: "12px", color: "var(--paper-500)" }}>
                Total Attempts
              </div>
              <div style={{ fontFamily: "var(--font-display)", fontSize: "28px", color: "var(--amber)" }}>
                {summary?.totalAttempts || 0}
              </div>
            </div>
          </div>

          <StateView
            loading={loading}
            error={error}
            isEmpty={!loading && !error && masteryItems.length === 0}
            emptyMessage="No attempts yet. Take a quiz to start tracking topic mastery."
            emptyAction={
              <Link
                to="/"
                className="glass-control"
                style={{
                  display: "inline-block",
                  padding: "8px 20px",
                  background: "var(--amber)",
                  color: "var(--bench-900)",
                  fontWeight: 600,
                  fontSize: "14px",
                }}
              >
                Explore Topics →
              </Link>
            }
            onRetry={loadProgress}
          >
            <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-4)" }}>
              {masteryItems.map((item) => {
                const topicTitle = topicsMap[item.topicId] || item.topicId;
                const isMastered = item.bestPercentage >= 80;

                return (
                  <div
                    key={item.topicId}
                    style={{
                      padding: "var(--space-4)",
                      borderRadius: "var(--radius-control)",
                      backgroundColor: "rgba(244, 237, 225, 0.03)",
                      border: "1px solid rgba(244, 237, 225, 0.08)",
                    }}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: "var(--space-2)" }}>
                      <div>
                        <Link
                          to={`/topics/${item.topicId}`}
                          style={{
                            fontSize: "18px",
                            fontWeight: 600,
                            color: "var(--paper-100)",
                            fontFamily: "var(--font-ui)",
                          }}
                        >
                          {topicTitle}
                        </Link>
                        <span style={{ fontFamily: "var(--font-mono)", fontSize: "12px", color: "var(--paper-500)", marginLeft: "8px" }}>
                          ({item.attempts} {item.attempts === 1 ? "attempt" : "attempts"})
                        </span>
                      </div>

                      <div style={{ display: "flex", alignItems: "baseline", gap: "6px" }}>
                        <span
                          style={{
                            fontFamily: "var(--font-mono)",
                            fontSize: "16px",
                            fontWeight: 700,
                            color: isMastered ? "var(--moss)" : "var(--amber)",
                          }}
                        >
                          {item.bestPercentage}%
                        </span>
                        <span style={{ fontSize: "12px", color: "var(--paper-500)" }}>best</span>
                      </div>
                    </div>

                    <SpectrumBar progress={item.bestPercentage} height="4px" />
                  </div>
                );
              })}
            </div>
          </StateView>
        </GlassPanel>
      </main>
    </div>
  );
}
