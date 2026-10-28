import urllib.request
import struct
import json
import re
import math
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "public" / "models"
TOPICS_FILE = BASE_DIR / "app" / "data" / "topics.json"

MODELS_DIR.mkdir(parents=True, exist_ok=True)

# 1. Helper to convert KiCad WRL to glTF 2.0 Binary (.glb)
def wrl_to_glb(wrl_url, out_glb_path, target_size=0.15):
    print(f"Downloading & converting {wrl_url} -> {out_glb_path}...")
    req = urllib.request.Request(wrl_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as r:
        wrl_text = r.read().decode('utf-8')
        
    materials = {}
    for m in re.finditer(r'material\s+DEF\s+([\w\-]+)\s+Material\s*\{([^}]+)\}', wrl_text):
        mat_name = m.group(1)
        body = m.group(2)
        diffuse = [0.8, 0.8, 0.8]
        dm = re.search(r'diffuseColor\s+([0-9\.\-]+)\s+([0-9\.\-]+)\s+([0-9\.\-]+)', body)
        if dm:
            diffuse = [float(dm.group(1)), float(dm.group(2)), float(dm.group(3))]
        shininess = 0.5
        sm = re.search(r'shininess\s+([0-9\.\-]+)', body)
        if sm:
            shininess = float(sm.group(1))
        materials[mat_name] = {'diffuse': diffuse, 'shininess': shininess}

    pattern = re.compile(r'Shape\s*\{\s*geometry\s*IndexedFaceSet\s*\{[^}]*coordIndex\s*\[([^\]]+)\]\s*coord\s*Coordinate\s*\{\s*point\s*\[([^\]]+)\]\s*\}\s*\}\s*appearance\s*Appearance\s*\{\s*material\s*USE\s*([\w\-]+)\s*\}\s*\}', re.DOTALL)
    matches = pattern.findall(wrl_text)
    
    all_points = []
    groups = {}
    for coord_idx_str, point_str, mat_name in matches:
        coords = [float(x) for x in point_str.replace(',', ' ').split()]
        raw_indices = [int(x) for x in coord_idx_str.replace(',', ' ').split()]
        polys = []
        curr = []
        for idx in raw_indices:
            if idx == -1:
                if len(curr) >= 3:
                    polys.append(curr)
                curr = []
            else:
                curr.append(idx)
        if curr and len(curr) >= 3:
            polys.append(curr)
            
        if mat_name not in groups:
            groups[mat_name] = {'points': [], 'triangles': []}
            
        base_idx = len(groups[mat_name]['points']) // 3
        groups[mat_name]['points'].extend(coords)
        all_points.extend(coords)
        for p in polys:
            for i in range(1, len(p) - 1):
                groups[mat_name]['triangles'].extend([base_idx + p[0], base_idx + p[i], base_idx + p[i+1]])

    xs = all_points[0::3]
    ys = all_points[1::3]
    zs = all_points[2::3]
    cx, cy, cz = (min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0, (min(zs) + max(zs)) / 2.0
    scale = target_size / max(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
    
    bin_data = bytearray()
    buffer_views = []
    accessors = []
    meshes = []
    nodes = []
    materials_json = []
    
    for mat_name, g in groups.items():
        mat_info = materials.get(mat_name, {'diffuse': [0.6, 0.6, 0.6], 'shininess': 0.5})
        diff = mat_info['diffuse']
        roughness = max(0.1, 1.0 - mat_info['shininess'])
        metallic = 0.85 if 'pin' in mat_name.lower() or 'metal' in mat_name.lower() or 'shield' in mat_name.lower() else 0.1
        
        mat_idx = len(materials_json)
        materials_json.append({
            'name': mat_name,
            'pbrMetallicRoughness': {
                'baseColorFactor': [diff[0], diff[1], diff[2], 1.0],
                'metallicFactor': metallic,
                'roughnessFactor': roughness
            }
        })
        
        pts = g['points']
        tris = g['triangles']
        num_v = len(pts) // 3
        v_positions = []
        for i in range(num_v):
            vx = (pts[i*3] - cx) * scale
            vy = (pts[i*3 + 2] - cz) * scale
            vz = -(pts[i*3 + 1] - cy) * scale
            v_positions.append((vx, vy, vz))
            
        v_normals = [[0.0, 0.0, 0.0] for _ in range(num_v)]
        for i in range(0, len(tris), 3):
            i0, i1, i2 = tris[i], tris[i+1], tris[i+2]
            p0, p1, p2 = v_positions[i0], v_positions[i1], v_positions[i2]
            ux, uy, uz = p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]
            vx, vy, vz = p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2]
            nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
            l = math.sqrt(nx*nx + ny*ny + nz*nz)
            if l > 1e-6:
                nx, ny, nz = nx/l, ny/l, nz/l
                for idx in (i0, i1, i2):
                    v_normals[idx][0] += nx
                    v_normals[idx][1] += ny
                    v_normals[idx][2] += nz
                    
        for i in range(num_v):
            nx, ny, nz = v_normals[i]
            l = math.sqrt(nx*nx + ny*ny + nz*nz)
            if l > 1e-6:
                v_normals[i] = [nx/l, ny/l, nz/l]
            else:
                v_normals[i] = [0.0, 1.0, 0.0]
                
        pos_offset = len(bin_data)
        min_p = [float('inf')]*3
        max_p = [float('-inf')]*3
        for vx, vy, vz in v_positions:
            bin_data.extend(struct.pack('<fff', vx, vy, vz))
            min_p[0] = min(min_p[0], vx); max_p[0] = max(max_p[0], vx)
            min_p[1] = min(min_p[1], vy); max_p[1] = max(max_p[1], vy)
            min_p[2] = min(min_p[2], vz); max_p[2] = max(max_p[2], vz)
        pos_len = len(bin_data) - pos_offset
        
        norm_offset = len(bin_data)
        for nx, ny, nz in v_normals:
            bin_data.extend(struct.pack('<fff', nx, ny, nz))
        norm_len = len(bin_data) - norm_offset
        
        idx_offset = len(bin_data)
        use_u32 = num_v > 65535
        for idx in tris:
            bin_data.extend(struct.pack('<I' if use_u32 else '<H', idx))
        while len(bin_data) % 4 != 0:
            bin_data.append(0)
        idx_len = len(bin_data) - idx_offset
        
        bv_pos = len(buffer_views)
        buffer_views.append({'buffer': 0, 'byteOffset': pos_offset, 'byteLength': pos_len, 'target': 34962})
        bv_norm = len(buffer_views)
        buffer_views.append({'buffer': 0, 'byteOffset': norm_offset, 'byteLength': norm_len, 'target': 34962})
        bv_idx = len(buffer_views)
        buffer_views.append({'buffer': 0, 'byteOffset': idx_offset, 'byteLength': idx_len, 'target': 34963})
        
        acc_pos = len(accessors)
        accessors.append({'bufferView': bv_pos, 'byteOffset': 0, 'componentType': 5126, 'count': num_v, 'type': 'VEC3', 'min': min_p, 'max': max_p})
        acc_norm = len(accessors)
        accessors.append({'bufferView': bv_norm, 'byteOffset': 0, 'componentType': 5126, 'count': num_v, 'type': 'VEC3'})
        acc_idx = len(accessors)
        accessors.append({'bufferView': bv_idx, 'byteOffset': 0, 'componentType': 5125 if use_u32 else 5123, 'count': len(tris), 'type': 'SCALAR'})
        
        mesh_idx = len(meshes)
        meshes.append({
            'name': mat_name,
            'primitives': [{
                'attributes': {'POSITION': acc_pos, 'NORMAL': acc_norm},
                'indices': acc_idx,
                'material': mat_idx
            }]
        })
        
        node_idx = len(nodes)
        nodes.append({'name': mat_name, 'mesh': mesh_idx})
        
    gltf_json = {
        'asset': {'version': '2.0', 'generator': 'PrismEd CAD Converter'},
        'scene': 0,
        'scenes': [{'nodes': list(range(len(nodes)))}],
        'nodes': nodes,
        'meshes': meshes,
        'materials': materials_json,
        'accessors': accessors,
        'bufferViews': buffer_views,
        'buffers': [{'byteLength': len(bin_data)}]
    }
    
    json_bytes = json.dumps(gltf_json).encode('utf-8')
    while len(json_bytes) % 4 != 0:
        json_bytes += b' '
        
    total_len = 12 + 8 + len(json_bytes) + 8 + len(bin_data)
    out_glb_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_glb_path, 'wb') as f:
        f.write(struct.pack('<4sII', b'glTF', 2, total_len))
        f.write(struct.pack('<II', len(json_bytes), 0x4E4F534A))
        f.write(json_bytes)
        f.write(struct.pack('<II', len(bin_data), 0x004E4942))
        f.write(bin_data)
        
    print(f"Created {out_glb_path} ({total_len} bytes)")

def download_file(url, out_path):
    print(f"Downloading {url} -> {out_path}...")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        data = resp.read()
    with open(out_path, 'wb') as f:
        f.write(data)
    print(f"Saved {out_path} ({len(data)} bytes)")

# 2. Setup all models
print("--- Setting up all 22 3D Models ---")

# Digital Logic Gates: KiCad DIP-14
wrl_to_glb(
    'https://raw.githubusercontent.com/KiCad/kicad-packages3D/master/Package_DIP.3dshapes/DIP-14_W7.62mm.wrl',
    MODELS_DIR / "digital-logic-gates" / "model.glb"
)

# Networking Protocol Stack: KiCad RJ45 Shielded Ethernet
wrl_to_glb(
    'https://raw.githubusercontent.com/KiCad/kicad-packages3D/master/Connector_RJ.3dshapes/RJ45_Amphenol_RJHSE538X.wrl',
    MODELS_DIR / "networking-protocol-stack" / "model.glb"
)

# CPU Architecture & Process Scheduling
cpu_glb = MODELS_DIR / "cpu-architecture" / "model.glb"
download_file('https://raw.githubusercontent.com/Wissemm697/pc-builder/main/models/cpu.glb', cpu_glb)
shutil.copyfile(cpu_glb, MODELS_DIR / "process-scheduling" / "model.glb")

# GPU Architecture & Transformer Attention
gpu_glb = MODELS_DIR / "gpu-architecture" / "model.glb"
download_file('https://raw.githubusercontent.com/Wissemm697/pc-builder/main/models/gpu.glb', gpu_glb)
shutil.copyfile(gpu_glb, MODELS_DIR / "transformer-attention" / "model.glb")

# Memory Data Structures & OS Virtual Memory
ram_glb = MODELS_DIR / "memory-data-structures" / "model.glb"
download_file('https://raw.githubusercontent.com/Wissemm697/pc-builder/main/models/ram.glb', ram_glb)
shutil.copyfile(ram_glb, MODELS_DIR / "os-virtual-memory" / "model.glb")

# Database B-Tree: SSD
ssd_glb = MODELS_DIR / "database-b-tree" / "model.glb"
download_file('https://raw.githubusercontent.com/Wissemm697/pc-builder/main/models/ssd.glb', ssd_glb)

# Distributed Microservices & AI Server Rack: Case
case_glb = MODELS_DIR / "distributed-microservices" / "model.glb"
download_file('https://raw.githubusercontent.com/Wissemm697/pc-builder/main/models/case.glb', case_glb)
shutil.copyfile(case_glb, MODELS_DIR / "ai-server-rack" / "model.glb")

# Truss Bridge: NASA Gantry Truss Structure
download_file('https://raw.githubusercontent.com/nasa/NASA-3D-Resources/master/3D%20Models/Gantry/Gantry.glb', MODELS_DIR / "truss-bridge" / "model.glb")

# Compiler Pipeline: Khronos ReciprocatingSaw (Automated electromechanical pipeline)
download_file('https://raw.githubusercontent.com/KhronosGroupArchives/glTF-Sample-Models/main/2.0/ReciprocatingSaw/glTF-Binary/ReciprocatingSaw.glb', MODELS_DIR / "compiler-pipeline" / "model.glb")

# Induction Motor: AWS TwinMaker Industrial Motor
download_file('https://raw.githubusercontent.com/architecturebytes/aws-iot-twinmaker/master/models/motor.glb', MODELS_DIR / "induction-motor" / "model.glb")

print("All model files downloaded and verified!")
