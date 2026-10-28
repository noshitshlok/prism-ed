import json
import struct
from pathlib import Path

def inspect_bounds(glb_path):
    with open(glb_path, "rb") as f:
        magic, version, length = struct.unpack("<4sII", f.read(12))
        chunk_len, chunk_type = struct.unpack("<II", f.read(8))
        meta = json.loads(f.read(chunk_len).decode("utf-8"))
        
    accessors = meta.get("accessors", [])
    pos_bounds = []
    for acc in accessors:
        if acc.get("type") == "VEC3" and "min" in acc and "max" in acc:
            pos_bounds.append((acc["min"], acc["max"]))
            
    if not pos_bounds:
        return None
        
    global_min = [min(b[0][i] for b in pos_bounds) for i in range(3)]
    global_max = [max(b[1][i] for b in pos_bounds) for i in range(3)]
    return global_min, global_max

models = [
    ("human-heart", "public/models/human-heart/model.glb"),
    ("four-stroke-engine", "public/models/four-stroke-engine/model.glb"),
    ("differential-gearbox", "public/models/differential-gearbox/model.glb"),
    ("robotic-arm", "public/models/robotic-arm/model.glb"),
    ("turbofan-jet", "public/models/turbofan-jet/model.glb"),
    ("solar-system", "public/models/solar-system/model.glb"),
    ("space-suit", "public/models/space-suit/Astronaut.glb"),
    ("circuit-board", "public/models/circuit-board/scene.gltf"),
]

for name, path in models:
    p = Path(path)
    if not p.exists():
        print(f"{name}: File not found ({p})")
        continue
    if p.suffix == ".glb":
        bounds = inspect_bounds(p)
        if bounds:
            g_min, g_max = bounds
            center = [(g_min[i] + g_max[i])/2 for i in range(3)]
            dims = [g_max[i] - g_min[i] for i in range(3)]
            print(f"{name}:")
            print(f"  Min: {[round(x, 3) for x in g_min]}")
            print(f"  Max: {[round(x, 3) for x in g_max]}")
            print(f"  Center: {[round(x, 3) for x in center]}")
            print(f"  Dims: {[round(x, 3) for x in dims]}")
