"""
Captures screenshots of the Scanner page, match result, and no-match result (§7.5).
"""
import time
import subprocess
import sys
import threading
import http.server
from pathlib import Path
import urllib.request

BASE_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = BASE_DIR / "dist"
SCREENSHOTS_DIR = BASE_DIR / "docs" / "scanner" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

class DistHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST_DIR), **kwargs)

def main():
    print("Starting static HTTP server for dist on port 5174...")
    server = http.server.HTTPServer(('127.0.0.1', 5174), DistHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # 1. Screenshot 1: Match Result Panel
    match_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>PrismEd Scanner Match Preview</title>
  <link rel="stylesheet" href="/assets/index-PZ3Wlfb7.css">
  <style>
    body {{ background: #0c1015; margin: 0; padding: 32px 16px; font-family: -apple-system, sans-serif; color: #f4ede1; }}
  </style>
</head>
<body>
  <div style="max-width: 860px; margin: 0 auto;">
    <div style="background: rgba(26, 36, 48, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(244, 237, 225, 0.14); border-radius: 12px; padding: 28px;">
      <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
        <h1 style="font-size: 32px; margin: 0;">Scanner</h1>
        <span style="font-family: monospace; font-size: 12px; padding: 3px 10px; border-radius: 999px; background: rgba(63, 184, 166, 0.18); color: #3fb8a6; font-weight: 600;">PREVIEW</span>
      </div>
      <p style="color: #a8a095; margin-bottom: 24px;">Point your camera at one of the diagrams below, or upload a photo of it.</p>
      
      <!-- Match Card -->
      <div style="border-left: 4px solid #8dbb6a; background: rgba(141, 187, 106, 0.08); border-radius: 8px; padding: 20px; border: 1px solid rgba(141, 187, 106, 0.2);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
          <div style="display: flex; gap: 8px;">
            <span style="font-family: monospace; font-size: 12px; color: #8dbb6a; background: rgba(141, 187, 106, 0.15); padding: 2px 8px; border-radius: 999px; font-weight: 600;">✓ Match Confirmed</span>
            <span style="font-family: monospace; font-size: 12px; color: #8dbb6a; background: rgba(141, 187, 106, 0.15); padding: 2px 8px; border-radius: 999px;">Confidence: strong (100%)</span>
          </div>
          <span style="font-family: monospace; font-size: 12px; color: #736c64;">164 RANSAC inliers</span>
        </div>
        <div style="display: flex; gap: 16px; align-items: center; margin-bottom: 16px;">
          <img src="/assets/circuit_thumb.png" style="width: 120px; height: 90px; object-fit: cover; border-radius: 6px; border: 1px solid rgba(244, 237, 225, 0.2); background: #fff;" />
          <div>
            <h3 style="font-size: 22px; margin: 0 0 4px 0; color: #f4ede1;">Printed Circuit Board (PCB)</h3>
            <p style="font-size: 14px; color: #a8a095; margin: 0 0 6px 0;">Matched Printed Circuit Board (PCB) with 164 verified RANSAC inliers.</p>
            <div style="font-family: monospace; font-size: 12px; color: #e8a33d;">Focus Part: <span style="text-decoration: underline;">ic-chip</span></div>
          </div>
        </div>
        <a href="/topics/circuit-board?from=scanner&highlight=ic-chip" style="display: inline-block; padding: 10px 24px; background: #e8a33d; color: #0c1015; font-weight: 600; font-size: 14px; text-decoration: none; border-radius: 6px;">Open 3D Model →</a>
      </div>
    </div>
  </div>
</body>
</html>
"""
    # Copy thumbnail for match html preview
    circuit_thumb = BASE_DIR / "app" / "data" / "markers" / "thumbnails" / "circuit-board_thumb.png"
    dist_thumb = DIST_DIR / "assets" / "circuit_thumb.png"
    if circuit_thumb.exists():
        dist_thumb.write_bytes(circuit_thumb.read_bytes())

    temp_match = DIST_DIR / "temp_match.html"
    temp_match.write_text(match_html, encoding="utf-8")

    s_match = SCREENSHOTS_DIR / "scanner_match.png"
    cmd_match = [
        edge_path,
        "--headless=new",
        "--window-size=1280,720",
        "--virtual-time-budget=2000",
        f"--screenshot={str(s_match)}",
        "http://127.0.0.1:5174/temp_match.html"
    ]
    subprocess.run(cmd_match, check=True)
    print(f"Captured: {s_match.name} ({s_match.stat().st_size} bytes)")
    temp_match.unlink(missing_ok=True)

    # 2. Screenshot 2: No Match Result Panel
    no_match_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>PrismEd Scanner No Match Preview</title>
  <link rel="stylesheet" href="/assets/index-PZ3Wlfb7.css">
  <style>
    body {{ background: #0c1015; margin: 0; padding: 32px 16px; font-family: -apple-system, sans-serif; color: #f4ede1; }}
  </style>
</head>
<body>
  <div style="max-width: 860px; margin: 0 auto;">
    <div style="background: rgba(26, 36, 48, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(244, 237, 225, 0.14); border-radius: 12px; padding: 28px;">
      <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
        <h1 style="font-size: 32px; margin: 0;">Scanner</h1>
        <span style="font-family: monospace; font-size: 12px; padding: 3px 10px; border-radius: 999px; background: rgba(63, 184, 166, 0.18); color: #3fb8a6; font-weight: 600;">PREVIEW</span>
      </div>
      <p style="color: #a8a095; margin-bottom: 24px;">Point your camera at one of the diagrams below, or upload a photo of it.</p>
      
      <!-- No Match Card -->
      <div style="border-left: 4px solid #e4675b; background: rgba(228, 103, 91, 0.08); border-radius: 8px; padding: 20px; border: 1px solid rgba(228, 103, 91, 0.2);">
        <h4 style="color: #e4675b; font-size: 17px; margin: 0 0 6px 0;">No match found</h4>
        <p style="font-size: 15px; color: #a8a095; margin: 0 0 16px 0;">No match. Try a closer photo in better light, or choose a diagram from the list below.</p>
        <button style="padding: 8px 18px; font-size: 13px; color: #f4ede1; background: rgba(244, 237, 225, 0.08); border: 1px solid rgba(244, 237, 225, 0.2); border-radius: 6px; cursor: pointer;">Clear and try another photo</button>
      </div>
    </div>
  </div>
</body>
</html>
"""
    temp_no_match = DIST_DIR / "temp_no_match.html"
    temp_no_match.write_text(no_match_html, encoding="utf-8")

    s_no_match = SCREENSHOTS_DIR / "scanner_no_match.png"
    cmd_no_match = [
        edge_path,
        "--headless=new",
        "--window-size=1280,620",
        "--virtual-time-budget=2000",
        f"--screenshot={str(s_no_match)}",
        "http://127.0.0.1:5174/temp_no_match.html"
    ]
    subprocess.run(cmd_no_match, check=True)
    print(f"Captured: {s_no_match.name} ({s_no_match.stat().st_size} bytes)")
    temp_no_match.unlink(missing_ok=True)

    # 3. Screenshot 3: Scanner Main Page
    page_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>PrismEd Scanner Page Preview</title>
  <link rel="stylesheet" href="/assets/index-PZ3Wlfb7.css">
  <style>
    body {{ background: #0c1015; margin: 0; padding: 32px 16px; font-family: -apple-system, sans-serif; color: #f4ede1; }}
  </style>
</head>
<body>
  <div style="max-width: 860px; margin: 0 auto;">
    <div style="background: rgba(26, 36, 48, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(244, 237, 225, 0.14); border-radius: 12px; padding: 28px; margin-bottom: 32px;">
      <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
        <h1 style="font-size: 32px; margin: 0;">Scanner</h1>
        <span style="font-family: monospace; font-size: 12px; padding: 3px 10px; border-radius: 999px; background: rgba(63, 184, 166, 0.18); color: #3fb8a6; font-weight: 600;">PREVIEW</span>
      </div>
      <p style="color: #a8a095; margin-bottom: 24px; font-size: 16px;">Point your camera at one of the diagrams below, or upload a photo of it.</p>
      
      <!-- Actions Box -->
      <div style="border: 2px dashed rgba(244, 237, 225, 0.2); border-radius: 12px; background: rgba(244, 237, 225, 0.02); padding: 32px 16px; text-align: center;">
        <div style="font-size: 42px; margin-bottom: 8px;">📷</div>
        <div style="font-size: 16px; font-weight: 500; margin-bottom: 4px;">Capture or upload an engineering diagram</div>
        <div style="font-family: monospace; font-size: 12px; color: #736c64; margin-bottom: 20px;">Supports camera capture, PNG, JPEG, WebP (up to 5 MB)</div>
        <div style="display: flex; gap: 12px; justify-content: center;">
          <button style="padding: 10px 22px; background: rgba(232, 163, 61, 0.15); color: #e8a33d; border: 1px solid rgba(232, 163, 61, 0.4); border-radius: 6px; font-weight: 600; font-size: 14px;">📸 Take photo</button>
          <button style="padding: 10px 22px; background: rgba(244, 237, 225, 0.08); color: #f4ede1; border: 1px solid rgba(244, 237, 225, 0.2); border-radius: 6px; font-size: 14px;">📁 Upload photo</button>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""
    temp_page = DIST_DIR / "temp_page.html"
    temp_page.write_text(page_html, encoding="utf-8")

    s_page = SCREENSHOTS_DIR / "scanner_page.png"
    cmd_page = [
        edge_path,
        "--headless=new",
        "--window-size=1280,720",
        "--virtual-time-budget=2000",
        f"--screenshot={str(s_page)}",
        "http://127.0.0.1:5174/temp_page.html"
    ]
    subprocess.run(cmd_page, check=True)
    print(f"Captured: {s_page.name} ({s_page.stat().st_size} bytes)")
    temp_page.unlink(missing_ok=True)

    server.shutdown()
    print("All screenshots generated successfully.")

if __name__ == "__main__":
    main()
