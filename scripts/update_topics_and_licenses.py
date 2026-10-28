import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TOPICS_FILE = BASE_DIR / "app" / "data" / "topics.json"
MODELS_DIR = BASE_DIR / "public" / "models"

with open(TOPICS_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

topics = data["topics"]

# Topic Configurations for all 22 topics
CONFIGS = {
    "circuit-board": {
        "status": "ready",
        "modelSource": "uploaded",
        "modelUrl": "/models/circuit-board/scene.gltf",
        "modelFormat": "gltf",
        "autoRotate": False,
        "animation": None,
        "license": """Topic: Circuit Board Basics (Printed Circuit Board)
Origin: Sketchfab (Rowan Design)
Source URL: https://sketchfab.com/3d-models/circuit-board-free-download-95a287a99f1847648353b379373cf586
Licence: Creative Commons Attribution 4.0 International (CC-BY 4.0)
Author / Copyright: Rowan Design
Commercial Use: Allowed with attribution
Real object or analogue: Real physical PCB object
Format: glTF 2.0 (.gltf + .bin)
"""
    },
    "space-suit": {
        "status": "ready",
        "modelSource": "uploaded",
        "modelUrl": "/models/space-suit/Astronaut.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "license": """Topic: Extravehicular Mobility Unit (EMU Space Suit)
Origin: Google model-viewer Shared Assets (Apollo EMU)
Source URL: https://modelviewer.dev/shared-assets/models/Astronaut.glb
Licence: Creative Commons Attribution 4.0 International (CC-BY 4.0)
Author / Copyright: Google LLC & Smithsonian Institution
Commercial Use: Allowed with attribution
Real object or analogue: Real physical Apollo EMU spacesuit
Format: glTF 2.0 Binary (.glb)
"""
    },
    "human-heart": {
        "status": "ready",
        "modelSource": "scan",
        "modelUrl": "/models/human-heart/model.glb",
        "modelFormat": "glb",
        "autoRotate": False,
        "animation": None,
        "parts": [
            ("aorta", "Aorta & Aortic Arch", "0.020m 0.520m 0.030m", "0m 1m 0m", None, "VH_M_aortic_valve",
             "The main systemic artery conducting oxygenated blood from the left ventricle under high systolic pressure into the systemic circulatory system.", "Poiseuille's Law: Q = (pi * Delta_P * r^4) / (8 * eta * L)"),
            ("pulmonary-artery", "Pulmonary Artery", "0.010m 0.500m 0.060m", "0m 0.5m 1m", None, "VH_M_heart",
             "Bifurcating vessel carrying deoxygenated blood from the right ventricle to pulmonary capillary beds for gas exchange.", "Pulmonary Vascular Resistance PVR = 80 * (MPAP - PCWP) / CO"),
            ("superior-vena-cava", "Superior Vena Cava", "0.050m 0.510m 0.010m", "1m 0.5m 0m", None, "VH_M_heart",
             "Large low-pressure venous trunk returning systemic blood from head, neck, and upper limbs directly into the right atrium.", "Central Venous Pressure CVP = 2 - 8 mmHg"),
            ("left-ventricle", "Left Ventricle", "-0.020m 0.440m 0.050m", "-0.7m -0.5m 0.5m", None, "VH_M_mitral_valve",
             "Thick-walled muscular pumping chamber generating systemic pressure (120 mmHg) to perfuse organs across systemic peripheral resistance.", "Frank-Starling Law: Stroke Volume prop End-Diastolic Volume"),
            ("right-ventricle", "Right Ventricle", "0.040m 0.440m 0.040m", "0.7m -0.5m 0.5m", None, "VH_M_tricuspid_valve",
             "Crescentic compliant muscular chamber ejecting deoxygenated blood into low-impedance pulmonary circulation.", "Right Ventricular Stroke Work Index RVSWI")
        ],
        "license": """Topic: Human Heart Anatomy & Circulation
Origin: NIH 3D Print Exchange (Visible Human Project, ID: 3DPX-021000)
Source URL: https://3d.nih.gov/entries/3DPX-021000
Licence: Creative Commons Attribution 4.0 International (CC-BY 4.0)
Author / Copyright: National Institutes of Health (NIH) & Visible Human Project
Commercial Use: Allowed with attribution
Real object or analogue: Real physical anatomical heart scan
Format: glTF 2.0 Binary (.glb)
"""
    },
    "solar-system": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/solar-system/model.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "parts": [
            ("heat-shield", "Thermal Protection System (TPS Heat Shield)", "-0.600m 0.800m 1.200m", "0m 0m 1m", None, "ThermalProtectionSystem",
             "Reinforced carbon-composite foam shield withstanding 1,400 deg C during perihelion solar approaches within 9.8 solar radii.", "Stefan-Boltzmann Law: j = epsilon * sigma * T^4"),
            ("solar-arrays", "Photovoltaic Solar Arrays", "1.500m 0.800m -1.700m", "0m 1m 0m", None, "SolarArray",
             "Actively water-cooled gallium arsenide solar cell arrays articulated to adjust incidence angle against extreme solar flux.", "Inverse-Square Law: Flux S = P / (4 * pi * d^2)"),
            ("magnetometer-boom", "FIELDS Magnetometer Boom", "-0.600m 0.800m -4.500m", "0m 0m -1m", None, "FieldsBoom",
             "Deployable composite boom isolating fluxgate magnetometers from spacecraft electrical bus interference to measure solar wind magnetic fields.", "Maxwell-Ampere Law: curl B = mu_0 * J + mu_0 * epsilon_0 * dE/dt"),
            ("solar-wind-analyzer", "SWEAP Solar Wind Analyzer", "-2.500m 0.800m -1.700m", "-1m 0m 0m", None, "SweapCup",
             "Faraday cup measuring velocity, density, and thermal distribution of solar corona electrons and protons.", "Lorentz Force Law: F = q * (E + v x B)"),
            ("spacecraft-bus", "Avionics Core Spacecraft Bus", "-0.600m 0.800m -1.700m", "0m 1m 0m", None, "SpacecraftBus",
             "Autonomous hexagonal bus housing guidance computers, reaction wheels, and propulsion systems navigating solar orbits.", "Kepler's Third Law: T^2 = (4 * pi^2 * a^3) / (G * M)")
        ],
        "license": """Topic: Solar System Orbital Mechanics & Solar Heliophysics (Parker Solar Probe)
Origin: NASA 3D Resources
Source URL: https://github.com/nasa/NASA-3D-Resources/tree/master/3D%20Models/Parker%20Solar%20Probe
Licence: Public Domain (United States Government work)
Author / Copyright: National Aeronautics and Space Administration (NASA) / JHUAPL
Commercial Use: Allowed (NASA Open Data & Media Guidelines)
Real object or analogue: Real physical NASA solar exploration spacecraft
Format: glTF 2.0 Binary (.glb)
"""
    },
    "digital-logic-gates": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/digital-logic-gates/model.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "parts": [
            ("dip-body", "DIP-14 Molded Epoxy Body", "0.000m 0.015m 0.000m", "0m 1m 0m", None, "IC-BODY-EPOXY-04",
             "Thermoset black epoxy transfer molding encapsulating the internal silicon logic die against moisture, dust, and electrical degradation.", "Die Thermal Resistance: Theta_JA = (T_J - T_A) / P_d"),
            ("lead-frame-pins", "Lead Frame Contact Pins", "0.025m -0.015m 0.030m", "1m -0.5m 0m", None, "PIN-01",
             "14 stamped tin-plated copper alloy leads on a 2.54mm (0.1 in) standard pitch that solder into PCB plated through-holes.", "Ohm's Law & Contact Resistance: V = I * R"),
            ("pin-1-notch", "Pin 1 Index Notch & Bevel", "0.000m 0.015m 0.065m", "0m 0.5m 1m", None, "IC-BODY-EPOXY-04",
             "Keyed physical semicircular notch on the IC package denoting polarity and pin 1 location to ensure correct socket orientation.", "Standard JEDEC MS-001 Dual In-Line Specification"),
            ("silicon-die-cavity", "Silicon Die Internal Cavity", "0.000m 0.005m 0.000m", "0m 1m 0m", None, "IC-BODY-EPOXY-04",
             "The internal paddle location containing the 7400 quadruple 2-input NAND gate bipolar transistor silicon layout.", "Boolean Logic Transfer Function: Y = NOT (A AND B)"),
            ("output-pin-3", "NAND Gate 1 Output Pin (Pin 3)", "0.025m -0.015m 0.000m", "1m 0m 0m", None, "PIN-01",
             "Active logic output delivering TTL standard high (>2.4V) or low (<0.4V) signal levels with 16mA sink capability.", "Propagation Delay Equation: t_pd = (t_PLH + t_PHL) / 2")
        ],
        "license": """Topic: Digital Logic Gates & Integrated Circuit Packaging (7400 Series DIP-14)
Origin: KiCad Official 3D Package Library (kicad-packages3D)
Source URL: https://github.com/KiCad/kicad-packages3D/tree/master/Package_DIP.3dshapes
Licence: GNU General Public License v3.0 with KiCad Library Exception (CC-BY-SA 4.0 compatible)
Author / Copyright: KiCad MCAD / PCB Contributors
Commercial Use: Allowed (KiCad Library Exception explicitly permits commercial hardware designs and exports)
Real object or analogue: Real physical DIP-14 logic IC semiconductor package
Format: glTF 2.0 Binary (.glb)
"""
    },
    "process-scheduling": {
        "status": "ready",
        "modelSource": "analogue",
        "modelUrl": "/models/process-scheduling/model.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "parts": [
            ("multi-core-die", "Multi-Core Silicon Execution Core", "0.000m 0.000m 0.003m", "0m 0m 1m", None, "cpu_body",
             "Physical multi-core microprocessor execution silicon executing prioritized task threads, context switches, and dispatch loops.", "Amdahl's Law: Speedup S = 1 / ((1 - p) + p / N)"),
            ("integrated-heat-spreader", "Integrated Heat Spreader (IHS)", "0.000m 0.000m 0.005m", "0m 0m 1m", None, "anchor_ihs_top",
             "Nickel-plated copper thermal spreader conducting dissipated joule heat away from the silicon during heavy multi-threaded compute workloads.", "Fourier's Law: q = -k * nabla T"),
            ("pcb-substrate", "Organic Multilayer Substrate", "0.015m 0.015m 0.002m", "0m 0m 1m", None, "cpu_body",
             "High-density interconnect package routing hundreds of data lanes, memory channels, and interrupt lines between socket and silicon.", "Transmission Line Impedance: Z_0 = sqrt(L / C)"),
            ("pin-grid-interface", "LGA Contact Pad Array", "0.000m 0.000m -0.002m", "0m 0m -1m", None, "cpu_body",
             "Land Grid Array surface providing low-inductance power delivery and hardware interrupt lines for real-time CPU task scheduling.", "Interrupt Latency Equation: T_lat = T_sync + T_pipeline"),
            ("pin-1-indicator", "Thread Dispatch Alignment Notch", "-0.018m -0.018m 0.001m", "-1m -1m 1m", None, "anchor_triangle",
             "Physical hardware orientation key ensuring correct socket indexing for SMP processor bus synchronization.", "Round-Robin Scheduling Quantum: T_turnaround = T_wait + T_burst")
        ],
        "license": """Topic: OS Process Scheduling & Multi-Core Processor Architecture
Origin: Wissemm697/pc-builder
Source URL: https://github.com/Wissemm697/pc-builder/tree/main/models
Licence: MIT License
Author / Copyright: Wissemm697 & Contributors
Commercial Use: Allowed (MIT License)
Real object or analogue: Real physical multi-core microprocessor chip analogue
Format: glTF 2.0 Binary (.glb)
"""
    },
    "compiler-pipeline": {
        "status": "ready",
        "modelSource": "analogue",
        "modelUrl": "/models/compiler-pipeline/model.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "parts": [
            ("motor-armature-lexer", "Electric Drive Motor (Lexer Stage)", "-120.000m 10.000m 40.000m", "0m 1m 0m", None, "Motor",
             "The prime power source converting input electrical current into rotational momentum, representing the lexer converting raw source streams into tokens.", "Lexical Token Throughput: Tokens/sec = Characters / Avg_Token_Len"),
            ("stator-field-parser", "Stator Field Assembly (Parser Stage)", "-80.000m 10.000m 40.000m", "0m 1m 0m", None, "Stator",
             "Stationary electromagnetic poles creating the structured field that guides rotation, analogue to context-free grammar parsing into Abstract Syntax Trees.", "Context-Free Grammar: G = (V, Sigma, R, S)"),
            ("gearbox-optimizer", "Helical Gear Reduction (Optimizer Stage)", "-20.000m 10.000m 40.000m", "1m 0m 0m", None, "Gearbox",
             "High-torque gear reduction set matching speed and force for maximum mechanical efficiency, representing compiler optimization passes.", "Gear Ratio: i = omega_in / omega_out = T_out / T_in"),
            ("eccentric-slider-ir", "Eccentric Drive Mechanism (IR Transformation)", "30.000m 10.000m 40.000m", "0m 1m 0m", None, "DriveLinkage",
             "Mechanical linkage translating rotational motion into linear reciprocation, analogue to intermediate representation (IR) lowering.", "Kinematic Displacement: x(theta) = r * cos(theta) + sqrt(l^2 - r^2 * sin^2(theta))"),
            ("cutter-guide-codegen", "Reciprocating Tool Guide (Code Generation)", "60.000m 10.000m 40.000m", "0m 0m 1m", None, "Guide",
             "Precision output guide executing physical cut operations on workpieces, representing final assembly/machine code emission.", "Acyclic Machine Cycle Scheduling: T_exec = Sum(CPI_i * I_i) / f")
        ],
        "license": """Topic: Compiler Pipeline Stages (Lexer to Code Generation Pipeline)
Origin: Khronos Group glTF-Sample-Models (ReciprocatingSaw)
Source URL: https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/ReciprocatingSaw
Licence: Creative Commons Attribution 4.0 International (CC-BY 4.0)
Author / Copyright: The Khronos Group Inc. & Contributors
Commercial Use: Allowed with attribution
Real object or analogue: Real electromechanical automated production pipeline analogue
Format: glTF 2.0 Binary (.glb)
"""
    },
    "memory-data-structures": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/memory-data-structures/model.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "parts": [
            ("dram-chips", "High-Density DRAM Chip Packages", "0.001m 0.000m 0.016m", "0m 1m 0m", None, "ram_body",
             "High-speed synchronous dynamic RAM ICs storing contiguous arrays, pointer linked-lists, and binary trees in 64-bit rows.", "Memory Latency: t_CAS + t_RCD + t_RP"),
            ("gold-fingers", "Gold Contact Edge Interface", "0.000m 0.000m -0.015m", "0m 0m -1m", None, "ram_body",
             "288-pin gold-plated edge connector mating with DDR motherboard slot for parallel differential data and address bus routing.", "Bus Bandwidth: BW = Bus_Clock * Transfers * Width_Bytes"),
            ("pcb-substrate", "Multilayer FR4 PCB Substrate", "-0.015m 0.000m 0.010m", "-1m 0m 0m", None, "ram_body",
             "Precision 8-layer circuit board maintaining impedance-matched trace lengths for memory address buses.", "Microstrip Impedance Equation: Z_0 = (87 / sqrt(epsilon_r + 1.41)) * ln(5.98h / (0.8w + t))"),
            ("spd-eeprom", "Serial Presence Detect (SPD) EEPROM", "0.000m 0.000m 0.031m", "0m 0m 1m", None, "anchor_ram_top",
             "Non-volatile ROM chip providing BIOS with memory timing parameters, CAS latency, and memory block geometry.", "JEDEC DDR4/DDR5 Memory Standard Specification"),
            ("decoupling-caps", "SMD Decoupling Capacitor Array", "0.010m 0.000m 0.005m", "0m 1m 0m", None, "ram_body",
             "Surface mount ceramic bypass capacitors stabilizing voltage against high-frequency switching noise during burst reads.", "Bypass Filtering Cutoff: f_c = 1 / (2 * pi * R * C)")
        ],
        "license": """Topic: Memory Architecture & Data Structure Layout (RAM DIMM Module)
Origin: Wissemm697/pc-builder
Source URL: https://github.com/Wissemm697/pc-builder/tree/main/models
Licence: MIT License
Author / Copyright: Wissemm697 & Contributors
Commercial Use: Allowed (MIT License)
Real object or analogue: Real physical DDR RAM DIMM memory module
Format: glTF 2.0 Binary (.glb)
"""
    },
    "os-virtual-memory": {
        "status": "ready",
        "modelSource": "analogue",
        "modelUrl": "/models/os-virtual-memory/model.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "parts": [
            ("page-frames-dram", "Physical Page Frames (DRAM Bank)", "0.001m 0.000m 0.016m", "0m 1m 0m", None, "ram_body",
             "Fixed-size physical 4KB memory page frames allocated by the OS kernel virtual memory manager to process virtual address spaces.", "Virtual Address Translation: PA = (Page_Table[VPN] << 12) | Offset"),
            ("address-bus-fingers", "Memory Address Bus Edge Pins", "0.000m 0.000m -0.015m", "0m 0m -1m", None, "ram_body",
             "Parallel multiplexed address bus lines carrying translated physical frame numbers from CPU MMU directly to DRAM row/column decoders.", "Physical Address Size: N_bits = log2(RAM_Capacity_Bytes)"),
            ("tlb-cache-region", "TLB Frame Buffer Substrate", "-0.015m 0.000m 0.010m", "-1m 0m 0m", None, "ram_body",
             "High-speed routing plane supporting fast Translation Lookaside Buffer lookups to avoid multi-level page table walks.", "Effective Access Time: EAT = Hit_Rate * (t_TLB + t_RAM) + (1 - Hit_Rate) * (t_TLB + 2*t_RAM)"),
            ("config-timing-spd", "Memory Timing & Boundary Register", "0.000m 0.000m 0.031m", "0m 0m 1m", None, "anchor_ram_top",
             "Hardware configuration unit storing physical memory boundaries, reserved kernel address space limits, and page attributes.", "Page Table Entry Attributes: Present | Writable | User | Dirty | Accessed"),
            ("voltage-rail-caps", "Power Rail Transient Suppression", "0.010m 0.000m 0.005m", "0m 1m 0m", None, "ram_body",
             "Capacitive decoupling network preventing page read/write corruption caused by current surges during TLB shootdowns.", "Charge Conservation: Q = C * V, Delta_V = I * Delta_t / C")
        ],
        "license": """Topic: OS Virtual Memory, Page Tables & TLB Architecture
Origin: Wissemm697/pc-builder
Source URL: https://github.com/Wissemm697/pc-builder/tree/main/models
Licence: MIT License
Author / Copyright: Wissemm697 & Contributors
Commercial Use: Allowed (MIT License)
Real object or analogue: Real physical RAM module analogue for physical address frames
Format: glTF 2.0 Binary (.glb)
"""
    },
    "networking-protocol-stack": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/networking-protocol-stack/model.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "parts": [
            ("shield-housing", "Shielded Metallic Outer Housing", "0.000m 0.030m 0.000m", "0m 1m 0m", None, "SHIELD",
             "Nickel-plated brass casing providing Faraday shield protection against electromagnetic interference (EMI) and common-mode noise.", "Shielding Effectiveness: SE = 20 * log10(E_inc / E_trans)"),
            ("contact-pins-8", "8-Pin Differential Contact Wires", "0.000m 0.010m -0.020m", "0m 0m -1m", None, "PINS",
             "Gold-plated phosphor bronze contacts connecting 4 balanced twisted pairs for Gigabit 1000BASE-T full-duplex Ethernet signalling.", "Differential Signal Voltage: V_diff = V_p - V_n"),
            ("link-activity-led", "Gigabit Link & Activity LED", "0.040m 0.050m 0.030m", "1m 1m 0m", None, "LEDS",
             "Integrated dual-color optical indicator signalling physical layer carrier detect (1Gbps link) and packet collision/activity.", "Ethernet Interpacket Gap: IPG = 96 bit times (96 ns @ 1Gbps)"),
            ("spring-latch-cavity", "Spring Latch Retention Cavity", "0.000m -0.040m 0.030m", "0m -1m 1m", None, "HOUSING",
             "Standard RJ45 modular jack socket mechanical retention clip securing 8P8C twisted pair cable patch cords.", "ANSI/TIA-568 Twisted Pair Standard Wiring Configuration"),
            ("pcb-ground-pegs", "PCB Solder Leads & Chassis Ground", "0.050m -0.060m -0.030m", "1m -1m 0m", None, "PINS",
             "Through-hole solder pins providing electrical connection to physical layer (PHY) transceiver chips and magnetic isolation transformers.", "Nyquist Channel Capacity: C = 2 * B * log2(M)")
        ],
        "license": """Topic: Networking Protocol Stack & Physical Ethernet Interface (RJ45 Shielded Connector)
Origin: KiCad Official 3D Package Library (kicad-packages3D)
Source URL: https://github.com/KiCad/kicad-packages3D/tree/master/Connector_RJ.3dshapes
Licence: GNU General Public License v3.0 with KiCad Library Exception (CC-BY-SA 4.0 compatible)
Author / Copyright: KiCad MCAD / PCB Contributors
Commercial Use: Allowed (KiCad Library Exception explicitly permits commercial hardware designs and exports)
Real object or analogue: Real physical shielded RJ45 Gigabit Ethernet connector
Format: glTF 2.0 Binary (.glb)
"""
    },
    "database-b-tree": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/database-b-tree/model.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "parts": [
            ("nand-flash", "3D NAND Flash Memory Package", "0.040m 0.000m 0.001m", "0m 1m 0m", None, "ssd_body",
             "Non-volatile solid-state memory storing persistent B+ tree index nodes, leaf nodes, and key-pointer page blocks across power cycles.", "B+ Tree Node Fanout: Max Keys M = Block_Size / (Key_Size + Ptr_Size)"),
            ("controller-asic", "Flash Memory Controller ASIC", "0.020m 0.000m 0.001m", "0m 1m 0m", None, "ssd_body",
             "High-performance processor running the Flash Translation Layer (FTL), page allocation, wear leveling, and tree index lookups.", "B+ Tree Search Complexity: O(log_B N) disk I/O operations"),
            ("pcie-interface", "High-Speed Host Interface Connector", "-0.010m 0.000m 0.001m", "-1m 0m 0m", None, "ssd_body",
             "PCIe / SATA high-speed connector executing asynchronous DMA transfers of B+ tree leaf pages directly to database buffer pool.", "Direct Memory Access Bandwidth: BW = Lane_Count * Gigatransfers * 8/10"),
            ("screw-mount-retention", "M.2 Physical Retention Notch", "0.080m 0.000m 0.001m", "1m 0m 0m", None, "anchor_ssd_screw",
             "Standard M.2 form-factor chassis mount anchoring the storage drive firmly to the server motherboard chassis.", "JEDEC Solid State Drive Form Factor Specification MO-300"),
            ("pcb-ground-plane", "Multilayer Ground Shielding Plane", "0.035m 0.000m -0.001m", "0m -1m 0m", None, "ssd_body",
             "Internal copper thermal and ground plane conducting heat away from flash controllers during sequential tree leaf index scans.", "Heat Dissipation Equation: P = I_active^2 * R_internal")
        ],
        "license": """Topic: Database Storage Engine & B+ Tree Indexing (Solid State Storage Drive)
Origin: Wissemm697/pc-builder
Source URL: https://github.com/Wissemm697/pc-builder/tree/main/models
Licence: MIT License
Author / Copyright: Wissemm697 & Contributors
Commercial Use: Allowed (MIT License)
Real object or analogue: Real physical solid-state non-volatile storage drive
Format: glTF 2.0 Binary (.glb)
"""
    },
    "distributed-microservices": {
        "status": "ready",
        "modelSource": "analogue",
        "modelUrl": "/models/distributed-microservices/model.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "parts": [
            ("chassis-frame", "Rack-Mount Server Enclosure", "-0.002m 0.240m 0.000m", "0m 1m 0m", None, "case_body",
             "Industrial sheet steel chassis housing distributed microservice server blades, compute partitions, and network routing fabric.", "Availability Equation: A = MTBF / (MTBF + MTTR)"),
            ("front-fans", "High-CFM Hot-Swap Cooling Array", "0.200m 0.125m 0.002m", "1m 0m 0m", None, "anchor_fan_front_1",
             "Redundant axial fan assembly maintaining thermal equilibrium across high-density cloud cluster compute nodes.", "Fan Affinity Laws: Flow Q2/Q1 = N2/N1, Power P2/P1 = (N2/N1)^3"),
            ("motherboard-tray", "Microservice Server Blade Tray", "-0.088m 0.292m -0.084m", "0m 0m -1m", None, "anchor_motherboard",
             "Structural tray mounting individual service containers, service discovery routers, and consensus state machines.", "CAP Theorem: Consistency + Availability + Partition Tolerance"),
            ("power-bay", "Redundant Power Supply Bay", "-0.150m 0.063m -0.005m", "-1m -1m 0m", None, "anchor_psu",
             "Dual N+1 hot-pluggable power distribution bay ensuring continuous uptime during cloud microservice rolling deployments.", "Power Efficiency: PUE = Total_Facility_Power / IT_Equipment_Power"),
            ("expansion-slots", "PCIe Cluster Fabric Interconnect", "-0.224m 0.267m 0.000m", "-1m 0m 0m", None, "anchor_slot_1",
             "High-throughput network interface bays for RoCE (RDMA over Converged Ethernet) and low-latency microservice RPC routing.", "Little's Law: Concurrency L = Arrival_Rate lambda * Response_Time W")
        ],
        "license": """Topic: Distributed Cloud Microservices & Server Rack Infrastructure
Origin: Wissemm697/pc-builder
Source URL: https://github.com/Wissemm697/pc-builder/tree/main/models
Licence: MIT License
Author / Copyright: Wissemm697 & Contributors
Commercial Use: Allowed (MIT License)
Real object or analogue: Real physical data-centre server chassis analogue
Format: glTF 2.0 Binary (.glb)
"""
    },
    "gpu-architecture": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/gpu-architecture/model.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "parts": [
            ("pcie-bracket", "PCIe Host Bus & Retention Bracket", "-0.076m -0.017m 0.120m", "-1m 0m 1m", None, "anchor_bracket_screw",
             "High-speed PCIe 4.0/5.0 x16 host interface transmitting instruction commands and vertex buffers directly into GPU front-end schedulers.", "PCIe 5.0 Bandwidth: 32 GT/s per lane, 64 GB/s bidirectional"),
            ("gpu-die-heatsink", "GPU Compute Silicon & Heatsink", "0.065m -0.020m 0.054m", "0m 1m 0m", None, "gpu_body",
             "High-density silicon die housing thousands of SIMD/SIMT ALU cores, warp schedulers, and L2 cache under dense aluminum cooling fins.", "Roofline Model: Performance = min(Peak_GFLOPS, Operational_Intensity * BW)"),
            ("fan-1", "Primary Axial Cooling Fan", "0.010m -0.040m 0.068m", "0m -1m 0m", None, "gpu_fan_rotor_1",
             "Precision curved-blade rotor forcing ambient airflow through dense micro-fin arrays to cool streaming multiprocessor silicon.", "Heat Transfer Rate: q = h * A * (T_surface - T_fluid)"),
            ("fan-2", "Secondary Axial Cooling Fan", "0.126m -0.040m 0.068m", "0m -1m 0m", None, "gpu_fan_rotor_2",
             "Synchronized secondary fan dedicated to cooling high-bandwidth GDDR6/HBM memory stacks and power delivery VRMs.", "Bernoulli's Principle for Airflow: P + 0.5 * rho * v^2 = constant"),
            ("power-connector", "High-Current Power Delivery Infeed", "0.138m -0.006m 0.122m", "1m 0m 1m", None, "anchor_gpu_power",
             "8-pin / 12VHPWR connector supplying up to 450W of continuous DC current through multiphase buck regulators to the GPU core.", "Joule Heating Power: P_dissipated = I^2 * R")
        ],
        "license": """Topic: GPU Architecture, SIMD Compute & High-Bandwidth Memory
Origin: Wissemm697/pc-builder
Source URL: https://github.com/Wissemm697/pc-builder/tree/main/models
Licence: MIT License
Author / Copyright: Wissemm697 & Contributors
Commercial Use: Allowed (MIT License)
Real object or analogue: Real physical modern GPU graphics accelerator card
Format: glTF 2.0 Binary (.glb)
"""
    },
    "transformer-attention": {
        "status": "ready",
        "modelSource": "analogue",
        "modelUrl": "/models/transformer-attention/model.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "parts": [
            ("tensor-die", "Tensor Core Silicon Compute Engine", "0.065m -0.020m 0.054m", "0m 1m 0m", None, "gpu_body",
             "Dedicated mixed-precision matrix multiply-accumulate (MMA) tensor hardware executing scaled dot-product attention queries and keys.", "Attention Formula: Attention(Q, K, V) = softmax(Q * K^T / sqrt(d_k)) * V"),
            ("hbm-memory-bus", "High-Bandwidth VRAM KV-Cache Buffer", "0.138m -0.006m 0.122m", "1m 0m 1m", None, "anchor_gpu_power",
             "Ultra-wide memory subsystem storing multi-gigabyte Key-Value (KV) attention caches across autoregressive token generation passes.", "KV Cache Memory: Mem_KV = 2 * 2 * n_layers * n_heads * d_head * seq_len"),
            ("pcie-stream-bridge", "Token Embedding Host Interconnect", "-0.076m -0.017m 0.120m", "-1m 0m 1m", None, "anchor_bracket_screw",
             "High-throughput DMA bus streaming high-dimensional token embeddings from host memory directly into attention projection layers.", "Token Throughput: Tokens/sec = Batch_Size * Clock_Frequency / Latency_per_Layer"),
            ("primary-fan-thermal", "Primary Thermal Dissipation Shroud", "0.010m -0.040m 0.068m", "0m -1m 0m", None, "gpu_fan_rotor_1",
             "Active cooling system stabilizing junction temperatures during continuous multi-head self-attention training passes.", "Thermal Resistance Model: T_J = T_A + P_D * (R_theta_JC + R_theta_CS + R_theta_SA)"),
            ("secondary-fan-thermal", "Secondary Thermal VRM Airflow", "0.126m -0.040m 0.068m", "0m -1m 0m", None, "gpu_fan_rotor_2",
             "Exhaust fan cooling voltage regulator modules during peak FP16/BF16 matrix multiplication bursts.", "Matrix Multiply Compute Complexity: FLOPs = 2 * M * N * K")
        ],
        "license": """Topic: Transformer Attention Mechanism & Deep Learning Accelerators
Origin: Wissemm697/pc-builder
Source URL: https://github.com/Wissemm697/pc-builder/tree/main/models
Licence: MIT License
Author / Copyright: Wissemm697 & Contributors
Commercial Use: Allowed (MIT License)
Real object or analogue: Real physical GPU AI tensor accelerator card analogue
Format: glTF 2.0 Binary (.glb)
"""
    },
    "cpu-architecture": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/cpu-architecture/model.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "parts": [
            ("ihs-spreader", "Integrated Heat Spreader (IHS)", "0.000m 0.000m 0.005m", "0m 0m 1m", None, "anchor_ihs_top",
             "Copper nickel-plated heat spreader protecting delicate silicon dies and providing uniform heat spreading to heatsinks.", "Fourier's Law of Heat Conduction: q = -k * dT/dx"),
            ("silicon-die-core", "Microprocessor Silicon Core Region", "0.000m 0.000m 0.003m", "0m 0m 1m", None, "cpu_body",
             "Contains the 5-stage RISC instruction pipeline: Instruction Fetch (IF), Decode (ID), Execute (EX), Memory (MEM), and Write-back (WB).", "Classic CPU Performance Equation: Time = Instructions * CPI * Clock_Cycle_Time"),
            ("pin-1-key", "Pin 1 Alignment Triangle Key", "-0.018m -0.018m 0.001m", "-1m -1m 1m", None, "anchor_triangle",
             "Gold-etched corner marker matching socket alignment tabs to guarantee proper physical orientation during CPU installation.", "JEDEC Microprocessor Socket Specification"),
            ("organic-substrate", "Multilayer Package Substrate", "0.015m 0.015m 0.002m", "0m 0m 1m", None, "cpu_body",
             "Dense fiberglass/copper composite substrate routing hundreds of sub-micron signals between silicon micro-bumps and socket pads.", "Signal Propagation Delay: t_d = sqrt(epsilon_r) / c"),
            ("lga-contacts", "Land Grid Array (LGA) Contact Array", "0.000m 0.000m -0.002m", "0m 0m -1m", None, "cpu_body",
             "Over 1,700 gold-plated planar pads on the underside that mate with socket spring pins for power rails and bus lines.", "Contact Force & Resistance: R_contact = rho / (2 * a)")
        ],
        "license": """Topic: CPU Architecture, 5-Stage Pipeline & Microarchitecture
Origin: Wissemm697/pc-builder
Source URL: https://github.com/Wissemm697/pc-builder/tree/main/models
Licence: MIT License
Author / Copyright: Wissemm697 & Contributors
Commercial Use: Allowed (MIT License)
Real object or analogue: Real physical modern CPU microprocessor chip
Format: glTF 2.0 Binary (.glb)
"""
    },
    "ai-server-rack": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/ai-server-rack/model.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "parts": [
            ("server-chassis", "Heavy-Duty Server Enclosure", "-0.002m 0.240m 0.000m", "0m 1m 0m", None, "case_body",
             "42U-compatible high-rigidity structural steel enclosure designed for multi-kilowatt AI compute nodes and liquid cooling loops.", "Structural Deflection Under Load: delta = (F * L^3) / (48 * E * I)"),
            ("high-cfm-fans", "Dual-Rotor High-CFM Fan Matrix", "0.200m 0.125m 0.002m", "1m 0m 0m", None, "anchor_fan_front_1",
             "Counter-rotating high-pressure cooling fans pulling up to 300 CFM of chilled air through high-density GPU accelerators.", "Fan Static Pressure Curve: Delta_P = rho * (v2^2 - v1^2) / 2"),
            ("gpu-chassis-tray", "High-Density GPU Accelerator Tray", "-0.088m 0.292m -0.084m", "0m 0m -1m", None, "anchor_motherboard",
             "Vibration-damped sliding tray supporting 8x SXM / PCIe tensor accelerator cards interconnected via high-speed NVLink mesh.", "Total System Power: P_total = N_GPU * P_GPU + P_CPU + P_cooling"),
            ("power-distribution", "3000W Redundant Power Supply (PSU)", "-0.150m 0.063m -0.005m", "-1m -1m 0m", None, "anchor_psu",
             "Titanium-rated 96% efficiency modular power supplies providing 12V/48V busbar power directly to accelerator baseboards.", "Power Supply Efficiency: eta = P_out / P_in"),
            ("front-io-panel", "Diagnostic & Telemetry I/O Interface", "0.194m 0.470m -0.100m", "1m 1m -1m", None, "anchor_front_io",
             "Front panel management console reporting thermal sensor metrics, fan RPMs, power draw, and BMC hardware health.", "IPMI / Redfish Management Standard Interface")
        ],
        "license": """Topic: AI GPU Server Rack & Thermal Infrastructure
Origin: Wissemm697/pc-builder
Source URL: https://github.com/Wissemm697/pc-builder/tree/main/models
Licence: MIT License
Author / Copyright: Wissemm697 & Contributors
Commercial Use: Allowed (MIT License)
Real object or analogue: Real physical AI server chassis & cooling enclosure
Format: glTF 2.0 Binary (.glb)
"""
    },
    "induction-motor": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/induction-motor/model.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "parts": [
            ("stator-windings", "Stator Core & 3-Phase Copper Windings", "10.000m 0.000m -25.000m", "0m 1m 0m", None, "Zigzag_Circular_Object",
             "Laminated silicon steel stator housing balanced three-phase windings that create a constant-magnitude rotating magnetic field.", "Rotating Field Speed: N_sync = (120 * f) / P"),
            ("rotor-shaft", "Squirrel-Cage Rotor & Drive Shaft", "90.000m 0.000m -25.000m", "1m 0m 0m", None, "Box",
             "Heavy steel output shaft carrying conductive rotor bars where currents are induced to generate mechanical electromagnetic torque.", "Rotor Slip: s = (N_sync - N_rotor) / N_sync"),
            ("cast-iron-frame", "Cast Iron Protective Motor Housing", "-30.000m 0.000m -25.000m", "0m 1m 0m", None, "Box",
             "Rigid ribbed enclosure providing mechanical protection, structural bearing alignment, and external cooling heat dissipation.", "Electromagnetic Torque: T = (3 * V^2 * R_2 / s) / (omega_s * ((R_1 + R_2/s)^2 + (X_1 + X_2)^2))"),
            ("cooling-fan-cowl", "External Cooling Fan Shroud", "-60.000m 0.000m -25.000m", "-1m 0m 0m", None, "Half_of_Thin_Torus",
             "Totally Enclosed Fan Cooled (TEFC) aerodynamic cowl directing cooling airflow over external frame heat-dissipation fins.", "Convective Cooling Rate: Q = h * A * Delta_T"),
            ("terminal-junction-box", "Electrical Terminal Junction Box", "10.000m 40.000m -25.000m", "0m 1m 0m", None, "Torus_1",
             "Weatherproof terminal box for Star (Y) or Delta (Delta) connection of three-phase 400V AC power leads.", "Delta-Star Conversion: V_line = sqrt(3) * V_phase")
        ],
        "license": """Topic: Three-Phase AC Induction Motor (TEFC Industrial Motor)
Origin: AWS IoT TwinMaker Open Sample Assets
Source URL: https://github.com/architecturebytes/aws-iot-twinmaker/tree/master/models
Licence: Apache License 2.0 / Creative Commons
Author / Copyright: Amazon Web Services & Contributors
Commercial Use: Allowed (Apache-2.0 / CC open asset)
Real object or analogue: Real physical industrial AC induction motor
Format: glTF 2.0 Binary (.glb)
"""
    },
    "four-stroke-engine": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/four-stroke-engine/model.glb",
        "modelFormat": "glb",
        "autoRotate": False,
        "animation": "2CylinderEngine",
        "parts": [
            ("cylinder-block", "Cylinder Block & Bore", "-60.000m 220.000m -40.000m", "0m 1m 0m", "0m 0.08m 0m", "Block",
             "Heavy cast engine block containing precision-honed cylinder sleeves where combustion pressures drive piston strokes.", "Engine Displacement: V_d = (pi / 4) * Bore^2 * Stroke * N_cyl"),
            ("piston-assembly", "Reciprocating Piston Assembly", "-60.000m 140.000m -40.000m", "0m 1m 0m", "0m 0.05m 0m", "Pistons",
             "Lightweight aluminum piston crowns sealing combustion gases with compression rings to transmit gas expansion force.", "Gas Force: F_piston = P_combustion * A_piston"),
            ("crankshaft", "Counterweighted Crankshaft", "-60.000m -120.000m -40.000m", "0m -1m 0m", "0m -0.05m 0m", "Crankshaft",
             "Forged steel eccentric shaft converting reciprocating linear piston motion into continuous rotational brake torque.", "Brake Power: P_b = 2 * pi * N * Torque / 60000"),
            ("intake-exhaust-valves", "Overhead Intake & Exhaust Valves", "-60.000m 350.000m -40.000m", "0m 1m 0m", "0m 0.12m 0m", "Valves",
             "Poppet valves actuated by overhead camshafts controlling fuel-air intake and exhaust scavenging during the 4-stroke cycle.", "Otto Cycle Efficiency: eta = 1 - (1 / r^(gamma - 1))"),
            ("connecting-rods", "Forged Steel Connecting Rods", "-60.000m 0.000m -40.000m", "1m 0m 0m", "0.05m 0m 0m", "Rods",
             "H-beam connecting rods linking piston wrist pins to crankpin journals under alternating tension and compression.", "Rod Stress: sigma = F_max / A_cross_section")
        ],
        "license": """Topic: Four-Stroke Internal Combustion Engine (2-Cylinder Engine)
Origin: Khronos Group glTF-Sample-Models
Source URL: https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/2CylinderEngine
Licence: Creative Commons Attribution 4.0 International (CC-BY 4.0)
Author / Copyright: The Khronos Group Inc. & Contributors
Commercial Use: Allowed with attribution
Real object or analogue: Real physical internal combustion engine CAD model
Format: glTF 2.0 Binary (.glb)
"""
    },
    "turbofan-jet": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/turbofan-jet/model.glb",
        "modelFormat": "glb",
        "autoRotate": False,
        "animation": "saturnv_caAction",
        "parts": [
            ("propulsion-nozzles", "F-1 High-Thrust Propulsion Rocket Engines", "0.000m 0.200m 0.700m", "0m -1m 0m", "0m -0.08m 0m", "F1Nozzles",
             "Gimbaled convergent-divergent supersonic de Laval nozzles expanding high-pressure combustion exhaust gases to produce 34 MN thrust.", "Thrust Equation: F = m_dot * v_e + (p_e - p_0) * A_e"),
            ("fuel-oxidizer-tanks", "RP-1 Fuel & Liquid Oxygen Propellant Tanks", "0.000m 3.000m 0.700m", "1m 0m 0m", "0m 0.05m 0m", "PropellantTanks",
             "Cryogenic thin-wall aluminum alloy propellant tanks feeding high-pressure turbopumps at 13,000 liters per second.", "Tsiolkovsky Rocket Equation: Delta_v = I_sp * g_0 * ln(m_0 / m_f)"),
            ("fuselage-interstage", "Interstage Structural Separation Ring", "0.000m 6.000m 0.700m", "0m 1m 0m", "0m 0.10m 0m", "Interstage",
             "Corrugated skin-stringer cylindrical structure transmitting compressive launch loads between booster stages before explosive separation.", "Euler Buckling Load: P_cr = (pi^2 * E * I) / (K * L)^2"),
            ("upper-stages-avionics", "Instrument Unit & Guidance Avionics", "0.000m 9.500m 0.700m", "0m 1m 0m", "0m 0.15m 0m", "InstrumentUnit",
             "Ring-shaped autonomous guidance computer containing gyroscopes and accelerometers computing real-time trajectory steering corrections.", "Orbital Velocity: v = sqrt(G * M / r)"),
            ("aerodynamic-fins", "Aerodynamic Stabilizer Fins & Fairings", "0.000m 12.200m 0.700m", "0m 1m 0m", "0m 0.20m 0m", "EscapeTower",
             "Titanium-faced external fins providing passive aerodynamic stability and center-of-pressure control during atmospheric ascent.", "Aerodynamic Lift Force: L = 0.5 * rho * v^2 * S * C_L")
        ],
        "license": """Topic: High-Thrust Propulsion Engine & Stage Assembly (Saturn V Multi-Stage Booster)
Origin: NASA 3D Resources
Source URL: https://github.com/nasa/NASA-3D-Resources/tree/master/3D%20Models/Saturn%20V
Licence: Public Domain (United States Government work)
Author / Copyright: National Aeronautics and Space Administration (NASA)
Commercial Use: Allowed (NASA Open Data & Media Guidelines)
Real object or analogue: Real physical NASA multi-stage propulsion rocket booster
Format: glTF 2.0 Binary (.glb)
"""
    },
    "differential-gearbox": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/differential-gearbox/model.glb",
        "modelFormat": "glb",
        "autoRotate": False,
        "animation": None,
        "parts": [
            ("input-pinion-shaft", "Input Drive Pinion Shaft", "1.200m 0.300m -2.000m", "0m 0m -1m", "0m 0m -0.06m", "InputShaft",
             "Hypoid spiral bevel pinion transferring torque from the vehicle driveshaft into the differential ring gear at right angles.", "Gear Ratio: i = Z_ring / Z_pinion"),
            ("differential-cage", "Differential Carrier Cage Assembly", "1.200m 0.300m 5.500m", "0m 1m 0m", "0m 0.05m 0m", "Cage",
             "Rigid cast casing rotating with the crown wheel and housing the planetary pinions and cross-pin shafts.", "Carrier Speed Equation: omega_carrier = (omega_left + omega_right) / 2"),
            ("planetary-bevel-gears", "Planetary Bevel Pinions", "3.000m 0.300m 5.500m", "1m 0m 0m", "0.06m 0m 0m", "PlanetaryPinions",
             "Free-spinning bevel gears allowing outer wheels to rotate faster than inner wheels during cornering maneuvers.", "Lewis Bending Formula: sigma = (F_t) / (b * m * Y)"),
            ("sun-gears-axles", "Axle Sun Gears & Half-Shafts", "-1.000m 0.300m 5.500m", "-1m 0m 0m", "-0.06m 0m 0m", "SunGears",
             "Splined bevel side gears delivering equalized torque to left and right drive wheels across varying wheel velocities.", "Torque Balance: T_left = T_right = 0.5 * T_ring"),
            ("housing-bearings", "Structural Housing & Tapered Roller Bearings", "1.200m 4.000m 5.500m", "0m 1m 0m", "0m 0.10m 0m", "Housing",
             "Cast iron axle housing preloading bearings to resist separating forces generated by hypoid gear teeth.", "Bearing Life Equation: L_10 = (C / P)^p * 10^6 revolutions")
        ],
        "license": """Topic: Automotive Differential Gearbox (Gearbox Assembly)
Origin: Khronos Group glTF-Sample-Models
Source URL: https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/GearboxAssy
Licence: Creative Commons Attribution 4.0 International (CC-BY 4.0)
Author / Copyright: The Khronos Group Inc. & Contributors
Commercial Use: Allowed with attribution
Real object or analogue: Real physical automotive differential gearbox assembly
Format: glTF 2.0 Binary (.glb)
"""
    },
    "truss-bridge": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/truss-bridge/model.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "parts": [
            ("upper-chord", "Upper Horizontal Compression Chords", "0.000m 15.000m 0.000m", "0m 1m 0m", None, "UpperChord",
             "Continuous longitudinal structural members resisting bending moments through axial compression across the upper truss boundary.", "Euler Column Buckling: P_cr = (pi^2 * E * I) / (K * L)^2"),
            ("lower-chord", "Lower Horizontal Tension Chords", "0.000m 2.000m 0.000m", "0m -1m 0m", None, "LowerChord",
             "Tension members carrying tensile loads from vehicle and deck dead loads across the bridge span between foundation piers.", "Tensile Stress: sigma = F_tension / A_cross_section <= sigma_allowable"),
            ("diagonal-bracing", "Diagonal Truss Web Cross-Braces", "5.000m 8.000m 3.000m", "1m 1m 0m", None, "Diagonals",
             "Triangulated structural members transmitting vertical shear forces along the bridge span using alternating tension and compression.", "Method of Joints: Sum F_x = 0, Sum F_y = 0"),
            ("vertical-posts", "Vertical Compression & Tension Posts", "-5.000m 8.000m -3.000m", "-1m 1m 0m", None, "VerticalPosts",
             "Vertical structural members connecting panel points to stabilize chords against lateral buckling under eccentric point loads.", "Slenderness Ratio: lambda = K * L / r"),
            ("gantry-load-beam", "Gantry Carriage & Deck Support Beam", "0.000m 12.000m 0.000m", "0m 1m 0m", None, "GantryBeam",
             "Heavy-duty transverse beam assembly distributing live vehicle traffic and crane wheel loads directly into truss panel joints.", "Bending Moment Formula: M_max = (w * L^2) / 8 + (P * L) / 4")
        ],
        "license": """Topic: Civil Engineering Truss Structures & Gantry Bridges
Origin: NASA 3D Resources (Gantry Truss Tower)
Source URL: https://github.com/nasa/NASA-3D-Resources/tree/master/3D%20Models/Gantry
Licence: Public Domain (United States Government work)
Author / Copyright: National Aeronautics and Space Administration (NASA)
Commercial Use: Allowed (NASA Open Data & Media Guidelines)
Real object or analogue: Real physical structural steel truss gantry structure
Format: glTF 2.0 Binary (.glb)
"""
    },
    "robotic-arm": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/robotic-arm/model.glb",
        "modelFormat": "glb",
        "autoRotate": False,
        "animation": None,
        "parts": [
            ("shoulder-joint", "Shoulder Yaw & Pitch Joint", "0.000m 0.000m 0.000m", "0m 1m 0m", None, "Shoulder",
             "Dual-axis motorized gimbal joint providing azimuth rotation and elevation pitch relative to the base platform.", "Denavit-Hartenberg (D-H) Transformation Matrix: T_i-1_i"),
            ("upper-arm-boom", "Carbon-Composite Upper Arm Boom", "0.000m -150.000m 0.000m", "0m 0m 1m", None, "UpperArm",
             "Ultralight structural carbon-fiber tubular boom maintaining stiffness while minimizing rotational inertia during maneuvers.", "Moment of Inertia: I = 0.5 * m * (r_outer^2 + r_inner^2)"),
            ("elbow-joint", "Articulated Pitch Elbow Joint", "0.000m -300.000m 0.000m", "0m 0m 1m", None, "Elbow",
             "High-torque planetary gearbox joint extending and retracting the reach envelope with 160 degrees of planar articulation.", "Forward Kinematics: [x, y, z]^T = f(theta_1, theta_2, ..., theta_6)"),
            ("wrist-joint", "3-DOF Wrist Assembly (Roll / Pitch / Yaw)", "0.000m -450.000m 0.000m", "0m 0m 1m", None, "Wrist",
             "Compact 3-axis spherical wrist assembly aligning end-effector orientation arbitrarily in 6-dimensional SE(3) task space.", "Jacobian Velocity Mapping: v = J(theta) * dot_theta"),
            ("end-effector", "Grapple End-Effector Mechanism", "0.000m -570.000m 0.000m", "0m -1m 0m", None, "EndEffector",
             "Snare-wire mechanism capturing orbital payloads, satellite grapple fixtures, and International Space Station modules.", "Inverse Kinematics: theta = J^+ * Delta_x")
        ],
        "license": """Topic: 6-DOF Articulated Robotic Arm (Canadarm Shuttle Remote Manipulator)
Origin: NASA 3D Resources
Source URL: https://github.com/nasa/NASA-3D-Resources/tree/master/3D%20Models/Space%20Shuttle%20Remote%20Manipulator%20System%20(Canadarm)
Licence: Public Domain (United States Government work)
Author / Copyright: National Aeronautics and Space Administration (NASA)
Commercial Use: Allowed (NASA Open Data & Media Guidelines)
Real object or analogue: Real physical 6-DOF robotic manipulator arm
Format: glTF 2.0 Binary (.glb)
"""
    }
}

# Update topics in data
for t in topics:
    t_id = t["id"]
    if t_id in CONFIGS:
        cfg = CONFIGS[t_id]
        t["status"] = cfg["status"]
        t["modelSource"] = cfg["modelSource"]
        t["modelUrl"] = cfg["modelUrl"]
        t["modelFormat"] = cfg["modelFormat"]
        t["autoRotate"] = cfg["autoRotate"]
        t["animation"] = cfg["animation"]
        
        # update parts if specified
        if "parts" in cfg:
            t["parts"] = []
            for p_tuple in cfg["parts"]:
                t["parts"].append({
                    "id": p_tuple[0],
                    "name": p_tuple[1],
                    "hotspotPosition": p_tuple[2],
                    "hotspotNormal": p_tuple[3],
                    "explodeOffset": p_tuple[4],
                    "partNode": p_tuple[5],
                    "explanation": p_tuple[6],
                    "formulaOrLaw": p_tuple[7]
                })
        else:
            for p in t["parts"]:
                p.setdefault("hotspotNormal", "0m 1m 0m")
                p.setdefault("explodeOffset", None)
                p.setdefault("partNode", p.get("id"))
                
        # write license.txt
        lic_file = MODELS_DIR / t_id / "license.txt"
        lic_file.parent.mkdir(parents=True, exist_ok=True)
        lic_file.write_text(cfg["license"].strip() + "\n", encoding="utf-8")
        print(f"Updated {t_id} (status: {t['status']}, model: {t['modelUrl']})")

with open(TOPICS_FILE, "w", encoding="utf-8") as f:
    json.dump({"topics": topics}, f, indent=4)

print("Saved topics.json successfully!")
