import React, { useState, useEffect } from "react";
import GlassPanel from "./GlassPanel";
import { fetchTopics } from "../api/topics";

export default function AboutSheet({ isOpen, onClose }) {
  const [topics, setTopics] = useState([]);

  useEffect(() => {
    if (isOpen) {
      fetchTopics()
        .then((data) => setTopics(data || []))
        .catch(() => {});
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const attributions = [
    {
      title: "Circuit Board (Free Download)",
      source: "https://sketchfab.com/3d-models/circuit-board-free-download-95a287a99f1847648353b379373cf586",
      author: "Rowan Design",
      license: "CC-BY-4.0",
      notes: "Attribution: Model by Rowan Design under CC-BY-4.0."
    },
    {
      title: "Astronaut Extravehicular Mobility Unit (EMU)",
      source: "https://modelviewer.dev/shared-assets/models/Astronaut.glb",
      author: "Google model-viewer / Poly asset collection",
      license: "CC-BY-4.0",
      notes: "3D model courtesy of Google model-viewer project (Poly collection)."
    },
    {
      title: "Human Heart (Visible Human Project)",
      source: "https://3d.nih.gov/entries/3DPX-021000",
      author: "Kristen Browne; Heidi Schlehlein (NIH 3D)",
      license: "CC-BY-4.0",
      notes: "Anatomical heart derived from Visible Human Project dataset."
    },
    {
      title: "2-Cylinder Internal Combustion Engine",
      source: "https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/2CylinderEngine",
      author: "The Khronos Group Inc. & Contributors",
      license: "CC-BY-4.0",
      notes: "Four-stroke engine assembly with reciprocating kinematics."
    },
    {
      title: "Automotive Differential Gearbox Assembly",
      source: "https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/GearboxAssy",
      author: "The Khronos Group Inc. & Contributors",
      license: "CC-BY-4.0",
      notes: "Differential gearbox with planetary bevel pinions and housing."
    },
    {
      title: "Canadarm Shuttle Remote Manipulator System",
      source: "https://github.com/nasa/NASA-3D-Resources/tree/master/3D%20Models/Space%20Shuttle%20Remote%20Manipulator%20System%20(Canadarm)",
      author: "National Aeronautics and Space Administration (NASA)",
      license: "Public Domain",
      notes: "6-DOF articulated robotic arm manipulator from NASA 3D Resources."
    },
    {
      title: "Saturn V Multi-Stage Propulsion Booster",
      source: "https://github.com/nasa/NASA-3D-Resources/tree/master/3D%20Models/Saturn%20V",
      author: "National Aeronautics and Space Administration (NASA)",
      license: "Public Domain",
      notes: "High-thrust chemical rocket propulsion booster stages from NASA."
    },
    {
      title: "Parker Solar Probe Spacecraft",
      source: "https://github.com/nasa/NASA-3D-Resources/tree/master/3D%20Models/Parker%20Solar%20Probe",
      author: "NASA / Johns Hopkins University Applied Physics Laboratory",
      license: "Public Domain",
      notes: "Solar heliophysics probe exploring orbital mechanics around the Sun."
    },
    {
      title: "OpenStax Anatomy and Physiology 2e (Heart Diagram)",
      source: "https://openstax.org/books/anatomy-and-physiology-2e",
      author: "OpenStax, Rice University",
      license: "CC-BY-4.0",
      notes: "Cardiovascular figures licensed under Creative Commons Attribution 4.0 International."
    },
    {
      title: "OpenStax Astronomy 2e (Planetary Ephemerides)",
      source: "https://openstax.org/books/astronomy-2e",
      author: "OpenStax, Rice University",
      license: "CC-BY-4.0",
      notes: "Planetary orbit figures licensed under Creative Commons Attribution 4.0 International."
    },
    {
      title: "OpenStax University Physics Vol 2 (Circuit Schematic)",
      source: "https://openstax.org/books/university-physics-volume-2",
      author: "OpenStax, Rice University",
      license: "CC-BY-4.0",
      notes: "DC circuit schematics licensed under Creative Commons Attribution 4.0 International."
    }
  ];

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        backgroundColor: "rgba(20, 17, 15, 0.7)",
        backdropFilter: "blur(6px)",
        WebkitBackdropFilter: "blur(6px)",
        zIndex: 1000,
        display: "flex",
        justifyContent: "flex-end",
      }}
      onClick={onClose}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "520px",
          height: "100%",
          overflowY: "auto",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <GlassPanel
          strong
          style={{
            minHeight: "100%",
            borderRadius: "0",
            borderLeft: "var(--glass-border)",
            borderTop: "none",
            borderRight: "none",
            borderBottom: "none",
            padding: "var(--space-6)",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "var(--space-4)",
            }}
          >
            <h2 style={{ fontSize: "24px" }}>About the Models</h2>
            <button
              onClick={onClose}
              className="glass-control"
              style={{
                width: "36px",
                height: "36px",
                borderRadius: "50%",
                fontSize: "18px",
                lineHeight: "1",
              }}
              aria-label="Close About Sheet"
            >
              ✕
            </button>
          </div>

          <p
            style={{
              fontSize: "15px",
              color: "var(--paper-300)",
              marginBottom: "var(--space-5)",
            }}
          >
            PrismEd utilizes Creative Commons assets and OpenStax open educational resources. Below are the verified sources, licenses, and classification for all 22 models.
          </p>

          {/* Model Registry Classification (§1, §7.2 Fix #6) */}
          <div style={{ marginBottom: "var(--space-6)" }}>
            <h3 style={{ fontSize: "18px", color: "var(--paper-100)", marginBottom: "var(--space-3)" }}>
              Model Source Classification ({topics.length} specimens)
            </h3>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "1fr",
                gap: "var(--space-2)",
                maxHeight: "260px",
                overflowY: "auto",
                paddingRight: "var(--space-2)",
              }}
            >
              {topics.map((t) => (
                <div
                  key={t.id}
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    padding: "6px 12px",
                    borderRadius: "var(--radius-control)",
                    backgroundColor: "rgba(244, 237, 225, 0.03)",
                    border: "1px solid rgba(244, 237, 225, 0.06)",
                    fontSize: "13px",
                  }}
                >
                  <span style={{ color: "var(--paper-100)" }}>{t.name}</span>
                  <span
                    style={{
                      fontFamily: "var(--font-mono)",
                      fontSize: "11px",
                      padding: "2px 6px",
                      borderRadius: "var(--radius-pill)",
                      backgroundColor:
                        t.modelSource === "uploaded"
                          ? "rgba(232, 163, 61, 0.15)"
                          : "rgba(63, 184, 166, 0.15)",
                      color:
                        t.modelSource === "uploaded"
                          ? "var(--amber)"
                          : "var(--teal)",
                      textTransform: "uppercase",
                    }}
                  >
                    {t.modelSource || "generated"}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* External Licences */}
          <h3 style={{ fontSize: "18px", color: "var(--paper-100)", marginBottom: "var(--space-3)" }}>
            Primary Attributions & Licences
          </h3>
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-4)" }}>
            {attributions.map((item, idx) => (
              <div
                key={idx}
                style={{
                  padding: "var(--space-4)",
                  borderRadius: "var(--radius-control)",
                  background: "rgba(244, 237, 225, 0.03)",
                  border: "1px solid rgba(244, 237, 225, 0.08)",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "baseline",
                    marginBottom: "var(--space-1)",
                  }}
                >
                  <h4 style={{ fontSize: "16px", color: "var(--paper-100)" }}>{item.title}</h4>
                  <span
                    style={{
                      fontFamily: "var(--font-mono)",
                      fontSize: "12px",
                      color: "var(--teal)",
                    }}
                  >
                    {item.license}
                  </span>
                </div>
                <div
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "12px",
                    color: "var(--paper-500)",
                    marginBottom: "var(--space-2)",
                  }}
                >
                  Author: {item.author}
                </div>
                <p style={{ fontSize: "14px", color: "var(--paper-300)", lineHeight: 1.5 }}>
                  {item.notes}
                </p>
                {item.source && (
                  <a
                    href={item.source}
                    target="_blank"
                    rel="noreferrer"
                    style={{
                      display: "inline-block",
                      marginTop: "var(--space-2)",
                      fontFamily: "var(--font-mono)",
                      fontSize: "12px",
                      color: "var(--amber)",
                    }}
                  >
                    View Source ↗
                  </a>
                )}
              </div>
            ))}
          </div>

          {/* Section: Diagram Scanner Reference Images (§5.5) */}
          <div style={{ marginTop: "var(--space-6)", paddingTop: "var(--space-5)", borderTop: "1px solid rgba(244, 237, 225, 0.12)" }}>
            <h3 style={{ fontSize: "18px", color: "var(--paper-100)", marginBottom: "var(--space-2)", fontFamily: "var(--font-display)" }}>
              Diagram Scanner (Preview) References
            </h3>
            <p style={{ fontSize: "14px", color: "var(--paper-300)", lineHeight: 1.5, marginBottom: "var(--space-3)" }}>
              Marker images are rendered from PrismEd&apos;s own 3D models.
            </p>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "var(--space-3)" }}>
              <div style={{ padding: "var(--space-3)", borderRadius: "var(--radius-control)", backgroundColor: "rgba(244, 237, 225, 0.03)", border: "1px solid rgba(244, 237, 225, 0.08)" }}>
                <div style={{ fontSize: "13px", color: "var(--paper-100)", fontWeight: 500 }}>Printed Circuit Board</div>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: "11px", color: "var(--teal)" }}>Project 3D Render • CC-BY-4.0</div>
              </div>
              <div style={{ padding: "var(--space-3)", borderRadius: "var(--radius-control)", backgroundColor: "rgba(244, 237, 225, 0.03)", border: "1px solid rgba(244, 237, 225, 0.08)" }}>
                <div style={{ fontSize: "13px", color: "var(--paper-100)", fontWeight: 500 }}>Differential Gearbox</div>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: "11px", color: "var(--teal)" }}>Project 3D Render • CC-BY-4.0</div>
              </div>
              <div style={{ padding: "var(--space-3)", borderRadius: "var(--radius-control)", backgroundColor: "rgba(244, 237, 225, 0.03)", border: "1px solid rgba(244, 237, 225, 0.08)" }}>
                <div style={{ fontSize: "13px", color: "var(--paper-100)", fontWeight: 500 }}>Four-Stroke IC Engine</div>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: "11px", color: "var(--teal)" }}>Project 3D Render • CC-BY-4.0</div>
              </div>
            </div>
          </div>
        </GlassPanel>
      </div>
    </div>
  );
}
