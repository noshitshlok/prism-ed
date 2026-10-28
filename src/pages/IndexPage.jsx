import React, { useState, useEffect } from "react";
import HeaderBar from "../shared/HeaderBar";
import DisciplineChip from "../features/topics/DisciplineChip";
import SpecimenCard from "../features/topics/SpecimenCard";
import StateView from "../shared/StateView";
import { fetchTopics } from "../api/topics";

const DISCIPLINES = [
  "All",
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

export default function IndexPage() {
  const [topics, setTopics] = useState([]);
  const [selectedDiscipline, setSelectedDiscipline] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadTopics = async (disciplineFilter) => {
    setLoading(true);
    setError(null);
    try {
      const filters = disciplineFilter && disciplineFilter !== "All" ? { discipline: disciplineFilter } : {};
      const data = await fetchTopics(filters);
      setTopics(data || []);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTopics(selectedDiscipline);
  }, [selectedDiscipline]);

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <HeaderBar />

      <main style={{ maxWidth: "1360px", margin: "0 auto", padding: "var(--space-6) var(--space-6)", width: "100%", flex: 1 }}>
        {/* Intro Section */}
        <div style={{ marginBottom: "var(--space-6)" }}>
          <h1 style={{ fontSize: "44px", letterSpacing: "-1px", marginBottom: "var(--space-2)" }}>
            The Engineering Bench
          </h1>
          <p
            style={{
              fontFamily: "var(--font-body)",
              fontSize: "20px",
              color: "var(--paper-300)",
            }}
          >
            Open a specimen, then look at it from every side.
          </p>
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
          {DISCIPLINES.map((disc) => (
            <DisciplineChip
              key={disc}
              label={disc}
              isSelected={selectedDiscipline === disc}
              onClick={() => setSelectedDiscipline(disc)}
            />
          ))}
        </div>

        {/* Grid of Specimen Cards */}
        <StateView
          loading={loading}
          error={error}
          isEmpty={!loading && !error && topics.length === 0}
          emptyMessage="No specimens registered in this discipline yet."
          onRetry={() => loadTopics(selectedDiscipline)}
        >
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(380px, 1fr))",
              gap: "var(--space-5)",
            }}
          >
            {topics.map((t, idx) => (
              <SpecimenCard key={t.id} topic={t} index={idx} />
            ))}
          </div>
        </StateView>
      </main>
    </div>
  );
}
