import React from "react";
import HeaderBar from "../shared/HeaderBar";
import ScanUpload from "../features/scanner/ScanUpload";

export default function ScanPage() {
  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <HeaderBar backTo="/" backLabel="Specimens" title="Diagram Scanner" />
      <main style={{ maxWidth: "1360px", margin: "0 auto", padding: "var(--space-6)", width: "100%", flex: 1 }}>
        <ScanUpload />
      </main>
    </div>
  );
}
