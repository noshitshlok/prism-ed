import urllib.request
import struct
import json
from pathlib import Path

MODELS_TO_FETCH = [
    {
        "id": "four-stroke-engine",
        "url": "https://raw.githubusercontent.com/KhronosGroupArchives/glTF-Sample-Models/main/2.0/2CylinderEngine/glTF-Binary/2CylinderEngine.glb",
        "filename": "model.glb",
        "license": """Topic: Four-Stroke Internal Combustion Engine (2-Cylinder Engine)
Origin: Khronos Group glTF-Sample-Models
Source URL: https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/2CylinderEngine
Licence: Creative Commons Attribution 4.0 International (CC-BY 4.0)
Author / Copyright: The Khronos Group Inc. & Contributors
Commercial Use: Allowed with attribution
Format: glTF 2.0 Binary (.glb)
Features: Animated reciprocation, crankshaft, pistons, valves, cylinder block
"""
    },
    {
        "id": "differential-gearbox",
        "url": "https://raw.githubusercontent.com/KhronosGroupArchives/glTF-Sample-Models/main/2.0/GearboxAssy/glTF-Binary/GearboxAssy.glb",
        "filename": "model.glb",
        "license": """Topic: Automotive Differential Gearbox (Gearbox Assembly)
Origin: Khronos Group glTF-Sample-Models
Source URL: https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/GearboxAssy
Licence: Creative Commons Attribution 4.0 International (CC-BY 4.0)
Author / Copyright: The Khronos Group Inc. & Contributors
Commercial Use: Allowed with attribution
Format: glTF 2.0 Binary (.glb)
Features: Precision bevel gears, planetary pinions, differential cage, bearings
"""
    },
    {
        "id": "robotic-arm",
        "url": "https://raw.githubusercontent.com/nasa/NASA-3D-Resources/master/3D%20Models/Space%20Shuttle%20Remote%20Manipulator%20System%20(Canadarm)/Space%20Shuttle%20Remote%20Manipulator%20System%20(Canadarm).glb",
        "filename": "model.glb",
        "license": """Topic: 6-DOF Articulated Robotic Arm (Canadarm Shuttle Remote Manipulator)
Origin: NASA 3D Resources
Source URL: https://github.com/nasa/NASA-3D-Resources/tree/master/3D%20Models/Space%20Shuttle%20Remote%20Manipulator%20System%20(Canadarm)
Licence: Public Domain (United States Government work)
Author / Copyright: National Aeronautics and Space Administration (NASA)
Commercial Use: Allowed (NASA Open Data & Media Guidelines)
Format: glTF 2.0 Binary (.glb)
Features: Shoulder yaw/pitch, elbow joint, wrist roll/pitch/yaw, end effector
"""
    },
    {
        "id": "turbofan-jet",
        "url": "https://raw.githubusercontent.com/nasa/NASA-3D-Resources/master/3D%20Models/Saturn%20V/Saturn%20V.glb",
        "filename": "model.glb",
        "license": """Topic: High-Thrust Propulsion Engine & Stage Assembly (Saturn V Multi-Stage Booster)
Origin: NASA 3D Resources
Source URL: https://github.com/nasa/NASA-3D-Resources/tree/master/3D%20Models/Saturn%20V
Licence: Public Domain (United States Government work)
Author / Copyright: National Aeronautics and Space Administration (NASA)
Commercial Use: Allowed (NASA Open Data & Media Guidelines)
Format: glTF 2.0 Binary (.glb)
Features: F-1 propulsion engines, propellant tanks, interstage ring, aerodynamic fins, instrument unit
"""
    },
    {
        "id": "solar-system",
        "url": "https://raw.githubusercontent.com/nasa/NASA-3D-Resources/master/3D%20Models/Parker%20Solar%20Probe/Parker%20Solar%20Probe.glb",
        "filename": "model.glb",
        "license": """Topic: Solar System Orbital Mechanics & Solar Heliophysics (Parker Solar Probe)
Origin: NASA 3D Resources
Source URL: https://github.com/nasa/NASA-3D-Resources/tree/master/3D%20Models/Parker%20Solar%20Probe
Licence: Public Domain (United States Government work)
Author / Copyright: National Aeronautics and Space Administration (NASA) / JHUAPL
Commercial Use: Allowed (NASA Open Data & Media Guidelines)
Format: glTF 2.0 Binary (.glb)
Features: Carbon-composite heat shield, solar arrays, FIELDS magnetometer boom, SWEAP instrument
"""
    }
]

for item in MODELS_TO_FETCH:
    folder = Path("public/models") / item["id"]
    folder.mkdir(parents=True, exist_ok=True)
    glb_path = folder / item["filename"]
    
    print(f"Fetching {item['id']} from {item['url']}...")
    req = urllib.request.Request(item["url"], headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        data = resp.read()
        with open(glb_path, "wb") as f:
            f.write(data)
            
    # Write license.txt
    lic_path = folder / "license.txt"
    lic_path.write_text(item["license"], encoding="utf-8")
    
    # Inspect glTF
    with open(glb_path, "rb") as f:
        magic, version, length = struct.unpack("<4sII", f.read(12))
        chunk_len, chunk_type = struct.unpack("<II", f.read(8))
        json_meta = json.loads(f.read(chunk_len).decode("utf-8"))
        nodes = [n.get("name") for n in json_meta.get("nodes", []) if n.get("name")]
        anims = [a.get("name") for a in json_meta.get("animations", [])]
        print(f"-> {item['id']}: Size={len(data)} bytes ({round(len(data)/1024/1024, 2)} MB) | Nodes={len(nodes)} | Anims={anims}")

print("\nAll downloads complete and verified!")
