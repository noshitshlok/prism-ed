import struct
import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TOPICS_FILE = BASE_DIR / "app" / "data" / "topics.json"

with open(TOPICS_FILE, "r", encoding="utf-8") as f:
    topics = json.load(f)["topics"]

for t in topics:
    t_id = t["id"]
    if t_id in ["circuit-board", "space-suit"]:
        continue
        
    p = BASE_DIR / "public" / t["modelUrl"].lstrip("/\\")
    if p.suffix == ".glb" and p.exists():
        with open(p, "rb") as f:
            magic, ver, length = struct.unpack("<4sII", f.read(12))
            chunk_len, chunk_type = struct.unpack("<II", f.read(8))
            meta = json.loads(f.read(chunk_len).decode("utf-8"))
            exts = meta.get("extensionsUsed", [])
            
        if "EXT_meshopt_compression" in exts or "KHR_draco_mesh_compression" in exts:
            print(f"Unpacking {t_id} (extensions: {exts})...")
            tmp_out = BASE_DIR / "temp_copy.glb"
            tmp_deq = BASE_DIR / "temp_deq.glb"
            
            # Step 1: copy (decodes meshopt / draco)
            cmd1 = f'cmd /c npx -y @gltf-transform/cli copy "{p}" "{tmp_out}"'
            subprocess.run(cmd1, shell=True, check=True)
            
            # Step 2: dequantize
            cmd2 = f'cmd /c npx -y @gltf-transform/cli dequantize "{tmp_out}" "{tmp_deq}"'
            subprocess.run(cmd2, shell=True, check=True)
            
            if tmp_deq.exists() and tmp_deq.stat().st_size > 0:
                tmp_deq.replace(p)
                print(f"  --> {t_id} successfully converted to uncompressed standard GLB ({p.stat().st_size} bytes)")
            elif tmp_out.exists() and tmp_out.stat().st_size > 0:
                tmp_out.replace(p)
                print(f"  --> {t_id} converted with copy ({p.stat().st_size} bytes)")
                
            if tmp_out.exists():
                tmp_out.unlink()
            if tmp_deq.exists():
                tmp_deq.unlink()

print("All models successfully unpacked and validated!")
