"""
PrismEd Marker Image Generator (Prompt v2 §3)
Renders the project's own verified 3D models at 1600px resolution on a clean plain light background.
Saves images to app/data/markers/images/<topic-id>.png and thumbnail copies.
"""
import http.server
import threading
import subprocess
import time
from pathlib import Path
import cv2

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "app" / "data" / "markers" / "images"
THUMBS_DIR = BASE_DIR / "app" / "data" / "markers" / "thumbnails"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
THUMBS_DIR.mkdir(parents=True, exist_ok=True)

MARKERS = [
    {
        "topicId": "circuit-board",
        "modelPath": "/public/models/circuit-board/scene.gltf",
        "cameraOrbit": "0deg 60deg 105%",
        "fieldOfView": "30deg"
    },
    {
        "topicId": "differential-gearbox",
        "modelPath": "/public/models/differential-gearbox/model.glb",
        "cameraOrbit": "-30deg 70deg 105%",
        "fieldOfView": "32deg"
    },
    {
        "topicId": "four-stroke-engine",
        "modelPath": "/public/models/four-stroke-engine/model.glb",
        "cameraOrbit": "auto auto auto",
        "fieldOfView": "auto"
    }
]

def main():
    server = http.server.HTTPServer(('127.0.0.1', 9993), http.server.SimpleHTTPRequestHandler)
    t = threading.Thread(target=server.serve_forever)
    t.daemon = True
    t.start()
    print("HTTP Server running on 127.0.0.1:9993")

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    for m in MARKERS:
        topic_id = m["topicId"]
        out_png = IMAGES_DIR / f"{topic_id}.png"
        thumb_png = THUMBS_DIR / f"{topic_id}_thumb.png"

        html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script type="module" src="/node_modules/@google/model-viewer/dist/model-viewer.min.js"></script>
<style>
  body {{
    margin: 0;
    padding: 0;
    background-color: #fbf9f5;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 1600px;
    height: 1200px;
    overflow: hidden;
  }}
  model-viewer {{
    width: 1560px;
    height: 1160px;
    --poster-color: transparent;
  }}
</style>
</head>
<body>
  <model-viewer
    id="viewer"
    src="{m['modelPath']}"
    camera-orbit="{m.get('cameraOrbit', '0deg 75deg 105%')}"
    field-of-view="{m.get('fieldOfView', '30deg')}"
    exposure="1.05"
    shadow-intensity="0.8"
    shadow-softness="0.5">
  </model-viewer>
</body>
</html>
"""
        temp_html = BASE_DIR / "scripts" / f"render_{topic_id}.html"
        temp_html.write_text(html_content, encoding="utf-8")

        cmd = [
            edge_path,
            "--headless=new",
            "--enable-webgl",
            "--use-gl=angle",
            "--use-angle=d3d11",
            "--window-size=1600,1200",
            "--virtual-time-budget=8000",
            f"--screenshot={str(out_png)}",
            f"http://127.0.0.1:9993/scripts/render_{topic_id}.html"
        ]
        print(f"Rendering {topic_id} at 1600x1200...")
        subprocess.run(cmd, check=True)
        temp_html.unlink(missing_ok=True)

        if out_png.exists():
            img = cv2.imread(str(out_png))
            # Generate thumbnail 400x300
            thumb = cv2.resize(img, (400, 300), interpolation=cv2.INTER_AREA)
            cv2.imwrite(str(thumb_png), thumb)
            print(f"Successfully generated {out_png.name} ({img.shape}) and {thumb_png.name}")
        else:
            print(f"Failed to render {topic_id}")

    server.shutdown()
    print("All marker images rendered.")

if __name__ == "__main__":
    main()
