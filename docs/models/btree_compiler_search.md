# 3D Model Sourcing Log: B+ Tree and Compiler Pipeline (§3 & §7.1)

**Specification:** `PRISMED_AGENT_FIX_BTREE_COMPILER.md` (§3)  
**Date:** 2026-10-29  
**Scope:** `database-b-tree` (DBT-01) and `compiler-pipeline` (CP-01)  

---

## 1. Search Log — Topic 1: B+ Tree Storage Engine (`database-b-tree`)

**Target Object:** Hard Disk Drive (HDD) with separable platters, read/write heads, actuator arm, spindle motor, and controller board.

| Priority | Source | Search Query / URL | Result | Finding & Licence Assessment |
|---|---|---|---|---|
| 1 | Repository Folders | `public/models/database-b-tree/model.glb` | **Rejected & Deleted** | Current file was `Wissemm697/pc-builder` SSD (`models/ssd.glb`). Depicts a flat card with an edge connector and round component. Rejected per owner review: does not show a mechanical storage engine. File deleted. |
| 2 | GitHub Repositories | `hard-drive glb`, `hdd cutaway gltf`, `hard drive 3d model` | **Negative** | Searched GitHub API. Found zero open, redistributable `.glb`/`.gltf` HDD models with separate nodes for platters and actuator arm. Checked `Wissemm697/pc-builder` tree: only contains `ssd.glb`, `case.glb`, `ram.glb`, `gpu.glb`, `cpu.glb`, no HDD. |
| 3 | model-viewer Shared Assets | `google/model-viewer/packages/shared-assets/models` | **Negative** | Inspected shared assets tree: includes `Astronaut.glb`, `NeilArmstrong.glb`, `Horse.glb`, `RobotExpressive.glb`, `RocketShip.glb`. No computer storage hardware or HDD models present. |
| 4 | Khronos glTF Sample Assets | `KhronosGroup/glTF-Sample-Assets/Models` & `glTF-Sample-Models/2.0` | **Negative** | Inspected full asset catalog. Contains engines (`2CylinderEngine`), mechanical assemblies (`GearboxAssy`), and primitives. Zero HDD or disk storage assets. |
| 5 | Sketchfab (CC-BY / CC0) | `"hard disk drive" CC-BY`, `"hard drive" CC0` | **Unreachable / Blocked** | Sketchfab API requires authenticated user account session to download assets. Automated agent download blocked. Several photogrammetry scans exist (e.g., GCarter06), but raw geometry is single-mesh photogrammetry without separable internal nodes. |
| 6 | Smithsonian 3D & NASA 3D | `3d.si.edu`, `nasa/NASA-3D-Resources` | **Negative / 403** | Searched Smithsonian Open Access: automated requests returned `403 Forbidden`. No hard disk drives in Smithsonian 3D. NASA 3D Resources searched: spacecraft, gantry, Canadarm, Saturn V, but no commercial computer disk storage drives. |

---

## 2. Search Log — Topic 2: Compiler Pipeline (`compiler-pipeline`)

**Target Object:** Real physical multi-stage sequential production process (industrial assembly line or printing press with distinct ordered stages: input feed, processing/lexing, transformation/opt, output generation).

| Priority | Source | Search Query / URL | Result | Finding & Licence Assessment |
|---|---|---|---|---|
| 1 | Repository Folders | `public/models/compiler-pipeline/model.glb` | **Rejected & Deleted** | Current file was `KhronosGroup/glTF-Sample-Models/2.0/ReciprocatingSaw`. Depicts a hand-held power saw with reciprocating blade. Rejected per owner review: completely unrelated to compilation. File deleted. |
| 2 | GitHub Repositories | `assembly-line glb`, `production line 3d model`, `conveyor gltf` | **Negative** | Searched GitHub API for open CAD models of multi-stage assembly lines. `AdityaWijayanto19/factory-glb-assembly` checked: configuration repo with no redistributable GLB assets on GitHub. No redistributable open-source multi-unit production lines found. |
| 3 | model-viewer Shared Assets | `google/model-viewer/packages/shared-assets/models` | **Negative** | No multi-stage industrial lines or printing presses in sample assets. |
| 4 | Khronos glTF Sample Assets | `KhronosGroup/glTF-Sample-Assets/Models` | **Negative** | No printing press or assembly line models in Khronos sample models. |
| 5 | Sketchfab (CC-BY / CC0) | `"production line" CC-BY`, `"printing press" CC0` | **Unreachable / Blocked** | Automated API access blocked by Sketchfab authentication requirement. |
| 6 | Smithsonian 3D | `3d.si.edu` ("Albion press, Hopkinson & Cope 1845") | **Unreachable / 403** | Smithsonian 3D catalog lists an Albion printing press (National Museum of American History), but automated script requests to `3d.si.edu` returned `403 Forbidden`. |

---

## 3. Honest Outcome (§8)

Per §1 Rule 5, §1 Rule 6, and §8 of `PRISMED_AGENT_FIX_BTREE_COMPILER.md`:
- A model of the wrong object is strictly worse than no model.
- Substituting primitive cubes, cylinders, or unrelated tools is forbidden.
- Since neither authentic multi-part HDD model nor verified open industrial production line model could be sourced without authentication/licence violations, both topics are honestly excluded and set to `status: "not_in_demo"`.
