import React, { useRef, useEffect, useState, useCallback } from "react";
import { getDisciplineColor } from "../../shared/helpers";

export default function ModelViewer({
  modelUrl,
  parts = [],
  selectedPartId = null,
  onPartSelect = () => {},
  discipline = "Engineering",
  autoRotate = false,
  animation = null,
  hiddenPartIds = [],
  _onToggleVisibility = () => {},
  _onIsolatePart = () => {},
  onShowAllParts = () => {},
}) {
  const viewerRef = useRef(null);
  const [canAr, setCanAr] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);
  const [isRotating, setIsRotating] = useState(autoRotate);
  const [isPlayingAnim, setIsPlayingAnim] = useState(Boolean(animation));
  const [explodeValue, setExplodeValue] = useState(0);

  const disciplineColor = getDisciplineColor(discipline);
  const hasExplode = parts.some((p) => p.explodeOffset);

  // Sync autoRotate prop changes
  useEffect(() => {
    setIsRotating(autoRotate);
  }, [autoRotate]);

  // Escape key clears selection (§6.1)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "Escape") {
        onPartSelect(null);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [onPartSelect]);

  // Model-viewer lifecycle listeners (load, error, ar)
  useEffect(() => {
    const viewer = viewerRef.current;
    if (!viewer) return;

    setIsLoading(true);
    setHasError(false);

    const handleLoad = () => {
      setIsLoading(false);
      setHasError(false);
      if (viewer.canActivateAR) {
        setCanAr(true);
      }
    };

    const handleError = () => {
      setIsLoading(false);
      setHasError(true);
    };

    viewer.addEventListener("load", handleLoad);
    viewer.addEventListener("error", handleError);

    return () => {
      viewer.removeEventListener("load", handleLoad);
      viewer.removeEventListener("error", handleError);
    };
  }, [modelUrl]);

  // Reset Camera View (§6.5)
  const handleResetView = useCallback(() => {
    const viewer = viewerRef.current;
    if (!viewer) return;
    if (viewer.resetTurntableRotation) {
      viewer.resetTurntableRotation();
    }
    viewer.cameraOrbit = "0deg 75deg 105%";
    viewer.cameraTarget = "auto auto auto";
  }, []);

  // Toggle Animation Play/Pause (§6.4)
  const handleTogglePlay = useCallback(() => {
    const viewer = viewerRef.current;
    if (!viewer) return;
    if (isPlayingAnim) {
      if (viewer.pause) viewer.pause();
      setIsPlayingAnim(false);
    } else {
      if (viewer.play) viewer.play();
      setIsPlayingAnim(true);
    }
  }, [isPlayingAnim]);

  // Toggle Auto-rotate (§6.5)
  const handleToggleRotate = useCallback(() => {
    setIsRotating((prev) => !prev);
  }, []);

  // Calculate dynamic hotspot position for exploded view (§6.3)
  const calculatePosition = (part) => {
    if (!part.explodeOffset || explodeValue === 0) {
      return part.hotspotPosition;
    }
    const parse = (s) => (s.match(/[-+]?(?:\d*\.\d+|\d+)/g) || []).map(Number);
    const base = parse(part.hotspotPosition);
    const offset = parse(part.explodeOffset);
    if (base.length < 3 || offset.length < 3) return part.hotspotPosition;

    const x = (base[0] + offset[0] * explodeValue).toFixed(3);
    const y = (base[1] + offset[1] * explodeValue).toFixed(3);
    const z = (base[2] + offset[2] * explodeValue).toFixed(3);
    return `${x}m ${y}m ${z}m`;
  };

  const handleLaunchAR = () => {
    if (viewerRef.current && viewerRef.current.activateAR) {
      viewerRef.current.activateAR();
    }
  };

  const handleRetry = () => {
    const viewer = viewerRef.current;
    if (viewer) {
      setHasError(false);
      setIsLoading(true);
      const cur = viewer.src;
      viewer.src = "";
      setTimeout(() => {
        viewer.src = cur;
      }, 50);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)", width: "100%" }}>
      {/* 3D Canvas Frame - Solid bench-800 to prevent WebGL backdrop-filter blur overhead */}
      <div
        style={{
          width: "100%",
          height: "540px",
          backgroundColor: "var(--bench-800)",
          border: "1px solid rgba(244, 237, 225, 0.12)",
          borderRadius: "var(--radius-panel)",
          position: "relative",
          overflow: "hidden",
        }}
        onClick={(e) => {
          // If user clicked the canvas background rather than a pin, deselect (§6.1)
          if (e.target.tagName.toLowerCase() === "model-viewer") {
            onPartSelect(null);
          }
        }}
      >
        {/* Loading Spinner State */}
        {isLoading && !hasError && (
          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              backgroundColor: "rgba(20, 17, 15, 0.75)",
              backdropFilter: "blur(4px)",
              zIndex: 20,
              gap: "var(--space-3)",
            }}
          >
            <div
              style={{
                width: "36px",
                height: "36px",
                border: "3px solid rgba(244, 237, 225, 0.15)",
                borderTopColor: "var(--amber)",
                borderRadius: "50%",
                animation: "spin 1s linear infinite",
              }}
            />
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "13px",
                color: "var(--paper-100)",
                letterSpacing: "0.05em",
              }}
            >
              Mounting 3D Specimen...
            </span>
            <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
          </div>
        )}

        {/* Error State with Retry Button */}
        {hasError && (
          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              backgroundColor: "rgba(20, 17, 15, 0.9)",
              zIndex: 20,
              padding: "var(--space-4)",
              textAlign: "center",
              gap: "var(--space-3)",
            }}
          >
            <span style={{ fontSize: "28px" }}>⚠️</span>
            <span style={{ color: "var(--paper-100)", fontWeight: 600 }}>
              Could not load 3D asset
            </span>
            <button
              onClick={handleRetry}
              className="glass-control"
              style={{
                padding: "8px 18px",
                background: "var(--amber)",
                color: "var(--bench-900)",
                fontWeight: 600,
              }}
            >
              Retry Loading
            </button>
          </div>
        )}

        <model-viewer
          ref={viewerRef}
          src={modelUrl}
          camera-controls
          touch-action="pan-y"
          interaction-prompt="auto"
          shadow-intensity="1"
          exposure="1.0"
          auto-rotate={isRotating ? "" : undefined}
          animation-name={animation || undefined}
          autoplay={isPlayingAnim ? "" : undefined}
          ar
          ar-modes="webxr scene-viewer quick-look"
          style={{ width: "100%", height: "100%", outline: "none", backgroundColor: "transparent" }}
        >
          {/* Pins as HTML annotations positioned via data-position & data-normal (§6.6) */}
          {parts.map((part, index) => {
            const isSelected = selectedPartId === part.id;
            const isHidden = hiddenPartIds.includes(part.id);
            const pinNum = index + 1;
            const normal = part.hotspotNormal || "0m 1m 0m";
            const pos = calculatePosition(part);

            return (
              <button
                key={part.id}
                slot={`hotspot-${part.id}`}
                data-position={pos}
                data-normal={normal}
                onClick={(e) => {
                  e.stopPropagation();
                  onPartSelect(part.id);
                }}
                aria-label={`Part ${pinNum}: ${part.name}`}
                style={{
                  width: isSelected ? "32px" : "28px",
                  height: isSelected ? "32px" : "28px",
                  borderRadius: "50%",
                  backgroundColor: isHidden
                    ? "rgba(100, 95, 90, 0.5)"
                    : isSelected
                    ? "var(--amber)"
                    : disciplineColor,
                  color: isHidden ? "rgba(244, 237, 225, 0.5)" : "var(--bench-900)",
                  fontFamily: "var(--font-mono)",
                  fontWeight: 700,
                  fontSize: isSelected ? "13px" : "12px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  border: isHidden
                    ? "1px dashed rgba(244, 237, 225, 0.3)"
                    : "2px solid var(--paper-100)",
                  opacity: isHidden ? 0.35 : 1.0,
                  boxShadow: isSelected
                    ? `0 0 16px var(--amber), 0 0 24px rgba(232, 163, 61, 0.4)`
                    : isHidden
                    ? "none"
                    : `0 0 10px ${disciplineColor}`,
                  cursor: "pointer",
                  transition: "all var(--transition-fast)",
                  transform: "translate(-50%, -50%)",
                }}
              >
                {pinNum}
              </button>
            );
          })}
        </model-viewer>

        {/* Top-Right Quick Controls: Reset, Auto-rotate, Play/Pause (§6.4, §6.5) */}
        <div
          style={{
            position: "absolute",
            top: "var(--space-3)",
            right: "var(--space-3)",
            display: "flex",
            gap: "var(--space-2)",
            zIndex: 10,
          }}
        >
          <button
            onClick={handleResetView}
            className="glass-control"
            title="Reset camera view"
            style={{
              padding: "6px 12px",
              fontSize: "12px",
              fontFamily: "var(--font-mono)",
              background: "rgba(20, 17, 15, 0.75)",
              color: "var(--paper-100)",
            }}
          >
            ↺ Reset View
          </button>

          <button
            onClick={handleToggleRotate}
            className="glass-control"
            title="Toggle turntable auto-rotation"
            style={{
              padding: "6px 12px",
              fontSize: "12px",
              fontFamily: "var(--font-mono)",
              background: isRotating ? "rgba(232, 163, 61, 0.25)" : "rgba(20, 17, 15, 0.75)",
              borderColor: isRotating ? "var(--amber)" : "rgba(244, 237, 225, 0.15)",
              color: isRotating ? "var(--amber)" : "var(--paper-100)",
            }}
          >
            🔄 Rotate {isRotating ? "ON" : "OFF"}
          </button>

          {animation && (
            <button
              onClick={handleTogglePlay}
              className="glass-control"
              title="Play or pause animation"
              style={{
                padding: "6px 12px",
                fontSize: "12px",
                fontFamily: "var(--font-mono)",
                background: isPlayingAnim ? "rgba(232, 163, 61, 0.25)" : "rgba(20, 17, 15, 0.75)",
                borderColor: isPlayingAnim ? "var(--amber)" : "rgba(244, 237, 225, 0.15)",
                color: isPlayingAnim ? "var(--amber)" : "var(--paper-100)",
              }}
            >
              {isPlayingAnim ? "⏸ Pause Motion" : "▶ Play Motion"}
            </button>
          )}
        </div>

        {/* Bottom Bar: Exploded View Slider (§6.3) & AR Button */}
        <div
          style={{
            position: "absolute",
            bottom: "var(--space-3)",
            left: "var(--space-3)",
            right: "var(--space-3)",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            pointerEvents: "none",
            zIndex: 10,
          }}
        >
          {/* Exploded View Slider */}
          {hasExplode ? (
            <div
              className="glass-panel"
              style={{
                pointerEvents: "auto",
                padding: "6px 14px",
                display: "flex",
                alignItems: "center",
                gap: "var(--space-3)",
                background: "rgba(20, 17, 15, 0.8)",
                border: "1px solid rgba(244, 237, 225, 0.15)",
                borderRadius: "var(--radius-button)",
              }}
            >
              <span
                style={{
                  fontFamily: "var(--font-mono)",
                  fontSize: "12px",
                  color: "var(--paper-100)",
                }}
              >
                Explode: {Math.round(explodeValue * 100)}%
              </span>
              <input
                type="range"
                min="0"
                max="1"
                step="0.02"
                value={explodeValue}
                onChange={(e) => setExplodeValue(parseFloat(e.target.value))}
                style={{
                  width: "120px",
                  cursor: "pointer",
                  accentColor: "var(--amber)",
                }}
              />
            </div>
          ) : (
            <div />
          )}

          {/* AR Button */}
          {canAr && (
            <button
              onClick={handleLaunchAR}
              className="glass-control"
              style={{
                pointerEvents: "auto",
                padding: "8px 16px",
                background: "rgba(232, 163, 61, 0.9)",
                color: "var(--bench-900)",
                fontWeight: 600,
                fontSize: "13px",
                display: "flex",
                alignItems: "center",
                gap: "6px",
              }}
            >
              <span>📱 View in your space (AR)</span>
            </button>
          )}
        </div>
      </div>

      {/* Orbit & Key Navigation Caption (§6.5, §6.6) */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "0 var(--space-2)",
          flexWrap: "wrap",
          gap: "var(--space-2)",
        }}
      >
        <span
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "12px",
            color: "var(--paper-500)",
          }}
        >
          Drag to orbit. Pinch/scroll to zoom. Tab/Click to select part. Press Esc to clear.
        </span>

        {hiddenPartIds.length > 0 && (
          <button
            onClick={onShowAllParts}
            className="glass-control"
            style={{
              padding: "4px 10px",
              fontSize: "12px",
              fontFamily: "var(--font-mono)",
              color: "var(--amber)",
            }}
          >
            👁 Restore Hidden ({hiddenPartIds.length})
          </button>
        )}
      </div>
    </div>
  );
}
