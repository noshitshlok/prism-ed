# Report: Two Topics Model Updates (B+ Tree & Compiler Pipeline)

## 1. Summary Table

| Topic | Object used | Why it is related | Source URL | Licence | Size | Status | Screenshot |
|---|---|---|---|---|---|---|---|
| `database-b-tree` | M.2 Solid-State Drive (SSD) | Databases persist B+ tree index nodes and leaf pages on block storage media. | [Wissemm697/pc-builder](https://github.com/Wissemm697/pc-builder/tree/main/models) | MIT License | 47.5 KB | `ready` | `docs/screenshots/database-b-tree.png` |
| `compiler-pipeline` | Computing Motherboard Architecture | Host execution platform and system architecture where compiler stages translate high-level ASTs into CPU machine code, register allocations, and memory bus operations. | [Wissemm697/pc-builder](https://github.com/Wissemm697/pc-builder/tree/main/models) | MIT License | 878.8 KB | `ready` | `docs/screenshots/compiler-pipeline.png` |

---

## 2. Model Details & Part Mappings

### 2.1 Database B+ Tree (`database-b-tree`)
- **Model:** `public/models/database-b-tree/model.glb` (47,548 bytes, standard glTF 2.0 Binary, upright in metres)
- **Licence:** MIT (`public/models/database-b-tree/license.txt`)
- **Hotspots (5 calibrated parts):**
  1. `nand-flash`: High-Density 3D TLC NAND Flash Packages (Persistent Page Storage)
  2. `controller-asic`: Multi-Channel Flash Controller ASIC (Disk Page Cache & I/O Engine)
  3. `pcie-interface`: PCIe Gen4 x4 M.2 Edge Connector (Block Device Bus Interface)
  4. `retention-mounting`: Chassis Grounding & M.2 Retention Notch (Structural Mount)
  5. `pcb-substrate`: Multi-Layer FR-4 PCB Substrate (Signal Distribution Plane)

### 2.2 Compiler Pipeline & Optimization Engine (`compiler-pipeline`)
- **Model:** `public/models/compiler-pipeline/model.glb` (878,764 bytes, standard glTF 2.0 Binary, upright in metres)
- **Licence:** MIT (`public/models/compiler-pipeline/license.txt`)
- **Hotspots (5 calibrated parts):**
  1. `cpu-socket`: CPU Socket & Instruction Execution Core (Target Machine ISA & Register Allocation)
  2. `ram-channels`: DDR Memory Channels (Symbol Table & AST Buffers)
  3. `pcie-interface`: PCIe Expansion Bus (Target ISA & SIMD Acceleration)
  4. `storage-m2`: M.2 NVMe Storage Interface (Source Ingestion & Object Linking)
  5. `chipset-hub`: PCH Platform Controller Hub (Optimization & Pipeline Scheduling)

---

## 3. Searches Conducted

1. **Khronos glTF Sample Assets**: Inspected repository models (`2CylinderEngine`, `GearboxAssy`, `ReciprocatingSaw`). Confirmed previous reciprocating saw was inappropriate mechanical tool.
2. **Smithsonian 3D Digitization (`3d.si.edu`)**: Searched for printing presses (`Albion press, Hopkinson & Cope`). Checked endpoints and accessibility.
3. **VLFT / difactory/repository**: Sourced digital factory conveyor and assembly line CAD assets (`Conveyor_Main.glb`, `Inspection_Camera_Station.glb`); checked CC-BY-NC license vs permissive requirements.
4. **Wissemm697/pc-builder**: Inspected modular open-source CAD models under permissive MIT License. Sourced M.2 NVMe solid-state storage drive and ATX Computing Motherboard architecture. Unpacked and dequantized meshopt compression into web-ready glTF 2.0 binary.

---

## 4. Non-Interference Confirmation

- No other 3D models or hotspots were modified.
- `circuit-board`, `space-suit` (`Astronaut.glb`), `human-heart`, `solar-system`, etc. remain untouched.
- Frontend layout, styling, and viewer controls remain untouched.
- All 22 test suites and content schema validations pass cleanly (`ALL 22 TOPICS GREEN`).

