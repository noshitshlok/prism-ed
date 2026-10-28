"""
PrismEd Procedural 3D Model Generator
Generates clean, valid, standard glTF 2.0 binary (.glb) files for all 20 diagram/hybrid topics
adhering to Section 8 of PRISMED_MODEL_ADDON_v1.1.md:
- Metres, Y-up, origin at base centre
- PBR metallic-roughness materials with warm palette tokens
- Nodes named after parts[].id
- Under 8 MB
"""
import os
import json
import struct
import math
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TOPICS_FILE = BASE_DIR / "app" / "data" / "topics.json"
MODELS_DIR = BASE_DIR / "public" / "models"

# Palette colors from Section 2.1 in linear float RGBA
COLORS = {
    "teal": [0.247, 0.722, 0.651, 1.0],      # #3FB8A6
    "amber": [0.910, 0.639, 0.239, 1.0],     # #E8A33D
    "coral": [0.894, 0.404, 0.357, 1.0],     # #E4675B
    "violet": [0.612, 0.549, 0.816, 1.0],    # #9C8CD0
    "sky": [0.435, 0.659, 0.863, 1.0],       # #6FA8DC
    "moss": [0.553, 0.733, 0.416, 1.0],      # #8DBB6A
    "paper": [0.957, 0.929, 0.882, 1.0],     # #F4EDE1
    "steel": [0.450, 0.450, 0.480, 1.0],     # Neutral metal
    "dark": [0.150, 0.130, 0.120, 1.0],      # Bench dark
}

def create_box(width=0.08, height=0.08, depth=0.08, center=(0, 0, 0)):
    hw, hh, hd = width / 2.0, height / 2.0, depth / 2.0
    cx, cy, cz = center

    # 6 faces * 4 vertices = 24 vertices
    positions = [
        # Front (+Z)
        cx - hw, cy - hh, cz + hd,  cx + hw, cy - hh, cz + hd,  cx + hw, cy + hh, cz + hd,  cx - hw, cy + hh, cz + hd,
        # Back (-Z)
        cx + hw, cy - hh, cz - hd,  cx - hw, cy - hh, cz - hd,  cx - hw, cy + hh, cz - hd,  cx + hw, cy + hh, cz - hd,
        # Top (+Y)
        cx - hw, cy + hh, cz + hd,  cx + hw, cy + hh, cz + hd,  cx + hw, cy + hh, cz - hd,  cx - hw, cy + hh, cz - hd,
        # Bottom (-Y)
        cx - hw, cy - hh, cz - hd,  cx + hw, cy - hh, cz - hd,  cx + hw, cy - hh, cz + hd,  cx - hw, cy - hh, cz + hd,
        # Right (+X)
        cx + hw, cy - hh, cz + hd,  cx + hw, cy - hh, cz - hd,  cx + hw, cy + hh, cz - hd,  cx + hw, cy + hh, cz + hd,
        # Left (-X)
        cx - hw, cy - hh, cz - hd,  cx - hw, cy - hh, cz + hd,  cx - hw, cy + hh, cz + hd,  cx - hw, cy + hh, cz - hd,
    ]

    normals = [
        # Front
        0, 0, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1,
        # Back
        0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1,
        # Top
        0, 1, 0,  0, 1, 0,  0, 1, 0,  0, 1, 0,
        # Bottom
        0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0,
        # Right
        1, 0, 0,  1, 0, 0,  1, 0, 0,  1, 0, 0,
        # Left
        -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0,
    ]

    indices = []
    for f in range(6):
        base = f * 4
        indices.extend([base, base + 1, base + 2, base, base + 2, base + 3])

    return positions, normals, indices

def create_sphere(radius=0.04, segments=12, rings=8, center=(0, 0, 0)):
    cx, cy, cz = center
    positions = []
    normals = []
    indices = []

    for r in range(rings + 1):
        v = r / rings
        phi = v * math.pi
        for s in range(segments + 1):
            u = s / segments
            theta = u * 2.0 * math.pi

            nx = math.sin(phi) * math.cos(theta)
            ny = math.cos(phi)
            nz = math.sin(phi) * math.sin(theta)

            px = cx + radius * nx
            py = cy + radius * ny
            pz = cz + radius * nz

            positions.extend([px, py, pz])
            normals.extend([nx, ny, nz])

    for r in range(rings):
        for s in range(segments):
            first = r * (segments + 1) + s
            second = first + segments + 1
            indices.extend([first, second, first + 1])
            indices.extend([second, second + 1, first + 1])

    return positions, normals, indices

def create_cylinder(radius=0.03, height=0.08, segments=12, center=(0, 0, 0)):
    cx, cy, cz = center
    positions = []
    normals = []
    indices = []
    hh = height / 2.0

    # Side vertices
    for s in range(segments + 1):
        u = s / segments
        theta = u * 2.0 * math.pi
        nx = math.cos(theta)
        nz = math.sin(theta)

        # Top vertex
        positions.extend([cx + radius * nx, cy + hh, cz + radius * nz])
        normals.extend([nx, 0.0, nz])
        # Bottom vertex
        positions.extend([cx + radius * nx, cy - hh, cz + radius * nz])
        normals.extend([nx, 0.0, nz])

    for s in range(segments):
        base = s * 2
        indices.extend([base, base + 1, base + 2])
        indices.extend([base + 1, base + 3, base + 2])

    return positions, normals, indices

def build_glb(nodes_info):
    """
    nodes_info: list of dicts:
    {
      "name": node_name,
      "positions": [...],
      "normals": [...],
      "indices": [...],
      "color": [r, g, b, a],
      "metallic": 0.2,
      "roughness": 0.6
    }
    """
    binary_data = bytearray()
    json_nodes = []
    json_meshes = []
    json_materials = []
    json_accessors = []
    json_buffer_views = []

    for mesh_idx, info in enumerate(nodes_info):
        pos_bytes = struct.pack(f"<{len(info['positions'])}f", *info['positions'])
        norm_bytes = struct.pack(f"<{len(info['normals'])}f", *info['normals'])
        ind_bytes = struct.pack(f"<{len(info['indices'])}H", *info['indices'])

        # Align buffer offsets to 4 bytes
        def align():
            while len(binary_data) % 4 != 0:
                binary_data.append(0)

        # 1. Position BufferView & Accessor
        align()
        pos_offset = len(binary_data)
        binary_data.extend(pos_bytes)
        pos_view_idx = len(json_buffer_views)
        json_buffer_views.append({
            "buffer": 0,
            "byteOffset": pos_offset,
            "byteLength": len(pos_bytes),
            "target": 34962 # ARRAY_BUFFER
        })

        # Min/max bounds for positions
        xs = info['positions'][0::3]
        ys = info['positions'][1::3]
        zs = info['positions'][2::3]
        pos_acc_idx = len(json_accessors)
        json_accessors.append({
            "bufferView": pos_view_idx,
            "byteOffset": 0,
            "componentType": 5126, # FLOAT
            "count": len(info['positions']) // 3,
            "type": "VEC3",
            "max": [max(xs), max(ys), max(zs)],
            "min": [min(xs), min(ys), min(zs)]
        })

        # 2. Normal BufferView & Accessor
        align()
        norm_offset = len(binary_data)
        binary_data.extend(norm_bytes)
        norm_view_idx = len(json_buffer_views)
        json_buffer_views.append({
            "buffer": 0,
            "byteOffset": norm_offset,
            "byteLength": len(norm_bytes),
            "target": 34962
        })
        norm_acc_idx = len(json_accessors)
        json_accessors.append({
            "bufferView": norm_view_idx,
            "byteOffset": 0,
            "componentType": 5126,
            "count": len(info['normals']) // 3,
            "type": "VEC3"
        })

        # 3. Index BufferView & Accessor
        align()
        ind_offset = len(binary_data)
        binary_data.extend(ind_bytes)
        ind_view_idx = len(json_buffer_views)
        json_buffer_views.append({
            "buffer": 0,
            "byteOffset": ind_offset,
            "byteLength": len(ind_bytes),
            "target": 34963 # ELEMENT_ARRAY_BUFFER
        })
        ind_acc_idx = len(json_accessors)
        json_accessors.append({
            "bufferView": ind_view_idx,
            "byteOffset": 0,
            "componentType": 5123, # UNSIGNED_SHORT
            "count": len(info['indices']),
            "type": "SCALAR"
        })

        # 4. Material
        mat_idx = len(json_materials)
        json_materials.append({
            "name": f"mat_{info['name']}",
            "pbrMetallicRoughness": {
                "baseColorFactor": info.get("color", COLORS["amber"]),
                "metallicFactor": info.get("metallic", 0.2),
                "roughnessFactor": info.get("roughness", 0.6)
            }
        })

        # 5. Mesh
        json_meshes.append({
            "name": f"mesh_{info['name']}",
            "primitives": [{
                "attributes": {
                    "POSITION": pos_acc_idx,
                    "NORMAL": norm_acc_idx
                },
                "indices": ind_acc_idx,
                "material": mat_idx
            }]
        })

        # 6. Node
        json_nodes.append({
            "name": info['name'],
            "mesh": mesh_idx
        })

    # Pad binary data to 4-byte boundary
    while len(binary_data) % 4 != 0:
        binary_data.append(0)

    gltf_json = {
        "asset": {
            "version": "2.0",
            "generator": "PrismEd 3D Model Procedural Engine"
        },
        "scene": 0,
        "scenes": [{
            "nodes": list(range(len(json_nodes)))
        }],
        "nodes": json_nodes,
        "meshes": json_meshes,
        "materials": json_materials,
        "accessors": json_accessors,
        "bufferViews": json_buffer_views,
        "buffers": [{
            "byteLength": len(binary_data)
        }]
    }

    json_str = json.dumps(gltf_json)
    json_bytes = json_str.encode("utf-8")
    # Pad JSON to 4-byte boundary with spaces
    while len(json_bytes) % 4 != 0:
        json_bytes += b' '

    # GLB Header: magic (4B), version (4B), length (4B)
    total_length = 12 + 8 + len(json_bytes) + 8 + len(binary_data)
    header = struct.pack("<4sII", b"glTF", 2, total_length)

    # Chunk 0: JSON
    chunk0_header = struct.pack("<II", len(json_bytes), 0x4E4F534A)
    # Chunk 1: BIN
    chunk1_header = struct.pack("<II", len(binary_data), 0x004E4942)

    return header + chunk0_header + json_bytes + chunk1_header + binary_data

def parse_hotspot(coords_str):
    import re
    nums = [float(x) for x in re.findall(r"[-+]?(?:\d*\.\d+|\d+)", coords_str)]
    return (nums[0], nums[1], nums[2])

def generate_all_models():
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    color_keys = ["teal", "amber", "coral", "violet", "sky", "moss"]

    for topic in data.get("topics", []):
        topic_id = topic["id"]
        # Skip circuit-board as it already has local scene.gltf
        if topic_id == "circuit-board":
            continue
        # Skip space-suit if Astronaut.glb exists
        if topic_id == "space-suit":
            target_file = MODELS_DIR / topic_id / "Astronaut.glb"
            if target_file.exists():
                print(f"Skipping {topic_id}: already self-hosted at {target_file}")
                continue

        model_url = topic["modelUrl"]
        # Determine target file name on disk
        filename = Path(model_url).name
        target_dir = MODELS_DIR / topic_id
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / filename

        nodes_info = []

        # Add central base platform structure for origin ground reference
        base_pos, base_norm, base_ind = create_box(width=0.18, height=0.015, depth=0.18, center=(0, -0.05, 0))
        nodes_info.append({
            "name": "base-mount",
            "positions": base_pos,
            "normals": base_norm,
            "indices": base_ind,
            "color": COLORS["dark"],
            "metallic": 0.8,
            "roughness": 0.3
        })

        # Build geometry for each part positioned at its hotspotPosition
        for idx, part in enumerate(topic["parts"]):
            px, py, pz = parse_hotspot(part["hotspotPosition"])
            color_choice = COLORS[color_keys[idx % len(color_keys)]]

            # Alternate geometric primitives per part
            shape_type = idx % 3
            if shape_type == 0:
                pos, norm, ind = create_sphere(radius=0.025, center=(px, py, pz))
            elif shape_type == 1:
                pos, norm, ind = create_cylinder(radius=0.02, height=0.05, center=(px, py, pz))
            else:
                pos, norm, ind = create_box(width=0.04, height=0.04, depth=0.04, center=(px, py, pz))

            nodes_info.append({
                "name": part["id"],
                "positions": pos,
                "normals": norm,
                "indices": ind,
                "color": color_choice,
                "metallic": 0.4,
                "roughness": 0.5
            })

        glb_bytes = build_glb(nodes_info)
        with open(target_path, "wb") as f_out:
            f_out.write(glb_bytes)

        size_kb = len(glb_bytes) / 1024
        print(f"[{topic_id}] Generated {target_path} ({size_kb:.1f} KB, {len(nodes_info)} nodes)")

if __name__ == "__main__":
    generate_all_models()
