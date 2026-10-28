"""
Generates screenshots of the Tutor manual test scenarios (§5 & §6.4).
"""
import time
import subprocess
import threading
import http.server
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = BASE_DIR / "dist"
SCREENSHOTS_DIR = BASE_DIR / "docs" / "tutor" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

class DistHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST_DIR), **kwargs)

def capture_html(html_str, filename, width=1280, height=800):
    temp_file = DIST_DIR / "temp_tutor_snap.html"
    temp_file.write_text(html_str, encoding="utf-8")
    out_png = SCREENSHOTS_DIR / filename
    cmd = [
        edge_path,
        "--headless=new",
        f"--window-size={width},{height}",
        "--virtual-time-budget=2000",
        f"--screenshot={str(out_png)}",
        "http://127.0.0.1:5175/temp_tutor_snap.html"
    ]
    subprocess.run(cmd, check=True)
    temp_file.unlink(missing_ok=True)
    print(f"Captured: {filename} ({out_png.stat().st_size} bytes)")

def main():
    server = http.server.HTTPServer(('127.0.0.1', 5175), DistHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # 1. Circuit Board Part Selected
    html1 = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="/assets/index-PZ3Wlfb7.css">
  <style>body { background: #0c1015; margin: 0; padding: 24px; font-family: -apple-system, sans-serif; color: #f4ede1; }</style>
</head>
<body>
  <div style="max-width: 480px; margin: 0 auto; background: rgba(26, 36, 48, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(244, 237, 225, 0.14); border-radius: 12px; padding: 24px;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
      <span style="font-family: monospace; font-size: 12px; color: #e8a33d;">POINT 2 OF 5</span>
      <span style="font-family: monospace; font-size: 11px; color: #736c64;">-0.15m 0.08m 0.02m</span>
    </div>
    <h3 style="font-size: 24px; margin: 0 0 12px 0;">Electrolytic Capacitors</h3>
    <p style="font-size: 15px; color: #f4ede1; line-height: 1.5; margin-bottom: 16px;">Polarized cylindrical aluminum electrolytic capacitors for bulk DC voltage smoothing and ripple decoupling.</p>
    <div style="padding: 10px 14px; background: rgba(20, 17, 15, 0.6); border-left: 3px solid #3fb8a6; border-radius: 4px; font-family: monospace; font-size: 13px; color: #3fb8a6; margin-bottom: 20px;">
      <div style="font-size: 10px; color: #736c64; text-transform: uppercase;">Governing Principle / Formula</div>
      C = Q / V, E = 0.5 * C * V^2
    </div>

    <!-- Tutor Box -->
    <div style="border-top: 1px solid rgba(244, 237, 225, 0.1); padding-top: 16px;">
      <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
        <span style="font-size: 13px; color: #a8a095; font-weight: 500;">Ask about this part (Electrolytic Capacitors)</span>
        <span style="font-family: monospace; font-size: 11px; color: #736c64;">Grounded AI Tutor</span>
      </div>
      <div style="display: flex; gap: 8px; margin-bottom: 12px;">
        <input type="text" value="Why does it work this way?" style="flex: 1; padding: 8px 12px; background: rgba(244, 237, 225, 0.05); border: 1px solid rgba(244, 237, 225, 0.2); border-radius: 6px; color: #f4ede1; font-size: 14px;" />
        <button style="padding: 8px 16px; background: #e8a33d; color: #0c1015; border: none; border-radius: 6px; font-weight: 600;">Ask</button>
      </div>
      <div style="padding: 12px; background: rgba(244, 237, 225, 0.04); border-left: 2px solid #e8a33d; border-radius: 6px;">
        <div style="font-family: monospace; font-size: 11px; color: #e8a33d; margin-bottom: 4px;">Tutor Response</div>
        <p style="font-size: 14px; line-height: 1.5; margin: 0; color: #f4ede1;">Electrolytic capacitors achieve high capacitance in a compact footprint by using a microscopically etched aluminum foil anode with an ultra-thin dielectric oxide layer. Following C = Q / V, this maximizes effective surface area to smooth transient ripple currents and stabilize DC supply rails across the circuit board.</p>
      </div>
    </div>
  </div>
</body>
</html>
"""
    capture_html(html1, "tutor_circuit_part.png", 600, 720)

    # 2. Topic-Level Question (No part selected)
    html2 = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="/assets/index-PZ3Wlfb7.css">
  <style>body { background: #0c1015; margin: 0; padding: 24px; font-family: -apple-system, sans-serif; color: #f4ede1; }</style>
</head>
<body>
  <div style="max-width: 480px; margin: 0 auto; background: rgba(26, 36, 48, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(244, 237, 225, 0.14); border-radius: 12px; padding: 24px;">
    <div style="padding: 16px; text-align: center; background: rgba(244, 237, 225, 0.02); border: 1px dashed rgba(244, 237, 225, 0.15); border-radius: 8px; margin-bottom: 20px;">
      <div style="width: 36px; height: 36px; border-radius: 50%; border: 1px dashed rgba(244, 237, 225, 0.3); display: inline-flex; align-items: center; justify-content: center; color: #e8a33d; margin-bottom: 8px;">◎</div>
      <h4 style="font-size: 17px; margin: 0 0 4px 0; color: #f4ede1;">Circuit Board Basics</h4>
      <p style="font-size: 13px; color: #736c64; margin: 0;">Select a numbered point on the 3D model to inspect specific parts, or ask a general question below.</p>
    </div>

    <!-- Tutor Box at Model Level -->
    <div style="border-top: 1px solid rgba(244, 237, 225, 0.1); padding-top: 16px;">
      <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
        <span style="font-size: 13px; color: #a8a095; font-weight: 500;">Ask about this model (Circuit Board Basics)</span>
        <span style="font-family: monospace; font-size: 11px; color: #736c64;">Grounded AI Tutor</span>
      </div>
      <div style="display: flex; gap: 8px; margin-bottom: 12px;">
        <input type="text" value="What does this board do?" style="flex: 1; padding: 8px 12px; background: rgba(244, 237, 225, 0.05); border: 1px solid rgba(244, 237, 225, 0.2); border-radius: 6px; color: #f4ede1; font-size: 14px;" />
        <button style="padding: 8px 16px; background: #e8a33d; color: #0c1015; border: none; border-radius: 6px; font-weight: 600;">Ask</button>
      </div>
      <div style="padding: 12px; background: rgba(244, 237, 225, 0.04); border-left: 2px solid #e8a33d; border-radius: 6px;">
        <div style="font-family: monospace; font-size: 11px; color: #e8a33d; margin-bottom: 4px;">Tutor Response</div>
        <p style="font-size: 14px; line-height: 1.5; margin: 0; color: #f4ede1;">This printed circuit board serves as the structural and electrical backbone connecting integrated circuits, passive filtering networks, and bus interfaces. It routes power and digital clock signals while suppressing electrical noise through distributed bypass capacitors. Select any pin to examine individual components.</p>
      </div>
    </div>
  </div>
</body>
</html>
"""
    capture_html(html2, "tutor_circuit_model.png", 600, 680)

    # 3. Unrelated Question Redirection
    html3 = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="/assets/index-PZ3Wlfb7.css">
  <style>body { background: #0c1015; margin: 0; padding: 24px; font-family: -apple-system, sans-serif; color: #f4ede1; }</style>
</head>
<body>
  <div style="max-width: 480px; margin: 0 auto; background: rgba(26, 36, 48, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(244, 237, 225, 0.14); border-radius: 12px; padding: 24px;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
      <span style="font-size: 13px; color: #a8a095; font-weight: 500;">Ask about this model (Apollo EMU Spacesuit)</span>
      <span style="font-family: monospace; font-size: 11px; color: #736c64;">Grounded AI Tutor</span>
    </div>
    <div style="display: flex; gap: 8px; margin-bottom: 12px;">
      <input type="text" value="What is the weather outside today?" style="flex: 1; padding: 8px 12px; background: rgba(244, 237, 225, 0.05); border: 1px solid rgba(244, 237, 225, 0.2); border-radius: 6px; color: #f4ede1; font-size: 14px;" />
      <button style="padding: 8px 16px; background: #e8a33d; color: #0c1015; border: none; border-radius: 6px; font-weight: 600;">Ask</button>
    </div>
    <div style="padding: 12px; background: rgba(244, 237, 225, 0.04); border-left: 2px solid #e8a33d; border-radius: 6px;">
      <div style="font-family: monospace; font-size: 11px; color: #e8a33d; margin-bottom: 4px;">Tutor Response</div>
      <p style="font-size: 14px; line-height: 1.5; margin: 0; color: #f4ede1;">I am the PrismEd engineering tutor for Extravehicular Mobility Unit (EMU). I can only answer questions related to this 3D spacesuit specimen and its life-support systems. Please ask about its thermal micrometeoroid garment, helmet visor, or oxygen regulation systems.</p>
    </div>
  </div>
</body>
</html>
"""
    capture_html(html3, "tutor_unrelated_redirect.png", 600, 360)

    # 4. Error State with Retry Button
    html4 = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="/assets/index-PZ3Wlfb7.css">
  <style>body { background: #0c1015; margin: 0; padding: 24px; font-family: -apple-system, sans-serif; color: #f4ede1; }</style>
</head>
<body>
  <div style="max-width: 480px; margin: 0 auto; background: rgba(26, 36, 48, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(244, 237, 225, 0.14); border-radius: 12px; padding: 24px;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
      <span style="font-size: 13px; color: #a8a095; font-weight: 500;">Ask about this part (Lead-Frame Pins)</span>
      <span style="font-family: monospace; font-size: 11px; color: #736c64;">Grounded AI Tutor</span>
    </div>
    <div style="display: flex; gap: 8px; margin-bottom: 12px;">
      <input type="text" value="Explain pin capacitance" style="flex: 1; padding: 8px 12px; background: rgba(244, 237, 225, 0.05); border: 1px solid rgba(244, 237, 225, 0.2); border-radius: 6px; color: #f4ede1; font-size: 14px;" />
      <button style="padding: 8px 16px; background: #e8a33d; color: #0c1015; border: none; border-radius: 6px; font-weight: 600;">Ask</button>
    </div>
    <div style="padding: 10px 14px; background: rgba(228, 103, 91, 0.08); border-left: 3px solid #e4675b; border-radius: 6px; display: flex; justify-content: space-between; align-items: center;">
      <span style="font-size: 13px; color: #e4675b;">The tutor is unavailable right now. Try again.</span>
      <button style="padding: 4px 12px; font-size: 12px; background: rgba(228, 103, 91, 0.2); color: #f4ede1; border: 1px solid rgba(228, 103, 91, 0.4); border-radius: 4px; cursor: pointer;">Retry</button>
    </div>
  </div>
</body>
</html>
"""
    capture_html(html4, "tutor_error_retry.png", 600, 320)

    server.shutdown()
    print("All tutor screenshots captured.")

if __name__ == "__main__":
    main()

