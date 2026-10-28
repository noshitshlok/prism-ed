import struct
import json
from pathlib import Path

def get_model_stats(glb_or_gltf_path):
    p = Path(glb_or_gltf_path)
    if not p.exists():
        return 0, 0
    size_bytes = p.stat().st_size
    triangles = 0
    
    if p.suffix == ".glb":
        with open(p, "rb") as f:
            magic, version, length = struct.unpack("<4sII", f.read(12))
            chunk_len, chunk_type = struct.unpack("<II", f.read(8))
            meta = json.loads(f.read(chunk_len).decode("utf-8"))
            
        accessors = meta.get("accessors", [])
        meshes = meta.get("meshes", [])
        for m in meshes:
            for prim in m.get("primitives", []):
                idx = prim.get("indices")
                if idx is not None and idx < len(accessors):
                    triangles += accessors[idx].get("count", 0) // 3
                elif "attributes" in prim and "POSITION" in prim["attributes"]:
                    pos_idx = prim["attributes"]["POSITION"]
                    if pos_idx < len(accessors):
                        triangles += accessors[pos_idx].get("count", 0) // 3
    elif p.suffix == ".gltf":
        with open(p, "r", encoding="utf-8") as f:
            meta = json.load(f)
        accessors = meta.get("accessors", [])
        meshes = meta.get("meshes", [])
        for m in meshes:
            for prim in m.get("primitives", []):
                idx = prim.get("indices")
                if idx is not None and idx < len(accessors):
                    triangles += accessors[idx].get("count", 0) // 3
    return size_bytes, triangles

topics_file = Path("app/data/topics.json")
with open(topics_file, "r", encoding="utf-8") as f:
    topics = json.load(f).get("topics", [])

for t in topics:
    m_path = Path("public") / t["modelUrl"].lstrip("/\\")
    size_b, tris = get_model_stats(m_path)
    print(f"{t['id']} | status: {t.get('status')} | size: {round(size_b/1024, 1)} KB | tris: {tris}")
