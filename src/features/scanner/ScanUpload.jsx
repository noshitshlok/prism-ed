import React, { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import GlassPanel from "../../shared/GlassPanel";
import { matchTextbookPhoto, fetchSupportedMarkers } from "../../api/scanner";

export default function ScanUpload() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [matchResult, setMatchResult] = useState(null);
  const [errorState, setErrorState] = useState(null);
  const [supportedMarkers, setSupportedMarkers] = useState([]);
  const [loadingMarkers, setLoadingMarkers] = useState(true);

  const takePhotoInputRef = useRef(null);
  const uploadFileInputRef = useRef(null);

  useEffect(() => {
    async function loadMarkers() {
      try {
        setLoadingMarkers(true);
        const res = await fetchSupportedMarkers();
        const list = res?.markers || res || [];
        setSupportedMarkers(list);
      } catch (err) {
        console.error("Failed to load markers:", err);
      } finally {
        setLoadingMarkers(false);
      }
    }
    loadMarkers();
  }, []);

  const handleSelectFile = (selected) => {
    if (selected) {
      setFile(selected);
      setPreviewUrl(URL.createObjectURL(selected));
      setMatchResult(null);
      setErrorState(null);
    }
  };

  const handleScan = async (fileToScan = file) => {
    if (!fileToScan) return;
    setIsScanning(true);
    setMatchResult(null);
    setErrorState(null);

    try {
      const res = await matchTextbookPhoto(fileToScan);
      setMatchResult(res);
    } catch (err) {
      console.error("Scanner error:", err);
      const detail = err.response?.data?.error?.message || "Failed to process photo with the scanner service.";
      setErrorState(detail);
    } finally {
      setIsScanning(false);
    }
  };

  const getConfidenceWord = (confidence) => {
    if (confidence >= 0.70) return { word: "strong", color: "var(--moss)", bg: "rgba(141, 187, 106, 0.15)" };
    if (confidence >= 0.40) return { word: "good", color: "var(--teal)", bg: "rgba(63, 184, 166, 0.15)" };
    return { word: "weak", color: "var(--amber)", bg: "rgba(232, 163, 61, 0.15)" };
  };

  return (
    <div style={{ maxWidth: "860px", margin: "0 auto", padding: "var(--space-6) var(--space-4)" }}>
      {/* Scanner Main Glass Card */}
      <GlassPanel strong style={{ padding: "var(--space-7)", marginBottom: "var(--space-6)" }}>
        {/* Header with Title and Preview Badge */}
        <div style={{ marginBottom: "var(--space-5)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "var(--space-2)" }}>
            <h1 style={{ fontSize: "32px", color: "var(--paper-100)", margin: 0, fontFamily: "var(--font-display)" }}>
              Scanner
            </h1>
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "12px",
                padding: "3px 10px",
                borderRadius: "var(--radius-pill)",
                backgroundColor: "rgba(63, 184, 166, 0.18)",
                color: "var(--teal)",
                letterSpacing: "0.5px",
                textTransform: "uppercase",
                fontWeight: 600,
              }}
            >
              Preview
            </span>
          </div>
          <p style={{ fontSize: "16px", color: "var(--paper-300)", lineHeight: 1.5, margin: 0 }}>
            Point your camera at one of the diagrams below, or upload a photo of it.
          </p>
        </div>

        {/* Hidden File Inputs */}
        <input
          type="file"
          accept="image/*"
          capture="environment"
          ref={takePhotoInputRef}
          style={{ display: "none" }}
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) {
              handleSelectFile(f);
            }
          }}
        />
        <input
          type="file"
          accept="image/*"
          ref={uploadFileInputRef}
          style={{ display: "none" }}
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) {
              handleSelectFile(f);
            }
          }}
        />

        {/* Actions Panel */}
        <div
          style={{
            border: "2px dashed rgba(244, 237, 225, 0.20)",
            borderRadius: "var(--radius-panel)",
            backgroundColor: "rgba(244, 237, 225, 0.02)",
            padding: "var(--space-6) var(--space-4)",
            textAlign: "center",
            marginBottom: "var(--space-5)",
          }}
        >
          {previewUrl ? (
            <div style={{ marginBottom: "var(--space-4)" }}>
              <img
                src={previewUrl}
                alt="Selected query photograph"
                style={{
                  maxHeight: "260px",
                  maxWidth: "100%",
                  borderRadius: "var(--radius-control)",
                  border: "1px solid rgba(244, 237, 225, 0.25)",
                  boxShadow: "0 8px 24px rgba(0, 0, 0, 0.35)",
                  marginBottom: "var(--space-3)",
                  objectFit: "contain",
                }}
              />
              <div style={{ fontFamily: "var(--font-mono)", fontSize: "13px", color: "var(--amber)" }}>
                Selected: {file?.name}
              </div>
            </div>
          ) : (
            <div style={{ marginBottom: "var(--space-5)" }}>
              <div style={{ fontSize: "42px", marginBottom: "var(--space-2)" }}>📷</div>
              <div style={{ fontSize: "16px", color: "var(--paper-100)", fontWeight: 500, marginBottom: "4px" }}>
                Capture or upload an engineering diagram
              </div>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: "12px", color: "var(--paper-500)" }}>
                Supports camera capture, PNG, JPEG, WebP (up to 5 MB)
              </div>
            </div>
          )}

          {/* Action Buttons: Take Photo & Upload Photo */}
          <div style={{ display: "flex", gap: "var(--space-3)", justifyContent: "center", flexWrap: "wrap" }}>
            <button
              type="button"
              onClick={() => takePhotoInputRef.current?.click()}
              className="glass-control"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                padding: "10px 22px",
                backgroundColor: "rgba(232, 163, 61, 0.15)",
                color: "var(--amber)",
                borderColor: "rgba(232, 163, 61, 0.4)",
                fontWeight: 600,
                fontSize: "14px",
              }}
            >
              <span>📸</span> Take photo
            </button>

            <button
              type="button"
              onClick={() => uploadFileInputRef.current?.click()}
              className="glass-control"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                padding: "10px 22px",
                backgroundColor: "rgba(244, 237, 225, 0.08)",
                color: "var(--paper-100)",
                fontWeight: 500,
                fontSize: "14px",
              }}
            >
              <span>📁</span> Upload photo
            </button>

            {file && (
              <button
                type="button"
                onClick={() => handleScan(file)}
                disabled={isScanning}
                className="glass-control"
                style={{
                  padding: "10px 28px",
                  backgroundColor: "var(--teal)",
                  color: "var(--bench-900)",
                  fontWeight: 600,
                  fontSize: "14px",
                  opacity: isScanning ? 0.6 : 1,
                  boxShadow: "0 0 16px rgba(63, 184, 166, 0.35)",
                }}
              >
                {isScanning ? "Processing Features..." : "Match Diagram →"}
              </button>
            )}
          </div>
        </div>

        {/* Scanning Progress State */}
        {isScanning && (
          <GlassPanel
            style={{
              padding: "var(--space-5)",
              textAlign: "center",
              marginBottom: "var(--space-5)",
              border: "1px solid rgba(63, 184, 166, 0.3)",
              backgroundColor: "rgba(63, 184, 166, 0.05)",
            }}
          >
            <div style={{ display: "inline-block", fontSize: "24px", marginBottom: "var(--space-2)" }}>⚡</div>
            <div style={{ fontSize: "15px", color: "var(--paper-100)", fontWeight: 500, marginBottom: "4px" }}>
              Scanning diagram features & estimating RANSAC homography...
            </div>
            <div style={{ fontFamily: "var(--font-mono)", fontSize: "12px", color: "var(--teal)" }}>
              Comparing query descriptors against verified 3D specimen database
            </div>
          </GlassPanel>
        )}

        {/* Error State with Retry Button */}
        {errorState && (
          <GlassPanel
            style={{
              padding: "var(--space-5)",
              marginBottom: "var(--space-5)",
              borderLeft: "4px solid var(--coral)",
              backgroundColor: "rgba(228, 103, 91, 0.08)",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <h4 style={{ color: "var(--coral)", fontSize: "16px", margin: "0 0 4px 0" }}>
                  Scanner request failed
                </h4>
                <p style={{ fontSize: "14px", color: "var(--paper-300)", margin: 0 }}>
                  {errorState}
                </p>
              </div>
              <button
                type="button"
                onClick={() => handleScan(file)}
                className="glass-control"
                style={{
                  padding: "6px 16px",
                  fontSize: "13px",
                  backgroundColor: "rgba(228, 103, 91, 0.2)",
                  color: "var(--coral)",
                }}
              >
                Retry
              </button>
            </div>
          </GlassPanel>
        )}

        {/* Match Result Panel */}
        {matchResult && (
          <div style={{ marginTop: "var(--space-4)" }}>
            {matchResult.matched ? (
              <GlassPanel
                style={{
                  borderLeft: "4px solid var(--moss)",
                  backgroundColor: "rgba(141, 187, 106, 0.08)",
                  padding: "var(--space-5)",
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "var(--space-3)", flexWrap: "wrap", gap: "8px" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                    <span
                      style={{
                        fontFamily: "var(--font-mono)",
                        fontSize: "12px",
                        color: "var(--moss)",
                        fontWeight: 600,
                        backgroundColor: "rgba(141, 187, 106, 0.15)",
                        padding: "2px 8px",
                        borderRadius: "var(--radius-pill)",
                      }}
                    >
                      ✓ Match Confirmed
                    </span>
                    {(() => {
                      const conf = getConfidenceWord(matchResult.confidence);
                      return (
                        <span
                          style={{
                            fontFamily: "var(--font-mono)",
                            fontSize: "12px",
                            color: conf.color,
                            backgroundColor: conf.bg,
                            padding: "2px 8px",
                            borderRadius: "var(--radius-pill)",
                          }}
                        >
                          Confidence: {conf.word} ({Math.round(matchResult.confidence * 100)}%)
                        </span>
                      );
                    })()}
                  </div>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: "12px", color: "var(--paper-500)" }}>
                    {matchResult.inliers} RANSAC inliers
                  </span>
                </div>

                <div style={{ display: "flex", gap: "var(--space-4)", alignItems: "center", marginBottom: "var(--space-4)", flexWrap: "wrap" }}>
                  {matchResult.markerId && (
                    <img
                      src={`/api/v1/scanner/markers/${matchResult.markerId}/thumbnail`}
                      alt="Matched Marker Reference"
                      style={{
                        width: "120px",
                        height: "90px",
                        objectFit: "cover",
                        borderRadius: "var(--radius-control)",
                        border: "1px solid rgba(244, 237, 225, 0.2)",
                        backgroundColor: "#ffffff",
                      }}
                    />
                  )}
                  <div style={{ flex: 1, minWidth: "220px" }}>
                    <h3 style={{ fontSize: "22px", color: "var(--paper-100)", margin: "0 0 4px 0", fontFamily: "var(--font-display)" }}>
                      {matchResult.topicName || matchResult.topicId}
                    </h3>
                    <p style={{ fontSize: "14px", color: "var(--paper-300)", margin: "0 0 6px 0" }}>
                      {matchResult.message}
                    </p>
                    {matchResult.highlightPartId && (
                      <div style={{ fontFamily: "var(--font-mono)", fontSize: "12px", color: "var(--amber)" }}>
                        Focus Part: <span style={{ textDecoration: "underline" }}>{matchResult.highlightPartId}</span>
                      </div>
                    )}
                  </div>
                </div>

                <Link
                  to={`/topics/${matchResult.topicId}?from=scanner${matchResult.highlightPartId ? `&highlight=${matchResult.highlightPartId}` : ""}`}
                  className="glass-control"
                  style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: "8px",
                    padding: "10px 24px",
                    backgroundColor: "var(--amber)",
                    color: "var(--bench-900)",
                    fontWeight: 600,
                    fontSize: "14px",
                    textDecoration: "none",
                  }}
                >
                  <span>Open 3D Model</span>
                  <span>→</span>
                </Link>
              </GlassPanel>
            ) : (
              <GlassPanel
                style={{
                  borderLeft: "4px solid var(--coral)",
                  backgroundColor: "rgba(228, 103, 91, 0.08)",
                  padding: "var(--space-5)",
                }}
              >
                <h4 style={{ color: "var(--coral)", fontSize: "17px", margin: "0 0 6px 0" }}>
                  No match found
                </h4>
                <p style={{ fontSize: "15px", color: "var(--paper-300)", margin: "0 0 var(--space-3) 0" }}>
                  No match. Try a closer photo in better light, or choose a diagram from the list below.
                </p>
                <button
                  type="button"
                  onClick={() => {
                    setFile(null);
                    setPreviewUrl(null);
                    setMatchResult(null);
                  }}
                  className="glass-control"
                  style={{
                    padding: "6px 16px",
                    fontSize: "13px",
                    color: "var(--paper-100)",
                  }}
                >
                  Clear and try another photo
                </button>
              </GlassPanel>
            )}
          </div>
        )}
      </GlassPanel>

      {/* Supported Marker Diagrams Catalogue Grid */}
      <div style={{ marginTop: "var(--space-7)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: "var(--space-4)" }}>
          <h2 style={{ fontSize: "22px", color: "var(--paper-100)", margin: 0, fontFamily: "var(--font-display)" }}>
            Supported Diagrams (Preview)
          </h2>
          <span style={{ fontFamily: "var(--font-mono)", fontSize: "12px", color: "var(--paper-500)" }}>
            Tap any card to view model directly
          </span>
        </div>

        {loadingMarkers ? (
          <div style={{ padding: "var(--space-5)", textAlign: "center", color: "var(--paper-500)", fontFamily: "var(--font-mono)" }}>
            Loading supported preview markers...
          </div>
        ) : (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
              gap: "var(--space-4)",
            }}
          >
            {supportedMarkers.map((m) => {
              const markerKey = m.markerId || m.id;
              const linkUrl = `/topics/${m.topicId}?from=scanner${m.highlightPartId ? `&highlight=${m.highlightPartId}` : ""}`;
              const thumbSrc = m.thumbnailUrl || `/api/v1/scanner/markers/${markerKey}/thumbnail`;

              return (
                <Link
                  key={markerKey}
                  to={linkUrl}
                  style={{ textDecoration: "none", color: "inherit", outline: "none" }}
                >
                  <GlassPanel
                    className="marker-card"
                    style={{
                      padding: "var(--space-4)",
                      height: "100%",
                      display: "flex",
                      flexDirection: "column",
                      justifyContent: "space-between",
                      transition: "transform var(--transition-fast), border-color var(--transition-fast)",
                      cursor: "pointer",
                    }}
                  >
                    <div>
                      {/* Thumbnail Image */}
                      <div
                        style={{
                          width: "100%",
                          height: "140px",
                          borderRadius: "var(--radius-control)",
                          overflow: "hidden",
                          backgroundColor: "#fbf9f5",
                          marginBottom: "var(--space-3)",
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          border: "1px solid rgba(244, 237, 225, 0.15)",
                        }}
                      >
                        <img
                          src={thumbSrc}
                          alt={m.displayName}
                          style={{
                            maxWidth: "100%",
                            maxHeight: "100%",
                            objectFit: "contain",
                          }}
                        />
                      </div>

                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "4px" }}>
                        <span style={{ fontFamily: "var(--font-mono)", fontSize: "11px", color: "var(--teal)" }}>
                          {markerKey}
                        </span>
                        <span
                          style={{
                            fontFamily: "var(--font-mono)",
                            fontSize: "10px",
                            padding: "1px 6px",
                            borderRadius: "var(--radius-pill)",
                            backgroundColor: "rgba(244, 237, 225, 0.08)",
                            color: "var(--paper-300)",
                          }}
                        >
                          3D specimen
                        </span>
                      </div>

                      <h4 style={{ fontSize: "17px", color: "var(--paper-100)", margin: "4px 0 6px 0", lineHeight: 1.3 }}>
                        {m.displayName}
                      </h4>
                    </div>

                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        marginTop: "var(--space-3)",
                        paddingTop: "var(--space-2)",
                        borderTop: "1px solid rgba(244, 237, 225, 0.08)",
                      }}
                    >
                      <span style={{ fontSize: "12px", fontFamily: "var(--font-mono)", color: "var(--paper-500)" }}>
                        Part: {m.highlightPartId || "default"}
                      </span>
                      <span style={{ fontSize: "13px", color: "var(--amber)", fontWeight: 500 }}>
                        Open model →
                      </span>
                    </div>
                  </GlassPanel>
                </Link>
              );
            })}
          </div>
        )}
      </div>

      <style>{`
        .marker-card:hover {
          transform: translateY(-2px);
          border-color: rgba(232, 163, 61, 0.35);
          box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        }
      `}</style>
    </div>
  );
}
