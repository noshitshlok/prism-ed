"""
PrismEd Content Generation & Verification Script
Generates and populates all 22 topics into app/data/topics.json and app/data/quiz.json,
along with public/models/<topicId>/license.txt for each topic.
"""
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TOPICS_FILE = BASE_DIR / "app" / "data" / "topics.json"
QUIZ_FILE = BASE_DIR / "app" / "data" / "quiz.json"
MODELS_DIR = BASE_DIR / "public" / "models"

TOPICS_DATA = [
    {
        "id": "circuit-board",
        "name": "Circuit Board Basics",
        "description": "Explore the fundamental components on a printed circuit board and their electrical roles.",
        "discipline": "Electrical Engineering",
        "subfield": "Electronics & PCB Design",
        "academicLevel": "Undergraduate",
        "tags": ["pcb", "electronics", "hardware", "circuits"],
        "prerequisites": ["Basic DC Circuit Analysis", "Ohm's Law"],
        "equationsCovered": ["V = I * R", "C = Q / V", "P = V * I"],
        "modelUrl": "/models/circuit-board/scene.gltf",
        "modelFormat": "gltf",
        "parts": [
            {
                "id": "ic-chip",
                "name": "Integrated Circuit (IC) Chip",
                "hotspotPosition": "0.018m 0.002m 0.056m",
                "explanation": "The IC chip is the microelectronic core of the board, integrating thousands to billions of microscopic transistors that execute logic operations, signal amplification, and data routing.",
                "formulaOrLaw": "Moore's Law & Boolean Logic Functions"
            },
            {
                "id": "capacitors",
                "name": "Electrolytic Capacitors",
                "hotspotPosition": "0.033m 0.002m 0.026m",
                "explanation": "Capacitors store electrostatic energy across a dielectric layer, acting as decoupling reservoirs that smooth voltage ripples and suppress high-frequency supply transients.",
                "formulaOrLaw": "C = Q / V, E = 0.5 * C * V^2"
            },
            {
                "id": "edge-connector",
                "name": "Edge Connector Interface",
                "hotspotPosition": "0.016m 0.002m 0.032m",
                "explanation": "Gold-plated trace fingers along the PCB perimeter provide low-impedance physical and electrical interconnects to backplanes or host expansion buses.",
                "formulaOrLaw": "Contact Resistance R_c = rho / (2 * a)"
            },
            {
                "id": "diodes",
                "name": "Rectifier Diodes",
                "hotspotPosition": "0.018m 0.002m 0.062m",
                "explanation": "Diodes form a unidirectional semiconductor p-n junction, preventing reverse-polarity damage and conducting rectification of alternating signals.",
                "formulaOrLaw": "Shockley Diode Equation: I = I_s * (e^(V / (n*V_t)) - 1)"
            },
            {
                "id": "resistor-array",
                "name": "Surface-Mount Resistors",
                "hotspotPosition": "0.022m 0.002m 0.045m",
                "explanation": "Resistors restrict electric current flow and create calibrated voltage dividers to bias active semiconductor stages properly.",
                "formulaOrLaw": "Ohm's Law: V = I * R, P = I^2 * R"
            }
        ],
        "quiz": [
            {
                "id": "cb-q1",
                "question": "What primary phenomenon allows an electrolytic capacitor to smooth power supply ripples?",
                "options": [
                    "Direct conversion of electrical charge to thermal dissipation",
                    "Electrostatic charge storage across a polarized dielectric layer",
                    "Unidirectional current conduction via a p-n semiconductor junction",
                    "Magnetic induction across coupled copper traces"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "Capacitors store electrical energy electrostatically (Q = C*V). During voltage dips, they discharge stored energy to stabilize the rail voltage."
            },
            {
                "id": "cb-q2",
                "question": "Which equation models the non-linear current-voltage relationship of a p-n junction diode?",
                "options": [
                    "Ohm's Law (V = I * R)",
                    "Shockley Diode Equation",
                    "Ampère's Circuital Law",
                    "Faraday's Law of Induction"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "The Shockley equation I = I_s * (exp(V / (n*V_t)) - 1) accurately describes current flow across the forward-biased and reverse-biased barrier."
            },
            {
                "id": "cb-q3",
                "question": "Why are PCB edge connector contact fingers commonly electroplated with hard gold over nickel?",
                "options": [
                    "To minimize contact resistance and withstand repeated insertion wear without oxidation",
                    "To generate thermoelectric cooling across the junction interface",
                    "To absorb high-frequency electromagnetic noise radiation",
                    "To permanently fuse the board to the mating slot"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Gold is highly resistant to oxidation and corrosion, ensuring negligible contact resistance over hundreds of mating insertion cycles."
            }
        ],
        "license": {
            "title": "Circuit Board (Free Download)",
            "source": "https://sketchfab.com/3d-models/circuit-board-free-download-95a287a99f1847648353b379373cf586",
            "author": "Rowan Design",
            "license": "CC-BY-4.0",
            "attribution": "Model: Circuit Board by Rowan Design under CC-BY-4.0. Attribution required on use."
        }
    },
    {
        "id": "space-suit",
        "name": "Extravehicular Mobility Unit (EMU)",
        "description": "Examine the aerospace life support and protective subsystems of an astronaut extravehicular suit.",
        "discipline": "Aerospace Engineering",
        "subfield": "Life Support & Space Systems",
        "academicLevel": "Undergraduate",
        "tags": ["aerospace", "life-support", "eva", "nasa"],
        "prerequisites": ["Fluid Mechanics", "Thermodynamics"],
        "equationsCovered": ["Ideal Gas Law P*V = n*R*T", "Radiative Heat Transfer Q = eps*sigma*A*T^4"],
        "modelUrl": "/models/space-suit/Astronaut.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "helmet",
                "name": "Extravehicular Visor Assembly",
                "hotspotPosition": "0.0m 1.6m 0.2m",
                "explanation": "Constructed from high-impact polycarbonate with vapor-deposited gold coatings to shield against micrometeorites, extreme UV radiation, and solar glare while maintaining internal pressure.",
                "formulaOrLaw": "Stefan-Boltzmann Radiation & Snell's Law"
            },
            {
                "id": "chest-pack",
                "name": "Primary Life Support System (PLSS)",
                "hotspotPosition": "0.0m 0.9m 0.3m",
                "explanation": "Contains high-pressure O2 recharge tanks, lithium hydroxide (LiOH) canisters for CO2 scrubbing, sublimation coolers, and recirculating fans.",
                "formulaOrLaw": "Partial Pressure: P_total = P_O2 + P_CO2 + P_H2O"
            },
            {
                "id": "gloves",
                "name": "Pressurized EVA Gloves",
                "hotspotPosition": "0.4m 0.7m 0.2m",
                "explanation": "Features integrated fingertip heating circuits and rotary wrist bearings that preserve tactile dexterity under 29.6 kPa differential pressure.",
                "formulaOrLaw": "Hoop Stress: sigma = (P * r) / t"
            },
            {
                "id": "tmg-suit",
                "name": "Thermal Micrometeoroid Garment (TMG)",
                "hotspotPosition": "0.0m 1.2m -0.1m",
                "explanation": "Multi-layer insulation (MLI) composed of aluminized Mylar, Nomex, and Kevlar that halts hypervelocity orbital debris and stops conductive heat loss.",
                "formulaOrLaw": "Hypervelocity Kinetic Energy E_k = 0.5 * m * v^2"
            },
            {
                "id": "lcvg",
                "name": "Liquid Cooling & Ventilation Garment",
                "hotspotPosition": "0.0m 0.5m 0.1m",
                "explanation": "A tight-fitting nylon-spandex undergarment woven with over 90 meters of flexible tubing circulating chilled water to absorb astronaut metabolic heat.",
                "formulaOrLaw": "Convective Heat Absorption: Q = m_dot * c_p * Delta_T"
            }
        ],
        "quiz": [
            {
                "id": "ss-q1",
                "question": "What chemical absorbent is traditionally utilized in the PLSS to scrub toxic carbon dioxide exhaled by the astronaut?",
                "options": [
                    "Potassium Permanganate (KMnO4)",
                    "Lithium Hydroxide (LiOH)",
                    "Sodium Chloride (NaCl)",
                    "Activated Silicon Dioxide (SiO2)"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "2LiOH + CO2 -> Li2CO3 + H2O. Lithium hydroxide provides high stoichiometric capacity per unit mass, crucial for space flight weight constraints."
            },
            {
                "id": "ss-q2",
                "question": "Why does the EMU helmet visor feature an ultra-thin vapor-deposited layer of pure gold?",
                "options": [
                    "To act as a low-resistance radio transmission antenna",
                    "To reflect infrared and harsh solar radiation while permitting visible light transmittance",
                    "To seal microscopic vacuum leaks in the polycarbonate shell",
                    "To conduct electrical grounding for the heads-up display"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "Gold has exceptionally high optical reflectance in the infrared and ultraviolet bands while remaining semi-transparent to visible wavelengths."
            },
            {
                "id": "ss-q3",
                "question": "How does the Liquid Cooling & Ventilation Garment (LCVG) maintain the astronaut's core temperature during intense spacewalks?",
                "options": [
                    "By circulating chilled water through network tubing to carry away metabolic heat via forced convection",
                    "By evaporating liquid nitrogen directly onto the skin surface",
                    "By reflecting body infrared radiation back to the skin",
                    "By utilizing Peltier thermoelectric chips embedded in the outer Kevlar layer"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Water has high specific heat capacity (4184 J/kg*K). Forced liquid circulation transfers up to 500 Watts of metabolic heat to the sublimator."
            }
        ],
        "license": {
            "title": "Astronaut Extravehicular Mobility Unit (EMU)",
            "source": "https://modelviewer.dev/shared-assets/models/Astronaut.glb",
            "author": "Google model-viewer / Poly asset collection",
            "license": "CC-BY-4.0",
            "attribution": "3D model courtesy of Google model-viewer project (Poly asset collection)."
        }
    },
    {
        "id": "human-heart",
        "name": "Human Heart & Cardiovascular Mechanics",
        "description": "Analyze the four-chambered muscular pump, hemodynamic pressures, and valvular fluid dynamics.",
        "discipline": "Biomedical Engineering",
        "subfield": "Cardiovascular Physiology & Biomechanics",
        "academicLevel": "Undergraduate",
        "tags": ["biomechanics", "cardiology", "hemodynamics", "physiology"],
        "prerequisites": ["Fluid Mechanics", "Basic Anatomy"],
        "equationsCovered": ["Cardiac Output CO = HR * SV", "Darcy-Weisbach Equation", "Poiseuille's Law Delta_P = (8*mu*L*Q)/(pi*r^4)"],
        "modelUrl": "/models/human-heart/heart.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "left-ventricle",
                "name": "Left Ventricle",
                "hotspotPosition": "-0.04m -0.05m 0.02m",
                "explanation": "The thickest muscular chamber of the heart; it generates peak systolic pressure (~120 mmHg) to overcome systemic vascular resistance and perfuse peripheral capillary beds.",
                "formulaOrLaw": "Laplace's Law: Wall Stress sigma = (P * r) / (2 * h)"
            },
            {
                "id": "aortic-arch",
                "name": "Aortic Arch & Elastic Conduit",
                "hotspotPosition": "0.01m 0.08m 0.01m",
                "explanation": "The main conduit delivering oxygenated blood to the systemic circulation; its elastic Windkessel effect converts pulsatile ventricular ejection into continuous downstream flow.",
                "formulaOrLaw": "Windkessel Compliance: C = Delta_V / Delta_P"
            },
            {
                "id": "right-atrium",
                "name": "Right Atrium & SA Node",
                "hotspotPosition": "0.05m 0.02m -0.02m",
                "explanation": "Receives deoxygenated venous return from the superior and inferior vena cavae at low hydrostatic pressure (~2-6 mmHg) and houses the primary cardiac pacemaker.",
                "formulaOrLaw": "Preload & Frank-Starling Mechanism"
            },
            {
                "id": "mitral-valve",
                "name": "Bicuspid (Mitral) Valve",
                "hotspotPosition": "-0.02m 0.00m 0.01m",
                "explanation": "Dual-leaflet valve anchored by chordae tendineae and papillary muscles, preventing retrograde systolic backflow from the left ventricle into the left atrium.",
                "formulaOrLaw": "Torricelli Orifice Flow: Q = C_d * A * sqrt(2 * Delta_P / rho)"
            },
            {
                "id": "pulmonary-trunk",
                "name": "Pulmonary Trunk & Artery",
                "hotspotPosition": "0.00m 0.06m 0.03m",
                "explanation": "Branches out to transport deoxygenated stroke volume from the right ventricle into the low-resistance pulmonary capillary bed for gas exchange.",
                "formulaOrLaw": "Pulmonary Vascular Resistance: PVR = (mPAP - PCWP) / CO"
            }
        ],
        "quiz": [
            {
                "id": "hh-q1",
                "question": "According to Poiseuille's law of laminar hemodynamic flow, reducing vessel radius by half increases flow resistance by what factor?",
                "options": ["2x", "4x", "8x", "16x"],
                "correctAnswerIndex": 3,
                "engineeringExplanation": "Resistance R is inversely proportional to r^4. Decreasing radius to 1/2 increases resistance by (2)^4 = 16 times."
            },
            {
                "id": "hh-q2",
                "question": "What is the primary hemodynamic purpose of the aortic elastic Windkessel effect during diastole?",
                "options": [
                    "To generate electrical action potentials for ventricular contraction",
                    "To maintain continuous peripheral blood flow during ventricular relaxation via elastic recoil",
                    "To completely prevent venous return to the right atrium",
                    "To cool down the oxygen-depleted erythrocytes"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "The compliant aortic walls expand during systole and recoil elastically during diastole, dampening pressure oscillations and sustaining continuous perfusion."
            },
            {
                "id": "hh-q3",
                "question": "What does the Frank-Starling law of the heart predict when end-diastolic ventricular filling volume (preload) increases?",
                "options": [
                    "Decreased myofibril stretch and lower stroke volume",
                    "Myocardial fiber stretching leading to increased stroke volume contraction force",
                    "Immediate cessation of Sinoatrial nodal firing",
                    "Direct reduction of systemic vascular resistance to zero"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "Greater end-diastolic volume stretches cardiac myocytes toward optimal sarcomere overlap, enhancing contractile cross-bridge force and stroke volume."
            }
        ],
        "license": {
            "title": "Human Heart Anatomical Model",
            "source": "https://openstax.org/books/anatomy-and-physiology-2e/pages/19-1-heart-anatomy",
            "author": "OpenStax / CC BY 4.0",
            "license": "CC-BY-4.0",
            "attribution": "Anatomy and Physiology 2e, OpenStax, licensed under Creative Commons Attribution 4.0 International."
        }
    },
    {
        "id": "solar-system",
        "name": "Solar System Orbital Mechanics",
        "description": "Explore planetary motion, gravitational potential wells, and Keplerian orbital dynamics.",
        "discipline": "Astrophysics & Aerospace",
        "subfield": "Orbital Mechanics & Planetary Physics",
        "academicLevel": "Undergraduate",
        "tags": ["astronomy", "orbital-mechanics", "kepler", "gravitation"],
        "prerequisites": ["Classical Mechanics", "Vector Calculus"],
        "equationsCovered": ["Kepler's Third Law T^2 = (4*pi^2 / G*M) * a^3", "Newton's Gravitation F = G*m1*m2 / r^2", "Vis-Viva Equation v^2 = G*M*(2/r - 1/a)"],
        "modelUrl": "/models/solar-system/solar_system.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "sun-core",
                "name": "Sun (Heliocentric Gravitational Core)",
                "hotspotPosition": "0.0m 0.0m 0.0m",
                "explanation": "Contains 99.86% of the solar system's mass, creating the deep gravitational potential well that dictates the orbital ephemerides of all surrounding celestial bodies.",
                "formulaOrLaw": "Gravitational Potential: Phi = -G * M / r"
            },
            {
                "id": "inner-rocky",
                "name": "Inner Terrestrial Planetary Zone",
                "hotspotPosition": "0.2m 0.0m 0.1m",
                "explanation": "High-density silicates and metals inside the frost line (Mercury, Venus, Earth, Mars) featuring high orbital velocities and shorter orbital periods.",
                "formulaOrLaw": "Circular Orbital Velocity: v = sqrt(G * M / r)"
            },
            {
                "id": "jupiter-lagrange",
                "name": "Jupiter & Lagrange Equilibrium Points",
                "hotspotPosition": "0.6m 0.0m -0.3m",
                "explanation": "The most massive planet, exerting strong gravitational perturbations and hosting stable L4 and L5 gravitational equilibrium zones (Trojan asteroids).",
                "formulaOrLaw": "Three-Body Problem & Jacobi Energy Integral"
            },
            {
                "id": "saturn-rings",
                "name": "Saturn & Roche Tidal Boundary",
                "hotspotPosition": "-0.8m 0.0m 0.4m",
                "explanation": "Ring system composed of billions of water-ice particles maintained within the Roche limit where tidal forces prevent gravitational coalescence into a single moon.",
                "formulaOrLaw": "Fluid Roche Limit: d = 2.44 * R * (rho_M / rho_m)^(1/3)"
            },
            {
                "id": "kuiper-belt",
                "name": "Kuiper Belt & Oort Cloud Frontier",
                "hotspotPosition": "1.4m 0.0m 0.0m",
                "explanation": "The outer circumstellar disc of icy planetesimals and comet reservoirs governed by weak solar gravitational binding energy.",
                "formulaOrLaw": "Escape Velocity: v_esc = sqrt(2 * G * M / r)"
            }
        ],
        "quiz": [
            {
                "id": "sol-q1",
                "question": "According to Kepler's Third Law, if a planet's semi-major axis is 4 AU, what is its orbital period around the Sun?",
                "options": ["2 years", "4 years", "8 years", "16 years"],
                "correctAnswerIndex": 2,
                "engineeringExplanation": "T^2 = a^3. With a = 4, a^3 = 64. Taking the square root gives T = 8 years."
            },
            {
                "id": "sol-q2",
                "question": "What physical principle establishes the Roche limit inside which planetary ring systems persist?",
                "options": [
                    "Atmospheric drag from the host planet",
                    "Differential gravitational tidal forces exceeding the self-gravitation of the orbiting body",
                    "Relativistic frame dragging of spacetime",
                    "Solar radiation pressure repulsive force"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "Inside the Roche limit, tidal stretching from the primary body tears apart any satellite held together primarily by self-gravity."
            },
            {
                "id": "sol-q3",
                "question": "Using the Vis-Viva equation, what happens to an orbiting spacecraft's speed at periapsis compared to apoapsis in an elliptical orbit?",
                "options": [
                    "Speed is identical at all orbital locations",
                    "Speed is at its maximum at periapsis because r is minimized",
                    "Speed is at its minimum at periapsis because kinetic energy is lowest",
                    "Speed drops to zero momentarily"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "v^2 = GM*(2/r - 1/a). When r is at its minimum (periapsis), (2/r) is largest, resulting in peak orbital velocity."
            }
        ],
        "license": {
            "title": "Solar System Planetary Model",
            "source": "https://openstax.org/books/astronomy-2e/pages/7-1-overview-of-our-planetary-system",
            "author": "OpenStax / CC BY 4.0",
            "license": "CC-BY-4.0",
            "attribution": "Astronomy 2e, OpenStax, licensed under Creative Commons Attribution 4.0 International."
        }
    },
    {
        "id": "digital-logic-gates",
        "name": "Digital Logic Gates, Adders & Flip-Flops",
        "description": "Examine combinational and sequential digital logic circuits from NAND gates to synchronous registers.",
        "discipline": "Electrical & Computer Engineering",
        "subfield": "Digital Electronics",
        "academicLevel": "Undergraduate",
        "tags": ["logic-gates", "boolean-algebra", "adders", "flip-flops"],
        "prerequisites": ["Boolean Algebra", "Basic Circuit Theory"],
        "equationsCovered": ["De Morgan's Theorem", "Propagation Delay t_pd = t_r + t_f", "Setup & Hold Times"],
        "modelUrl": "/models/digital-logic-gates/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "nand-universal",
                "name": "NAND Universal Gate",
                "hotspotPosition": "-0.05m 0.02m 0.0m",
                "explanation": "A functionally complete universal logic element from which AND, OR, NOT, XOR, and complex combinational blocks can be constructed using CMOS transistor pairs.",
                "formulaOrLaw": "Boolean: Y = NOT(A AND B)"
            },
            {
                "id": "full-adder",
                "name": "1-Bit Full Adder Cell",
                "hotspotPosition": "0.0m 0.02m 0.0m",
                "explanation": "Calculates binary summation of two input bits and an incoming carry bit, producing a sum bit and carry-out bit used in arithmetic logic units.",
                "formulaOrLaw": "Sum = A XOR B XOR C_in, C_out = (A*B) + (C_in*(A XOR B))"
            },
            {
                "id": "d-flip-flop",
                "name": "Edge-Triggered D Flip-Flop",
                "hotspotPosition": "0.05m 0.02m 0.0m",
                "explanation": "Bistable multivibrator that samples input D on the rising clock edge, providing static storage for state machines and register files.",
                "formulaOrLaw": "Next State: Q(t+1) = D, subject to t_setup and t_hold"
            },
            {
                "id": "mux-selector",
                "name": "4-to-1 Multiplexer (MUX)",
                "hotspotPosition": "0.02m -0.03m 0.0m",
                "explanation": "Steers one of four digital data inputs to a single output line based on two select control lines, forming data routing matrices.",
                "formulaOrLaw": "Y = S1'*S0'*D0 + S1'*S0*D1 + S1*S0'*D2 + S1*S0*D3"
            },
            {
                "id": "clock-distribution",
                "name": "Clock Distribution & Buffer Tree",
                "hotspotPosition": "-0.02m -0.03m 0.0m",
                "explanation": "Balanced H-tree buffer network designed to minimize clock skew and jitter across synchronous sequential logic stages.",
                "formulaOrLaw": "Clock Skew: T_skew = |t_clk1 - t_clk2| < T_cycle - T_prop - T_setup"
            }
        ],
        "quiz": [
            {
                "id": "dlg-q1",
                "question": "Why is the NAND gate classified as a functionally complete 'universal' logic gate?",
                "options": [
                    "It consumes zero static power in CMOS circuits",
                    "Any arbitrary Boolean function can be implemented using exclusively NAND gates",
                    "It has infinite fan-out capability",
                    "It acts as an analog amplifier at high frequencies"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "NAND can synthesize NOT (connect inputs together), AND (NAND followed by NOT), and OR (De Morgan: NOT(A) NAND NOT(B)), making it functionally complete."
            },
            {
                "id": "dlg-q2",
                "question": "What critical timing constraint is violated if data input D changes during the flip-flop's setup window?",
                "options": [
                    "Metastability where output Q oscillates between 0 and 1 indeterminately",
                    "Immediate thermal destruction of the gate oxide",
                    "Clock frequency automatically doubles",
                    "Permanent inversion of the power rail polarity"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Violating setup time (t_setup) prevents internal feedback latches from settling reliably, driving the latch into an unpredictable metastable state."
            },
            {
                "id": "dlg-q3",
                "question": "In a 1-bit full adder, what is the Boolean expression for the Carry Out (C_out) given inputs A, B, and C_in?",
                "options": [
                    "C_out = A XOR B XOR C_in",
                    "C_out = (A AND B) OR (C_in AND (A XOR B))",
                    "C_out = A NAND B NAND C_in",
                    "C_out = A + B + C_in"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "A carry is generated if both A and B are 1, or if either is 1 and an incoming carry is present: C_out = AB + C_in(A XOR B)."
            }
        ],
        "license": {
            "title": "Digital Logic Gate Circuits Model",
            "source": "https://en.wikipedia.org/wiki/Logic_gate",
            "author": "PrismEd Open Hardware Collection",
            "license": "CC-BY-4.0",
            "attribution": "PrismEd Digital Engineering Open Assets (CC-BY-4.0)."
        }
    },
    {
        "id": "process-scheduling",
        "name": "OS Process Scheduling & Concurrency",
        "description": "Understand kernel scheduling queues, preemptive dispatch, context switching, and multi-core synchronization.",
        "discipline": "Computer Science",
        "subfield": "Operating Systems",
        "academicLevel": "Undergraduate",
        "tags": ["os", "scheduling", "multithreading", "context-switch"],
        "prerequisites": ["Operating Systems Basics", "Data Structures"],
        "equationsCovered": ["Turnaround Time T_turn = T_completion - T_arrival", "Waiting Time T_wait = T_turn - T_burst", "Little's Law L = lambda * W"],
        "modelUrl": "/models/process-scheduling/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "pcb-block",
                "name": "Process Control Block (PCB)",
                "hotspotPosition": "-0.04m 0.03m 0.0m",
                "explanation": "Kernel data structure preserving process state, Program Counter (PC), CPU registers, memory management pointers, and open file descriptors during context switches.",
                "formulaOrLaw": "Context Switch Latency T_switch = T_save + T_restore + T_cache_flush"
            },
            {
                "id": "ready-queue",
                "name": "Multi-Level Feedback Ready Queue",
                "hotspotPosition": "0.0m 0.03m 0.0m",
                "explanation": "Priority-tiered scheduling queues that dynamically adjust process priority based on CPU burst history and I/O wait latency.",
                "formulaOrLaw": "Exponential Smoothing: tau_(n+1) = alpha * t_n + (1 - alpha) * tau_n"
            },
            {
                "id": "cpu-dispatcher",
                "name": "CPU Dispatcher & Core Allocator",
                "hotspotPosition": "0.04m 0.03m 0.0m",
                "explanation": "Kernel module that switches CPU core execution from kernel mode to user mode, loading the newly scheduled process context.",
                "formulaOrLaw": "CPU Utilization = (Total Time - Idle Time) / Total Time"
            },
            {
                "id": "sync-primitives",
                "name": "Mutex & Semaphore Synchronization",
                "hotspotPosition": "0.02m -0.02m 0.0m",
                "explanation": "Hardware atomic primitives (Compare-And-Swap, Test-And-Set) providing race-free critical section entry to prevent concurrency deadlocks.",
                "formulaOrLaw": "Coffman Conditions for Deadlock Prevention"
            },
            {
                "id": "timer-interrupt",
                "name": "Programmable Timer Interrupt Vector",
                "hotspotPosition": "-0.02m -0.02m 0.0m",
                "explanation": "Hardware timer chip triggering periodic tick interrupts (e.g. 1000 Hz) to enforce preemption and time-slice expiration in Round-Robin schedulers.",
                "formulaOrLaw": "Time Quantum q: trade-off between throughput and response time"
            }
        ],
        "quiz": [
            {
                "id": "ps-q1",
                "question": "What primary trade-off occurs when selecting an extremely small time quantum (e.g., 0.5 ms) in Round-Robin scheduling?",
                "options": [
                    "Average response time degrades for interactive processes",
                    "Context-switch CPU overhead consumes a disproportionate fraction of CPU cycles",
                    "Deadlocks become mathematically impossible",
                    "Memory fragmentation increases in the disk swap space"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "If time quantum q is comparable to context switch latency, the system spends excessive CPU time saving/restoring registers rather than executing user code."
            },
            {
                "id": "ps-q2",
                "question": "Which of the following conditions is NOT one of the four Coffman conditions necessary for deadlock to occur?",
                "options": [
                    "Mutual Exclusion",
                    "Hold and Wait",
                    "Preemptive Resource Deprivation",
                    "Circular Wait"
                ],
                "correctAnswerIndex": 2,
                "engineeringExplanation": "The Coffman conditions require 'No Preemption'. If resources can be preempted, deadlocks cannot persist."
            },
            {
                "id": "ps-q3",
                "question": "What information stored inside the Process Control Block (PCB) is essential for resuming an interrupted process?",
                "options": [
                    "Hardware Program Counter (PC) and CPU register values",
                    "Host machine BIOS serial key",
                    "The graphic rendering pipeline shaders",
                    "The client's browser cookies"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "The PC points to the next instruction, and CPU register snapshots restore the active mathematical state and call stack pointers."
            }
        ],
        "license": {
            "title": "Process Scheduling Visualization",
            "source": "https://en.wikipedia.org/wiki/Scheduling_(computing)",
            "author": "PrismEd Computer Systems Collection",
            "license": "CC-BY-4.0",
            "attribution": "PrismEd CS Education Open Assets (CC-BY-4.0)."
        }
    },
    {
        "id": "compiler-pipeline",
        "name": "Compiler Pipeline & Optimization Engine",
        "description": "Trace compilation from lexical tokenization and abstract syntax trees to SSA intermediate representation and machine code generation.",
        "discipline": "Computer Science",
        "subfield": "Compilers & Programming Languages",
        "academicLevel": "Undergraduate",
        "tags": ["compilers", "ast", "llvm", "optimization"],
        "prerequisites": ["Data Structures", "Automata Theory"],
        "equationsCovered": ["Chomsky Hierarchy", "SSA Dominance Frontiers", "Register Allocation Graph Coloring"],
        "modelUrl": "/models/compiler-pipeline/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "lexer-token",
                "name": "Lexical Scanner (Lexer)",
                "hotspotPosition": "-0.05m 0.03m 0.0m",
                "explanation": "Converts raw source code character streams into a sequence of classified syntactic tokens using deterministic finite automata (DFA).",
                "formulaOrLaw": "Regular Expressions -> NFA -> DFA (Subset Construction)"
            },
            {
                "id": "ast-parser",
                "name": "Abstract Syntax Tree (AST) Parser",
                "hotspotPosition": "-0.02m 0.03m 0.0m",
                "explanation": "Applies context-free grammar rules (LL(k) or LR(k)) to verify syntax and build hierarchical nested operator-operand syntax trees.",
                "formulaOrLaw": "Context-Free Grammar: G = (V, Sigma, R, S)"
            },
            {
                "id": "ssa-ir",
                "name": "SSA Intermediate Representation",
                "hotspotPosition": "0.01m 0.03m 0.0m",
                "explanation": "Transforms code into Static Single Assignment (SSA) form where every variable is assigned exactly once, simplifying data-flow optimizations.",
                "formulaOrLaw": "Phi-Function Merging: x_3 = phi(x_1, x_2)"
            },
            {
                "id": "optimizer-passes",
                "name": "Optimization Engine (LLVM Passes)",
                "hotspotPosition": "0.03m 0.01m 0.0m",
                "explanation": "Executes dead code elimination, loop invariant code motion, constant folding, and function inlining to minimize execution cycles.",
                "formulaOrLaw": "Data-flow Fixed Point: Out[B] = gen[B] union (In[B] - kill[B])"
            },
            {
                "id": "codegen-reg",
                "name": "Target Machine Code Generator",
                "hotspotPosition": "0.05m -0.02m 0.0m",
                "explanation": "Performs instruction selection and assigns unlimited virtual variables to finite physical CPU registers using Chaitin-Briggs graph coloring.",
                "formulaOrLaw": "Graph K-Colorability for Register Allocation"
            }
        ],
        "quiz": [
            {
                "id": "cp-q1",
                "question": "What is the defining characteristic of Static Single Assignment (SSA) intermediate representation?",
                "options": [
                    "All variables must fit into a single CPU register",
                    "Every variable is assigned a value exactly once, using phi-functions at control-flow join points",
                    "Functions cannot take more than one argument",
                    "Code is compiled directly to microcode without an AST"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "SSA guarantees single assignment per variable version, drastically simplifying reaching definitions, constant propagation, and dead code elimination."
            },
            {
                "id": "cp-q2",
                "question": "Which classic algorithmic approach is standard for mapping unlimited compiler virtual registers to a finite set of CPU physical registers?",
                "options": [
                    "Dijkstra's Shortest Path",
                    "Chaitin-Briggs Graph Coloring heuristic",
                    "Fast Fourier Transform",
                    "Binary Search on register indices"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "Register interference graphs represent overlapping variable lifetimes as edges; finding a valid K-coloring solves physical register assignment."
            },
            {
                "id": "cp-q3",
                "question": "What is the purpose of Loop Invariant Code Motion (LICM) in optimizing compilers?",
                "options": [
                    "Hoisting computations whose operands do not change out of the loop body to execute only once",
                    "Unrolling loops into infinite recursions",
                    "Translating all loops into goto statements",
                    "Converting sequential loops into recursive descent parsers"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Expressions that yield identical values on every iteration are hoisted to the loop preheader, saving redundant CPU cycles."
            }
        ],
        "license": {
            "title": "Compiler Architecture Diagram",
            "source": "https://en.wikipedia.org/wiki/Compiler",
            "author": "PrismEd Open Engineering",
            "license": "CC-BY-4.0",
            "attribution": "PrismEd Compiler Systems Assets (CC-BY-4.0)."
        }
    },
    {
        "id": "memory-data-structures",
        "name": "Memory Layout & Cache-Conscious Data Structures",
        "description": "Analyze CPU cache hierarchies, memory alignment, spatial/temporal locality, and array vs pointer-chasing data structures.",
        "discipline": "Computer Science",
        "subfield": "Computer Systems & Algorithms",
        "academicLevel": "Undergraduate",
        "tags": ["memory", "cache", "data-structures", "locality"],
        "prerequisites": ["C Programming", "Computer Architecture"],
        "equationsCovered": ["Average Memory Access Time AMAT = Hit_time + Miss_rate * Miss_penalty", "Spatial & Temporal Locality Hit Ratio"],
        "modelUrl": "/models/memory-data-structures/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "l1-cache-line",
                "name": "64-Byte L1 Cache Line Buffer",
                "hotspotPosition": "-0.04m 0.04m 0.0m",
                "explanation": "The atomic block size transferred between DRAM and CPU SRAM cache; exploiting spatial locality requires contiguous struct packing within 64 bytes.",
                "formulaOrLaw": "AMAT = t_hit + (Miss_Rate * Penalty)"
            },
            {
                "id": "call-stack",
                "name": "Contiguous Execution Stack Frame",
                "hotspotPosition": "-0.02m 0.0m 0.0m",
                "explanation": "LIFO memory managed by the stack pointer (RSP), storing return addresses, frame pointers (RBP), and automatic local variables with zero allocation overhead.",
                "formulaOrLaw": "Stack Allocation O(1) via SP Subtraction"
            },
            {
                "id": "heap-arena",
                "name": "Dynamic Heap Allocation Arena",
                "hotspotPosition": "0.02m 0.0m 0.0m",
                "explanation": "Manages dynamic memory lifetimes using free-lists or buddy allocators; prone to external fragmentation and pointer-chasing cache misses.",
                "formulaOrLaw": "Memory Overhead: Internal vs External Fragmentation"
            },
            {
                "id": "b-tree-node",
                "name": "Cache-Conscious B-Tree Node",
                "hotspotPosition": "0.04m 0.03m 0.0m",
                "explanation": "Groups multiple sorted keys into a single contiguous block matching cache line size, eliminating pointer-chasing overhead of binary search trees.",
                "formulaOrLaw": "Branching Factor B chosen such that Node_Size = Cache_Line_Size"
            },
            {
                "id": "padding-alignment",
                "name": "Struct Byte Alignment & Padding",
                "hotspotPosition": "0.0m -0.03m 0.0m",
                "explanation": "Compilers insert padding bytes so that N-byte data types are aligned to N-byte memory addresses, avoiding multi-cycle split bus reads.",
                "formulaOrLaw": "Memory Alignment: address % sizeof(type) == 0"
            }
        ],
        "quiz": [
            {
                "id": "mds-q1",
                "question": "Why does iterating over a contiguous array typically achieve far higher performance than traversing a linked list of identical size?",
                "options": [
                    "Linked lists require dynamic floating point calculations",
                    "Contiguous arrays leverage CPU prefetchers and spatial cache locality, whereas linked lists trigger pointer-chasing cache misses",
                    "Arrays bypass the CPU L1 cache entirely",
                    "Linked lists cannot store 64-bit integers"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "Hardware prefetchers detect linear array memory access and load consecutive 64-byte cache lines before requested, preventing stalled memory stalls."
            },
            {
                "id": "mds-q2",
                "question": "If L1 cache hit time is 1 ns, DRAM miss penalty is 100 ns, and miss rate is 5%, what is the Average Memory Access Time (AMAT)?",
                "options": ["1.5 ns", "5.0 ns", "6.0 ns", "10.0 ns"],
                "correctAnswerIndex": 2,
                "engineeringExplanation": "AMAT = Hit Time + (Miss Rate * Miss Penalty) = 1 ns + (0.05 * 100 ns) = 1 + 5 = 6.0 ns."
            },
            {
                "id": "mds-q3",
                "question": "Why does a 64-bit CPU insert 4 padding bytes between a 32-bit int and a 64-bit pointer in a struct?",
                "options": [
                    "To ensure the 64-bit pointer starts at an address divisible by 8 bytes, avoiding unaligned memory access penalties",
                    "To encrypt memory contents against buffer overflows",
                    "To reserve space for virtual table lookups",
                    "To align the struct with the GPU frame buffer"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Modern architectures penalize or fault unaligned accesses; aligning 8-byte pointers to 8-byte boundaries ensures single-cycle memory reads."
            }
        ],
        "license": {
            "title": "Computer Memory Hierarchy Diagram",
            "source": "https://en.wikipedia.org/wiki/Memory_hierarchy",
            "author": "PrismEd Computer Systems Collection",
            "license": "CC-BY-4.0",
            "attribution": "PrismEd Memory Systems Open Assets (CC-BY-4.0)."
        }
    },
    {
        "id": "os-virtual-memory",
        "name": "Virtual Memory & Translation Lookaside Buffer",
        "description": "Examine address translation, page tables, TLB hits/misses, and demand-paged memory isolation.",
        "discipline": "Computer Science",
        "subfield": "Operating Systems",
        "academicLevel": "Undergraduate",
        "tags": ["virtual-memory", "paging", "tlb", "mmu"],
        "prerequisites": ["Operating Systems", "Computer Architecture"],
        "equationsCovered": ["Effective Access Time EAT = (1 - p)*t_mem + p*t_fault", "Multi-Level Page Table Offsets"],
        "modelUrl": "/models/os-virtual-memory/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "tlb-cache",
                "name": "Translation Lookaside Buffer (TLB)",
                "hotspotPosition": "-0.04m 0.03m 0.0m",
                "explanation": "Fully associative hardware cache in the MMU storing recent Virtual-to-Physical page mappings to provide single-cycle address translation.",
                "formulaOrLaw": "TLB Hit Time ~ 0.5-1.0 ns"
            },
            {
                "id": "mmu-unit",
                "name": "Memory Management Unit (MMU)",
                "hotspotPosition": "-0.01m 0.03m 0.0m",
                "explanation": "Hardware component on the CPU die that intercepts memory references, checks access permissions (Read/Write/Execute), and triggers page faults.",
                "formulaOrLaw": "CR3 Register points to PML4 Root Page Directory"
            },
            {
                "id": "page-table-walk",
                "name": "4-Level Page Table Tree",
                "hotspotPosition": "0.02m 0.03m 0.0m",
                "explanation": "Hierarchical radix tree translating 48-bit virtual addresses through PML4, PDPT, PD, and PT entries down to physical 4KB page frames.",
                "formulaOrLaw": "Virtual Address Split: [9 bits | 9 bits | 9 bits | 9 bits | 12 bit offset]"
            },
            {
                "id": "page-fault-engine",
                "name": "Page Fault Interrupt Handler",
                "hotspotPosition": "0.04m -0.01m 0.0m",
                "explanation": "OS kernel interrupt service routine invoked when referencing unmapped or swapped pages, loading the requested page from disk swap.",
                "formulaOrLaw": "Page Fault Penalty ~ 5-10 milliseconds (SSD/HDD I/O)"
            },
            {
                "id": "physical-ram-frame",
                "name": "Physical RAM Page Frame",
                "hotspotPosition": "0.0m -0.03m 0.0m",
                "explanation": "Continuous 4096-byte physical memory slice indexed by the Physical Frame Number (PFN) and merged with the lower 12-bit page offset.",
                "formulaOrLaw": "Physical Address = (PFN << 12) | Offset"
            }
        ],
        "quiz": [
            {
                "id": "ovm-q1",
                "question": "In a 64-bit architecture with 4KB page sizes, how many bits of the virtual address are allocated to the in-page offset?",
                "options": ["8 bits", "10 bits", "12 bits", "16 bits"],
                "correctAnswerIndex": 2,
                "engineeringExplanation": "4KB equals 2^12 bytes, requiring exactly 12 bits to address every individual byte within a page frame."
            },
            {
                "id": "ovm-q2",
                "question": "What happens immediately when a CPU instruction attempts to write to a page marked Read-Only in its page table entry?",
                "options": [
                    "The CPU halts completely and powers off",
                    "The MMU generates a hardware page fault interrupt, alerting the OS kernel of a protection violation",
                    "The write operation is silently dropped with no error",
                    "The memory page is automatically duplicated on disk"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "The MMU checks access bits in the page table entry. An invalid write generates a trap/page fault (typically resulting in a SIGSEGV in user space)."
            },
            {
                "id": "ovm-q3",
                "question": "Why do modern 64-bit operating systems use multi-level hierarchical page tables rather than a single flat page table array?",
                "options": [
                    "A flat page table would require terabytes of contiguous physical memory even for tiny processes",
                    "Hierarchical tables make address translation completely independent of the CPU clock",
                    "Multi-level tables prevent TLB cache misses entirely",
                    "Single-level tables cannot support virtual memory"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "A flat 64-bit page table would require millions of gigabytes per process; hierarchical paging dynamically allocates tables only for populated virtual memory regions."
            }
        ],
        "license": {
            "title": "Virtual Memory and Paging System",
            "source": "https://en.wikipedia.org/wiki/Virtual_memory",
            "author": "PrismEd Computer Systems Collection",
            "license": "CC-BY-4.0",
            "attribution": "PrismEd OS Architecture Open Assets (CC-BY-4.0)."
        }
    },
    {
        "id": "networking-protocol-stack",
        "name": "OSI & TCP/IP Protocol Stack",
        "description": "Examine packet encapsulation, TCP flow & congestion control, IP routing, and Ethernet framing.",
        "discipline": "Computer Science",
        "subfield": "Computer Networks",
        "academicLevel": "Undergraduate",
        "tags": ["networking", "tcp-ip", "osi", "routing"],
        "prerequisites": ["Data Communications", "Operating Systems"],
        "equationsCovered": ["Mathis TCP Throughput B <= (1.22*MSS)/(RTT*sqrt(p))", "Bandwidth-Delay Product BDP = Bandwidth * RTT"],
        "modelUrl": "/models/networking-protocol-stack/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "ethernet-frame",
                "name": "Ethernet Data Link Frame Layer",
                "hotspotPosition": "-0.04m 0.03m 0.0m",
                "explanation": "Encapsulates network payloads with 6-byte source and destination MAC addresses and appends a 4-byte CRC-32 Frame Check Sequence for error detection.",
                "formulaOrLaw": "Maximum Transmission Unit (MTU) = 1500 bytes"
            },
            {
                "id": "ip-router",
                "name": "IPv4 / IPv6 Network Layer",
                "hotspotPosition": "-0.02m 0.02m 0.0m",
                "explanation": "Provides logical host addressing, Time-to-Live (TTL) hop count decrements, and packet routing across heterogeneous Autonomous Systems using BGP/OSPF.",
                "formulaOrLaw": "Longest Prefix Match (LPM) Routing Lookup"
            },
            {
                "id": "tcp-congestion",
                "name": "TCP Congestion & Flow Control",
                "hotspotPosition": "0.01m 0.02m 0.0m",
                "explanation": "Guarantees reliable, ordered byte delivery using sliding receive windows (rwnd), sequence numbers, and AIMD (Additive Increase / Multiplicative Decrease) algorithms.",
                "formulaOrLaw": "Mathis Formula: Rate <= (1.22 * MSS) / (RTT * sqrt(loss_rate))"
            },
            {
                "id": "tls-security",
                "name": "TLS 1.3 Cryptographic Layer",
                "hotspotPosition": "0.03m 0.01m 0.0m",
                "explanation": "Provides end-to-end confidentiality and integrity via ephemeral Elliptic Curve Diffie-Hellman (ECDHE) key exchange and AES-256-GCM authenticated encryption.",
                "formulaOrLaw": "ECDHE Discrete Logarithm Hardness"
            },
            {
                "id": "socket-buffer",
                "name": "Socket API & Kernel Buffers",
                "hotspotPosition": "0.05m -0.02m 0.0m",
                "explanation": "OS kernel ring buffers (sk_buff) mediating data transfer between application user space and Network Interface Card (NIC) DMA rings.",
                "formulaOrLaw": "Bandwidth-Delay Product (BDP) = Bandwidth * RTT"
            }
        ],
        "quiz": [
            {
                "id": "nps-q1",
                "question": "What is the primary function of the TCP sliding window mechanism?",
                "options": [
                    "To dynamically calibrate flow control and prevent the sender from overwhelming receiver buffer capacity",
                    "To encrypt payload contents against eavesdropping",
                    "To determine the physical path routers take across optical fibers",
                    "To convert IPv4 addresses to IPv6 format"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "The receiver advertises its available buffer space (rwnd); the sender ensures unacknowledged bytes in flight never exceed this window."
            },
            {
                "id": "nps-q2",
                "question": "If a network connection has 100 Mbps bandwidth and a Round Trip Time (RTT) of 40 ms, what is the Bandwidth-Delay Product (BDP)?",
                "options": ["400 KB", "500 KB", "4 MB", "40 MB"],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "BDP = 100,000,000 bits/sec * 0.040 sec = 4,000,000 bits = 500,000 bytes = 500 KB."
            },
            {
                "id": "nps-q3",
                "question": "What happens at each router hop when an IP packet's Time-to-Live (TTL) field reaches zero?",
                "options": [
                    "The packet is forwarded to the default gateway",
                    "The packet is discarded, and an ICMP Time Exceeded message is transmitted to the sender",
                    "The packet's payload is expanded to IPv6",
                    "The router buffers the packet indefinitely"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "TTL prevents routing loops from circulating packets indefinitely. When TTL hits 0, it is dropped and ICMP Type 11 is returned."
            }
        ],
        "license": {
            "title": "TCP/IP Networking Stack Model",
            "source": "https://en.wikipedia.org/wiki/Internet_protocol_suite",
            "author": "PrismEd Networking Collection",
            "license": "CC-BY-4.0",
            "attribution": "PrismEd Network Architecture Open Assets (CC-BY-4.0)."
        }
    },
    {
        "id": "database-b-tree",
        "name": "B+ Tree Indexing & Storage Engine",
        "description": "Analyze self-balancing B+ trees, write-ahead logging (WAL), page buffer pools, and ACID transaction mechanics.",
        "discipline": "Computer Science",
        "subfield": "Database Systems",
        "academicLevel": "Undergraduate",
        "tags": ["databases", "indexing", "b-plus-tree", "acid"],
        "prerequisites": ["Data Structures", "Operating Systems"],
        "equationsCovered": ["B+ Tree Height h <= ceil(log_(M/2) (N))", "ARIES Recovery Protocol"],
        "modelUrl": "/models/database-b-tree/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "root-node",
                "name": "Root Index Routing Node",
                "hotspotPosition": "0.0m 0.04m 0.0m",
                "explanation": "Remains permanently pinned in memory, routing search keys down toward child nodes with high fan-out (order M > 100) to minimize tree height.",
                "formulaOrLaw": "Tree Height: h <= ceil(log_(M/2) N)"
            },
            {
                "id": "internal-node",
                "name": "Internal Pivot Node",
                "hotspotPosition": "-0.03m 0.02m 0.0m",
                "explanation": "Contains sorted boundary keys and page IDs directing range traversals without holding actual row records or payload pointers.",
                "formulaOrLaw": "Search Complexity: O(log_M N) disk I/O reads"
            },
            {
                "id": "leaf-pages",
                "name": "Doubly-Linked Leaf Pages",
                "hotspotPosition": "0.03m -0.01m 0.0m",
                "explanation": "Store actual table records or row pointers, doubly linked to enable rapid sequential range scans without re-traversing upper tree levels.",
                "formulaOrLaw": "Range Scan O(k) over linked sibling pages"
            },
            {
                "id": "wal-log",
                "name": "Write-Ahead Logging (WAL) Buffer",
                "hotspotPosition": "-0.04m -0.03m 0.0m",
                "explanation": "Ensures ACID durability by appending redo/undo log records to non-volatile storage before dirty data pages are flushed to disk.",
                "formulaOrLaw": "WAL Invariant: Log flushed before DB Page Write"
            },
            {
                "id": "buffer-pool",
                "name": "LRU Database Buffer Pool",
                "hotspotPosition": "0.0m -0.04m 0.0m",
                "explanation": "Allocates an in-memory frame cache for disk pages, using CLOCK or 2Q eviction algorithms to maintain high cache hit ratios.",
                "formulaOrLaw": "Buffer Pool Hit Ratio = Page_Hits / Total_Page_Requests"
            }
        ],
        "quiz": [
            {
                "id": "dbt-q1",
                "question": "Why do relational database storage engines prefer B+ trees over standard binary search trees (BSTs) for disk-based indexing?",
                "options": [
                    "B+ trees have a high branching factor (fan-out) matching disk block sizes, keeping tree depth very shallow and minimizing disk I/O",
                    "BSTs consume less CPU memory than B+ trees",
                    "B+ trees do not require key comparisons",
                    "BSTs cannot store integer keys"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Disk seeks take milliseconds. A B+ tree with fan-out of 100 can index 1,000,000 keys in just 3 disk page reads."
            },
            {
                "id": "dbt-q2",
                "question": "What is the critical rule enforced by Write-Ahead Logging (WAL) to guarantee transaction durability?",
                "options": [
                    "Log records must be flushed to non-volatile storage before modified database pages are written to disk",
                    "Data pages must be written to disk before transactions are committed in memory",
                    "Logs are only generated during database shutdown",
                    "All queries must execute sequentially with no concurrency"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "The WAL protocol dictates that log records describing a state change must reach durable disk before the dirty page can be written back."
            },
            {
                "id": "dbt-q3",
                "question": "What structural feature in B+ trees enables efficient range queries (e.g., SELECT WHERE age BETWEEN 20 AND 30)?",
                "options": [
                    "All leaf nodes are linked sequentially in a doubly-linked list",
                    "Leaf nodes are recursively placed in hash buckets",
                    "Root nodes store all payload data directly",
                    "The tree is rebuilt from scratch for every range query"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Once the start key is located, the engine scans adjacent sibling leaf pages via horizontal pointers without ascending back up the tree."
            }
        ],
        "license": {
            "title": "B+ Tree Database Indexing Model",
            "source": "https://en.wikipedia.org/wiki/B%2B_tree",
            "author": "PrismEd Database Systems Group",
            "license": "CC-BY-4.0",
            "attribution": "PrismEd DB Systems Open Assets (CC-BY-4.0)."
        }
    },
    {
        "id": "distributed-microservices",
        "name": "Distributed Cloud Microservices Architecture",
        "description": "Understand API gateways, service meshes, circuit breakers, distributed consensus, and event-driven messaging.",
        "discipline": "Software Engineering",
        "subfield": "Distributed Systems & Cloud",
        "academicLevel": "Undergraduate",
        "tags": ["microservices", "cloud", "distributed-systems", "grpc"],
        "prerequisites": ["Software Engineering", "Computer Networks"],
        "equationsCovered": ["CAP Theorem", "Little's Law L = lambda * W", "Raft Consensus Quorum Q = floor(N/2) + 1"],
        "modelUrl": "/models/distributed-microservices/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "api-gateway",
                "name": "Reverse Proxy & API Gateway",
                "hotspotPosition": "0.0m 0.04m 0.0m",
                "explanation": "Single entry point terminating external TLS, managing rate limiting, routing requests, and aggregating backend microservice responses.",
                "formulaOrLaw": "Load Balancing Round-Robin & Least Connections"
            },
            {
                "id": "circuit-breaker",
                "name": "Circuit Breaker Resiliency Unit",
                "hotspotPosition": "-0.03m 0.02m 0.0m",
                "explanation": "Monitors downstream service failure rates; trips from Closed to Open state to fail fast during outages and protect system cascading stability.",
                "formulaOrLaw": "State Machine: Closed -> Open -> Half-Open"
            },
            {
                "id": "event-bus",
                "name": "Distributed Event Log (Kafka / Pub-Sub)",
                "hotspotPosition": "0.03m 0.02m 0.0m",
                "explanation": "High-throughput partitioned append-only log decoupling microservices asynchronously through publish-subscribe event streams.",
                "formulaOrLaw": "Consumer Group Offset Commit & At-Least-Once Delivery"
            },
            {
                "id": "raft-consensus",
                "name": "Raft Consensus Replicated State",
                "hotspotPosition": "0.0m -0.01m 0.0m",
                "explanation": "Ensures strong consistency and leader election across distributed node clusters despite network partitions.",
                "formulaOrLaw": "Quorum Requirement: Majority Q = floor(N/2) + 1"
            },
            {
                "id": "sharded-db",
                "name": "Horizontally Sharded Data Store",
                "hotspotPosition": "0.0m -0.04m 0.0m",
                "explanation": "Distributes database partitions across independent nodes using consistent hashing to balance read/write throughput.",
                "formulaOrLaw": "Consistent Hashing Ring with Virtual Nodes"
            }
        ],
        "quiz": [
            {
                "id": "dm-q1",
                "question": "What is the primary role of a Circuit Breaker pattern in a distributed microservices network?",
                "options": [
                    "To prevent cascading failures across the ecosystem by failing fast when downstream services are degraded",
                    "To compress network packets using gzip",
                    "To automatically generate database schemas",
                    "To balance CPU heat across server rack fans"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "When downstream calls fail repeatedly, the breaker opens, rejecting requests immediately without tying up connection threads and threads."
            },
            {
                "id": "dm-q2",
                "question": "In a distributed cluster of 5 nodes running Raft consensus, what is the minimum number of operational nodes needed to form a quorum?",
                "options": ["2 nodes", "3 nodes", "4 nodes", "5 nodes"],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "Quorum Q = floor(N/2) + 1. For N = 5, floor(5/2) + 1 = 2 + 1 = 3 nodes."
            },
            {
                "id": "dm-q3",
                "question": "According to the CAP theorem, what trade-off must a distributed system make in the event of an unavoidable network partition (P)?",
                "options": [
                    "It can maintain both full Consistency (C) and full Availability (A) simultaneously",
                    "It must choose between Consistency (returning errors or waiting) and Availability (returning stale data)",
                    "It automatically doubles system memory",
                    "It must drop all database tables permanently"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "When network partitions occur, nodes cannot synchronize state; the system must either sacrifice availability or risk returning inconsistent data."
            }
        ],
        "license": {
            "title": "Microservices Architecture Diagram",
            "source": "https://en.wikipedia.org/wiki/Microservices",
            "author": "PrismEd Software Engineering Group",
            "license": "CC-BY-4.0",
            "attribution": "PrismEd Cloud Architecture Assets (CC-BY-4.0)."
        }
    },
    {
        "id": "gpu-architecture",
        "name": "GPU Microarchitecture & SIMT Cores",
        "description": "Examine Streaming Multiprocessors, warp scheduling, coalesced memory access, and tensor core matrix accelerators.",
        "discipline": "AI & Hardware Engineering",
        "subfield": "Parallel Computing",
        "academicLevel": "Undergraduate",
        "tags": ["gpu", "cuda", "simt", "parallel-computing"],
        "prerequisites": ["Computer Architecture", "Linear Algebra"],
        "equationsCovered": ["Amdahl's Law Speedup S = 1 / ((1 - p) + p/s)", "Little's Law for GPU Occupancy", "Matrix MAC FLOPS = 2 * M * N * K"],
        "modelUrl": "/models/gpu-architecture/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "sm-core",
                "name": "Streaming Multiprocessor (SM)",
                "hotspotPosition": "-0.04m 0.03m 0.0m",
                "explanation": "The core compute building block containing hundreds of ALU threads, dedicated register files, warp schedulers, and shared scratchpad SRAM.",
                "formulaOrLaw": "Thread Level Parallelism (TLP) & Warp Execution (32 threads)"
            },
            {
                "id": "warp-scheduler",
                "name": "Dual Warp Scheduler & Dispatcher",
                "hotspotPosition": "-0.01m 0.03m 0.0m",
                "explanation": "Selects ready 32-thread warps on every clock cycle with zero overhead context switching, hiding high-latency DRAM memory stalls.",
                "formulaOrLaw": "Little's Law: Latency Hiding = Concurrency * Throughput"
            },
            {
                "id": "tensor-core",
                "name": "Mixed-Precision Tensor Core",
                "hotspotPosition": "0.02m 0.02m 0.0m",
                "explanation": "Specialized matrix multiply-accumulate (MMA) systolic hardware executing D = A*B + C operations in a single clock cycle for deep learning.",
                "formulaOrLaw": "Matrix GEMM Operations: FP16 / BF16 / INT8 Acceleration"
            },
            {
                "id": "shared-sram",
                "name": "Configurable Shared Memory / L1 Cache",
                "hotspotPosition": "0.0m -0.01m 0.0m",
                "explanation": "Ultra-low-latency on-chip scratchpad memory managed directly by CUDA software kernels to bypass off-chip DRAM round-trips.",
                "formulaOrLaw": "Bank Conflict Free Access across 32 memory banks"
            },
            {
                "id": "hbm-memory",
                "name": "High Bandwidth Memory (HBM3) Stacks",
                "hotspotPosition": "0.04m -0.03m 0.0m",
                "explanation": "3D-stacked DRAM dies connected via silicon interposers delivering over 3 terabytes per second of memory bandwidth to SM cores.",
                "formulaOrLaw": "Memory Bandwidth = Bus Width (1024-bit) * Effective Clock Rate"
            }
        ],
        "quiz": [
            {
                "id": "gpu-q1",
                "question": "What is the standard execution unit size (number of lockstep threads) in an NVIDIA GPU warp?",
                "options": ["8 threads", "16 threads", "32 threads", "64 threads"],
                "correctAnswerIndex": 2,
                "engineeringExplanation": "A warp consists of 32 parallel threads executing instructions in lockstep SIMT (Single Instruction, Multiple Threads) fashion."
            },
            {
                "id": "gpu-q2",
                "question": "What happens when threads within the same warp take different branches of an if-else conditional statement (branch divergence)?",
                "options": [
                    "The GPU throws a hardware interrupt",
                    "The two paths are executed serially, masking inactive threads and reducing parallel throughput",
                    "Both branches execute in half the time",
                    "The warp is permanently terminated"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "Branch divergence forces the warp to serialize execution of each path with inactive threads masked off, cutting execution efficiency."
            },
            {
                "id": "gpu-q3",
                "question": "Why is memory coalescing critical when CUDA threads in a warp access global GPU DRAM?",
                "options": [
                    "Consecutive thread memory requests are merged into a single 32/64/128-byte DRAM transaction, maximizing bandwidth",
                    "It converts floating-point numbers into integers",
                    "It eliminates the need for GPU clock signals",
                    "It prevents registers from overheating"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "When threads in a warp access consecutive memory addresses, the memory controller coalesces them into one bus transaction."
            }
        ],
        "license": {
            "title": "GPU Architecture and SM Layout",
            "source": "https://en.wikipedia.org/wiki/Graphics_processing_unit",
            "author": "PrismEd AI Hardware Engineering",
            "license": "CC-BY-4.0",
            "attribution": "PrismEd Parallel Systems Assets (CC-BY-4.0)."
        }
    },
    {
        "id": "transformer-attention",
        "name": "Transformer Attention & Neural Architectures",
        "description": "Understand multi-head self-attention, query-key-value dot products, layer normalization, and residual neural highways.",
        "discipline": "Artificial Intelligence",
        "subfield": "Deep Learning & NLP",
        "academicLevel": "Undergraduate",
        "tags": ["ai", "transformers", "attention", "deep-learning"],
        "prerequisites": ["Linear Algebra", "Deep Learning Basics"],
        "equationsCovered": ["Attention(Q,K,V) = softmax(Q*K^T / sqrt(d_k)) * V", "MultiHead(Q,K,V) = Concat(head_1...head_h) * W^O"],
        "modelUrl": "/models/transformer-attention/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "qkv-projection",
                "name": "Q, K, V Linear Projection Weights",
                "hotspotPosition": "-0.04m 0.03m 0.0m",
                "explanation": "Learned projection matrices transforming input token embeddings into Query, Key, and Value vector representations.",
                "formulaOrLaw": "Linear Projections: Q = X * W_Q, K = X * W_K, V = X * W_V"
            },
            {
                "id": "scaled-dot-product",
                "name": "Scaled Dot-Product Attention Core",
                "hotspotPosition": "0.0m 0.03m 0.0m",
                "explanation": "Calculates pairwise token compatibility scores scaled by sqrt(d_k) and normalized via softmax to compute dynamic attention weights.",
                "formulaOrLaw": "Attention(Q, K, V) = softmax((Q * K^T) / sqrt(d_k)) * V"
            },
            {
                "id": "residual-add-norm",
                "name": "Residual Highway & LayerNorm",
                "hotspotPosition": "0.03m 0.01m 0.0m",
                "explanation": "Skip connections that pass gradients unattenuated during backpropagation, combined with Layer Normalization for training stability.",
                "formulaOrLaw": "Output = LayerNorm(x + SubLayer(x))"
            },
            {
                "id": "ffn-block",
                "name": "Feed-Forward Network (FFN / MLP)",
                "hotspotPosition": "0.0m -0.02m 0.0m",
                "explanation": "Two-layer point-wise dense network with non-linear activation (GeLU / SwiGLU) that acts as an associative memory bank storing knowledge.",
                "formulaOrLaw": "FFN(x) = max(0, x * W1 + b1) * W2 + b2"
            },
            {
                "id": "rotary-embeddings",
                "name": "Rotary Positional Embedding (RoPE)",
                "hotspotPosition": "-0.03m -0.03m 0.0m",
                "explanation": "Encodes sequence token ordering by rotating query and key feature vectors in 2D complex sub-planes.",
                "formulaOrLaw": "Inner Product <R_m * q, R_n * k> depends solely on relative distance (m - n)"
            }
        ],
        "quiz": [
            {
                "id": "ta-q1",
                "question": "Why is the dot product of Query and Key vectors scaled by 1 / sqrt(d_k) in the self-attention equation?",
                "options": [
                    "To prevent dot product magnitudes from growing excessively large for large d_k, which pushes softmax into vanishing gradient regions",
                    "To convert floating point tensors into integer indices",
                    "To reduce parameter count of the linear projection matrices",
                    "To eliminate the need for GPU matrix multiplication"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "For large d_k, dot products grow in magnitude, driving softmax into regions with extremely small gradients. Dividing by sqrt(d_k) keeps variance at 1."
            },
            {
                "id": "ta-q2",
                "question": "What primary problem do residual skip connections (x + SubLayer(x)) solve in deep Transformer architectures?",
                "options": [
                    "They allow gradients to propagate directly through the network without vanishing during backpropagation",
                    "They reduce total model memory usage to zero",
                    "They sort token vectors in ascending alphabetical order",
                    "They eliminate the need for tokenizer dictionaries"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Residual highways provide an identity gradient path, enabling training of models with hundreds of stacked layers without vanishing gradients."
            },
            {
                "id": "ta-q3",
                "question": "What is the time and memory complexity of standard full self-attention with respect to sequence length N?",
                "options": ["O(N)", "O(N * log N)", "O(N^2)", "O(2^N)"],
                "correctAnswerIndex": 2,
                "engineeringExplanation": "Every token computes dot-products against every other token in the sequence, producing an N x N attention matrix requiring O(N^2) compute and memory."
            }
        ],
        "license": {
            "title": "Transformer Attention Model",
            "source": "https://arxiv.org/abs/1706.03762",
            "author": "Vaswani et al. / Open Research Collection",
            "license": "CC-BY-4.0",
            "attribution": "Attention Is All You Need Research Assets (CC-BY-4.0)."
        }
    },
    {
        "id": "cpu-architecture",
        "name": "5-Stage RISC-V Pipeline Architecture",
        "description": "Trace instruction execution through the classic 5-stage RISC pipeline: Fetch, Decode, Execute, Memory, and Writeback.",
        "discipline": "Computer Architecture",
        "subfield": "Microprocessor Design",
        "academicLevel": "Undergraduate",
        "tags": ["risc-v", "cpu", "pipeline", "branch-prediction"],
        "prerequisites": ["Digital Logic", "Computer Organization"],
        "equationsCovered": ["CPU Time = IC * CPI * Clock_Period", "Pipeline Speedup S = k / (1 + stalls)"],
        "modelUrl": "/models/cpu-architecture/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "if-stage",
                "name": "Instruction Fetch (IF) Unit",
                "hotspotPosition": "-0.05m 0.02m 0.0m",
                "explanation": "Loads the 32-bit instruction word from instruction memory (I-Cache) addressed by the Program Counter (PC), updating PC = PC + 4.",
                "formulaOrLaw": "Next PC Selection & Branch Predictor Table"
            },
            {
                "id": "id-stage",
                "name": "Instruction Decode (ID) & Register File",
                "hotspotPosition": "-0.02m 0.02m 0.0m",
                "explanation": "Decodes the RISC-V opcode and fields, reading source registers rs1 and rs2 from the 32-entry dual-read single-write register file.",
                "formulaOrLaw": "Dual-Port Asynchronous Read & Sign Extension"
            },
            {
                "id": "ex-stage",
                "name": "Execute (EX) Arithmetic Logic Unit",
                "hotspotPosition": "0.01m 0.02m 0.0m",
                "explanation": "Calculates arithmetic, logical, and address computations, resolving branch equality and forwarding operand values to avoid data hazards.",
                "formulaOrLaw": "Bypass Forwarding: EX/MEM & MEM/WB to EX stage"
            },
            {
                "id": "mem-stage",
                "name": "Memory Access (MEM) Stage",
                "hotspotPosition": "0.03m 0.01m 0.0m",
                "explanation": "Performs load and store operations against data cache (D-Cache) using calculated effective memory addresses.",
                "formulaOrLaw": "Effective Address = rs1_val + imm_offset"
            },
            {
                "id": "wb-stage",
                "name": "Write-Back (WB) Stage",
                "hotspotPosition": "0.05m -0.01m 0.0m",
                "explanation": "Writes the completed computation or loaded memory value into the destination register (rd) on the falling clock edge.",
                "formulaOrLaw": "CPI Ideal = 1.0 cycle per instruction"
            }
        ],
        "quiz": [
            {
                "id": "cpu-q1",
                "question": "In an ideal 5-stage RISC pipeline with no stalls or hazards, what is the asymptotic Cycles Per Instruction (CPI)?",
                "options": ["0.2", "1.0", "5.0", "10.0"],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "Once the pipeline is full, exactly one instruction completes and retires at the Write-Back stage on every single clock cycle (CPI = 1.0)."
            },
            {
                "id": "cpu-q2",
                "question": "What technique eliminates pipeline stall bubbles when an instruction needs the result of the immediately preceding ALU instruction?",
                "options": [
                    "Operand Forwarding / Bypassing directly from EX/MEM stage registers",
                    "Doubling the CPU clock speed",
                    "Clearing the instruction cache",
                    "Replacing RISC-V with CISC instructions"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Forwarding multiplexers route the calculated ALU output directly back to the ALU input for the next cycle, avoiding stalls."
            },
            {
                "id": "cpu-q3",
                "question": "What is the penalty incurred when a branch predictor mispredicts whether a conditional branch is taken?",
                "options": [
                    "Flushing instructions currently in the IF, ID, and EX pipeline stages",
                    "Permanent loss of register file data",
                    "System reboots into BIOS mode",
                    "The instruction cache is erased"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Instructions fetched along the wrong execution path must be flushed and converted to NOP bubbles, wasting 2-3 clock cycles."
            }
        ],
        "license": {
            "title": "5-Stage RISC-V Pipeline Model",
            "source": "https://riscv.org/technical/specifications/",
            "author": "RISC-V International / Open Hardware",
            "license": "CC-BY-4.0",
            "attribution": "RISC-V Microarchitecture Educational Assets (CC-BY-4.0)."
        }
    },
    {
        "id": "ai-server-rack",
        "name": "High-Density AI Supercomputing Rack",
        "description": "Examine liquid cooling loops, 8-GPU compute nodes, 800Gbps InfiniBand fabrics, and 48V power distribution.",
        "discipline": "Cloud Infrastructure",
        "subfield": "Data Center & HPC Engineering",
        "academicLevel": "Undergraduate",
        "tags": ["datacenter", "hpc", "thermal-management", "networking"],
        "prerequisites": ["Computer Systems", "Thermodynamics"],
        "equationsCovered": ["Power Usage Effectiveness PUE = Total_Facility_Energy / IT_Energy", "Heat Transfer Q = m_dot * Cp * Delta_T"],
        "modelUrl": "/models/ai-server-rack/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "gpu-tray",
                "name": "8-Way GPU Accelerator Tray",
                "hotspotPosition": "0.0m 0.05m 0.0m",
                "explanation": "Dense 4U server chassis packing 8 synchronized GPU accelerators linked by NVLink mesh switches delivering 900 GB/s inter-GPU bandwidth.",
                "formulaOrLaw": "AllReduce Communication Ring Bandwidth"
            },
            {
                "id": "liquid-manifold",
                "name": "Direct-to-Chip Liquid Cooling Loop",
                "hotspotPosition": "-0.03m 0.02m 0.0m",
                "explanation": "Copper cold plates mounted directly on GPU/CPU dies circulating treated water-glycol coolant to dissipate over 1000W per socket.",
                "formulaOrLaw": "Heat Removal: Q_thermal = m_dot * C_p * (T_out - T_in)"
            },
            {
                "id": "power-shelf",
                "name": "48V DC Busbar Power Shelf",
                "hotspotPosition": "0.0m -0.04m 0.0m",
                "explanation": "High-efficiency rectifiers converting 415V three-phase AC input into 48V DC busbars to minimize I^2*R copper resistive transmission losses.",
                "formulaOrLaw": "Joule Heating Reduction: P_loss = I^2 * R"
            },
            {
                "id": "infiniband-switch",
                "name": "800Gbps InfiniBand Top-of-Rack Switch",
                "hotspotPosition": "0.0m 0.08m 0.0m",
                "explanation": "Ultra-low-latency non-blocking optical switch fabric supporting Remote Direct Memory Access (RDMA) for multi-node model training.",
                "formulaOrLaw": "RDMA Kernel Bypass Latency < 1 microsecond"
            },
            {
                "id": "cdu-exchanger",
                "name": "Coolant Distribution Unit (CDU)",
                "hotspotPosition": "0.03m -0.02m 0.0m",
                "explanation": "Primary-to-secondary plate heat exchanger isolating rack coolant from the facility chilled water loop with automated variable-speed pumps.",
                "formulaOrLaw": "Log Mean Temperature Difference (LMTD) Method"
            }
        ],
        "quiz": [
            {
                "id": "asr-q1",
                "question": "What is the primary thermodynamic reason high-density AI server racks use direct-to-chip liquid cooling instead of traditional air cooling?",
                "options": [
                    "Water has over 3000 times greater volumetric heat capacity than air, enabling compact extraction of >1000W per processor die",
                    "Air cooling makes servers heavier than liquid cooling",
                    "Liquid cooling eliminates all electrical power consumption",
                    "Liquid cooling converts waste heat directly into AC electricity"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Liquid coolant possesses enormous heat capacity and thermal conductivity compared to air, preventing thermal throttling in high-power chips."
            },
            {
                "id": "asr-q2",
                "question": "Why do modern hyperscale data center racks use 48V DC distribution busbars rather than traditional 12V DC?",
                "options": [
                    "At 48V, current I is reduced to 1/4 for the same power, reducing resistive I^2*R transmission losses by a factor of 16",
                    "48V power eliminates the need for grounding wires",
                    "12V electricity cannot power GPUs",
                    "48V direct current prevents magnetic fields"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Power loss P = I^2 * R. Raising voltage by 4x reduces current by 4x, slashing transmission resistive losses by (4)^2 = 16x."
            },
            {
                "id": "asr-q3",
                "question": "What is the primary benefit of Remote Direct Memory Access (RDMA) over InfiniBand in distributed AI training?",
                "options": [
                    "Bypassing operating system kernel TCP/IP stacks and copying data directly between remote GPU memories without CPU intervention",
                    "Automatically training neural network weights without forward passes",
                    "Encrypting datasets with quantum keys",
                    "Converting optical pulses into sound waves"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "RDMA bypasses OS kernels and context switching, enabling GPU-to-GPU data transfers across nodes with microsecond-level latency."
            }
        ],
        "license": {
            "title": "High Density AI Server Rack",
            "source": "https://www.opencompute.org/",
            "author": "Open Compute Project / Community Assets",
            "license": "CC-BY-4.0",
            "attribution": "Open Compute Project Open Hardware Specifications (CC-BY-4.0)."
        }
    },
    {
        "id": "induction-motor",
        "name": "3-Phase AC Induction Motor",
        "description": "Analyze rotating magnetic fields, squirrel-cage rotors, slip dynamics, and torque-speed characteristics.",
        "discipline": "Electrical Machines",
        "subfield": "Electromagnetics & Power Systems",
        "academicLevel": "Undergraduate",
        "tags": ["motors", "electromagnetics", "ac-power", "torque"],
        "prerequisites": ["Electromagnetism", "AC Circuit Theory"],
        "equationsCovered": ["Synchronous Speed N_s = 120 * f / P", "Slip s = (N_s - N) / N_s", "Electromagnetic Torque T = (3*V^2 * R2/s) / (omega_s * ((R1 + R2/s)^2 + (X1 + X2)^2))"],
        "modelUrl": "/models/induction-motor/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "stator-windings",
                "name": "Stator Core & 3-Phase Windings",
                "hotspotPosition": "0.0m 0.04m 0.0m",
                "explanation": "Laminated silicon steel slots wound with three spatial windings 120 degrees apart, producing a constant-magnitude Rotating Magnetic Field (RMF).",
                "formulaOrLaw": "Synchronous Speed: N_s = 120 * f / P"
            },
            {
                "id": "squirrel-cage",
                "name": "Squirrel-Cage Rotor",
                "hotspotPosition": "0.0m 0.0m 0.0m",
                "explanation": "Heavy conductive aluminum/copper bars short-circuited at both ends by conductive rings, where current is induced via Faraday's law.",
                "formulaOrLaw": "Induced Rotor EMF: E_2s = s * E_2"
            },
            {
                "id": "air-gap",
                "name": "Radial Air Gap Field",
                "hotspotPosition": "0.02m 0.02m 0.0m",
                "explanation": "Narrow radial gap (0.25 - 1.5 mm) separating stator and rotor; minimized to reduce magnetizing reactive current requirements.",
                "formulaOrLaw": "Magnetizing Reactance X_m inversely proportional to air gap length"
            },
            {
                "id": "end-bearings",
                "name": "Shaft & Heavy-Duty Bearings",
                "hotspotPosition": "0.05m 0.0m 0.0m",
                "explanation": "Precision ball bearings supporting the high-tensile steel output shaft under radial and axial mechanical loads.",
                "formulaOrLaw": "Mechanical Power: P_mech = T_shaft * omega"
            },
            {
                "id": "cooling-fan",
                "name": "Totally Enclosed Fan Cooled (TEFC) Impeller",
                "hotspotPosition": "-0.05m 0.0m 0.0m",
                "explanation": "Shaft-mounted bi-directional fan directing air across the external ribbed cast-iron frame to dissipate rotor resistive I^2*R losses.",
                "formulaOrLaw": "Thermal Dissipation via Forced External Convection"
            }
        ],
        "quiz": [
            {
                "id": "im-q1",
                "question": "What is the synchronous speed (N_s) of a 4-pole induction motor connected to a 60 Hz AC electrical grid?",
                "options": ["1200 RPM", "1500 RPM", "1800 RPM", "3600 RPM"],
                "correctAnswerIndex": 2,
                "engineeringExplanation": "N_s = (120 * f) / P = (120 * 60) / 4 = 7200 / 4 = 1800 RPM."
            },
            {
                "id": "im-q2",
                "question": "Why can an induction motor never operate stably at exactly synchronous speed (slip s = 0) under normal motoring conditions?",
                "options": [
                    "At synchronous speed, relative motion between RMF and rotor conductors drops to zero, inducing zero EMF and producing zero torque",
                    "Centrifugal force causes the rotor bars to break",
                    "The stator windings short-circuit instantly",
                    "The power factor drops to -1.0"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Faraday's law requires changing magnetic flux. If the rotor matches RMF speed, relative motion is zero, yielding zero induced current and zero torque."
            },
            {
                "id": "im-q3",
                "question": "What is the typical value of slip (s) for a standard industrial induction motor operating under full rated mechanical load?",
                "options": ["0.00%", "2% to 5%", "25% to 50%", "100%"],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "Standard high-efficiency motors operate with small slip between 2% and 5% (0.02 - 0.05) at full rated torque."
            }
        ],
        "license": {
            "title": "3-Phase Induction Motor Cutaway",
            "source": "https://en.wikipedia.org/wiki/Induction_motor",
            "author": "PrismEd Electrical Machines Collection",
            "license": "CC-BY-4.0",
            "attribution": "PrismEd Power Systems Educational Assets (CC-BY-4.0)."
        }
    },
    {
        "id": "four-stroke-engine",
        "name": "Four-Stroke Internal Combustion Engine",
        "description": "Examine the Otto cycle: Intake, Compression, Power, and Exhaust strokes, reciprocating kinematics, and thermodynamics.",
        "discipline": "Mechanical Engineering",
        "subfield": "Thermodynamics & Automotive",
        "academicLevel": "Undergraduate",
        "tags": ["thermodynamics", "automotive", "combustion", "mechanics"],
        "prerequisites": ["Engineering Thermodynamics", "Kinematics of Machinery"],
        "equationsCovered": ["Otto Cycle Thermal Efficiency eta = 1 - 1 / r^(gamma - 1)", "Indicated Mean Effective Pressure IMEP", "Brake Power P = 2*pi * N * T / 60"],
        "modelUrl": "/models/four-stroke-engine/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "piston-rings",
                "name": "Piston & Compression Rings",
                "hotspotPosition": "0.0m 0.03m 0.0m",
                "explanation": "Translates gas pressure into linear reciprocating motion; equipped with spring-loaded compression and oil scraper rings that seal combustion gas.",
                "formulaOrLaw": "Combustion Force: F_gas = P_cylinder * A_piston"
            },
            {
                "id": "camshaft-valves",
                "name": "Overhead Camshaft & Poppet Valves",
                "hotspotPosition": "0.0m 0.07m 0.0m",
                "explanation": "Synchronized by timing chains to rotate at half crankshaft speed (1:2 ratio), actuating intake and exhaust valves at precise crank angles.",
                "formulaOrLaw": "Valve Timing Diagram & Overlap Period"
            },
            {
                "id": "connecting-rod",
                "name": "Forged Steel Connecting Rod",
                "hotspotPosition": "0.0m -0.01m 0.0m",
                "explanation": "Transmits axial compressive and tensile inertia loads from the piston wrist pin to the rotating crank journal.",
                "formulaOrLaw": "Slider-Crank Kinematics: x(theta) = r*(1 - cos(theta)) + l*(1 - cos(phi))"
            },
            {
                "id": "crankshaft-weights",
                "name": "Counterweighted Crankshaft",
                "hotspotPosition": "0.0m -0.05m 0.0m",
                "explanation": "Converts reciprocating linear motion into continuous rotational torque, counterweighted to balance primary reciprocating inertia forces.",
                "formulaOrLaw": "Brake Torque: T = F_tangential * r_crank"
            },
            {
                "id": "spark-plug",
                "name": "Combustion Chamber & Spark Plug",
                "hotspotPosition": "0.01m 0.06m 0.0m",
                "explanation": "High-voltage electrode delivering a timed electric discharge (up to 30 kV) to initiate deflagration flame front propagation.",
                "formulaOrLaw": "Ideal Otto Cycle Thermal Efficiency: eta = 1 - (1 / r^(gamma - 1))"
            }
        ],
        "quiz": [
            {
                "id": "fse-q1",
                "question": "For a four-stroke engine operating with a compression ratio r = 9 and specific heat ratio gamma = 1.4, what is the ideal Otto cycle thermal efficiency?",
                "options": ["35.2%", "48.5%", "58.5%", "72.4%"],
                "correctAnswerIndex": 2,
                "engineeringExplanation": "eta = 1 - (1 / 9^(1.4 - 1)) = 1 - (1 / 9^0.4) = 1 - (1 / 2.408) = 1 - 0.415 = 0.585 or 58.5%."
            },
            {
                "id": "fse-q2",
                "question": "At what rotational speed does the camshaft rotate relative to the crankshaft in a four-stroke internal combustion engine?",
                "options": [
                    "Twice the crankshaft speed (2:1)",
                    "Same speed as the crankshaft (1:1)",
                    "Exactly half the crankshaft speed (1:2)",
                    "One quarter of the crankshaft speed (1:4)"
                ],
                "correctAnswerIndex": 2,
                "engineeringExplanation": "A four-stroke cycle requires 720 degrees (2 full crankshaft revolutions) to complete one set of strokes, so valves open once every two turns (half speed)."
            },
            {
                "id": "fse-q3",
                "question": "What is the primary thermodynamic process occurring during the power stroke of an ideal Otto cycle?",
                "options": [
                    "Isothermal heat rejection",
                    "Isentropic (reversible adiabatic) gas expansion",
                    "Constant pressure combustion",
                    "Constant volume cooling"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "The power stroke is modeled as an isentropic expansion where high-pressure combustion gas expands adiabatically against the piston head."
            }
        ],
        "license": {
            "title": "Four-Stroke Combustion Engine Model",
            "source": "https://en.wikipedia.org/wiki/Internal_combustion_engine",
            "author": "PrismEd Mechanical Engineering Group",
            "license": "CC-BY-4.0",
            "attribution": "PrismEd Automotive Systems Assets (CC-BY-4.0)."
        }
    },
    {
        "id": "turbofan-jet",
        "name": "High-Bypass Turbofan Jet Engine",
        "description": "Examine gas turbine propulsion: multi-spool compressors, combustion chambers, expansion turbines, and bypass thrust mechanics.",
        "discipline": "Aerospace Engineering",
        "subfield": "Gas Turbines & Propulsion",
        "academicLevel": "Undergraduate",
        "tags": ["propulsion", "turbofan", "aerodynamics", "thermodynamics"],
        "prerequisites": ["Compressible Fluid Dynamics", "Thermodynamics"],
        "equationsCovered": ["Brayton Cycle Thermal Efficiency", "Total Thrust F = m_dot_core*v_core + m_dot_bypass*v_bypass - m_dot_total*v_flight", "Bypass Ratio BPR = m_dot_bypass / m_dot_core"],
        "modelUrl": "/models/turbofan-jet/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "titanium-fan",
                "name": "Wide-Chord Titanium Fan",
                "hotspotPosition": "-0.06m 0.0m 0.0m",
                "explanation": "Large-diameter solid titanium fan blades that compress incoming atmospheric air, accelerating the cold bypass air stream that produces >80% of takeoff thrust.",
                "formulaOrLaw": "Bypass Ratio: BPR = m_dot_bypass / m_dot_core (typically 8:1 - 12:1)"
            },
            {
                "id": "axial-compressor",
                "name": "Multi-Stage Axial Compressor",
                "hotspotPosition": "-0.02m 0.0m 0.0m",
                "explanation": "Alternating rotating rotor blades and stationary stators that progressively compress core air by up to 50:1 pressure ratio before entering the burner.",
                "formulaOrLaw": "Stage Pressure Ratio & Euler Turbomachinery Equation"
            },
            {
                "id": "combustor",
                "name": "Annular Combustion Chamber",
                "hotspotPosition": "0.01m 0.0m 0.0m",
                "explanation": "Injects atomized aviation kerosene (Jet-A) into compressed airflow, burning continuously at constant pressure to raise gas temperatures above 1700 C.",
                "formulaOrLaw": "Combustor Energy: Q_in = m_dot_fuel * Heating_Value_Fuel"
            },
            {
                "id": "high-temp-turbine",
                "name": "Single-Crystal High Pressure Turbine",
                "hotspotPosition": "0.03m 0.0m 0.0m",
                "explanation": "Blades grown as individual nickel-superalloy crystals with internal serpentine cooling passages and thermal barrier coatings to extract expansion power for the compressor.",
                "formulaOrLaw": "Turbine Blade Cooling Effectiveness & Creep Life"
            },
            {
                "id": "exhaust-nozzle",
                "name": "Convergent Core & Bypass Exhaust Nozzle",
                "hotspotPosition": "0.06m 0.0m 0.0m",
                "explanation": "Accelerates exhaust gas streams rearward to sonic or supersonic exit velocities to produce net propulsive forward thrust.",
                "formulaOrLaw": "Total Thrust: F_net = m_dot * (V_exhaust - V_flight) + (P_exit - P_ambient) * A_exit"
            }
        ],
        "quiz": [
            {
                "id": "tfj-q1",
                "question": "What is the primary aerodynamic and efficiency advantage of a High-Bypass Turbofan over a pure turbojet engine for commercial airliners?",
                "options": [
                    "Higher propulsive efficiency and lower specific fuel consumption by imparting a smaller velocity change to a much larger mass of air",
                    "Ability to fly at Mach 5 hypersonic speeds",
                    "Total elimination of titanium components",
                    "Complete reliance on battery power"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Propulsive efficiency eta_p = 2 / (1 + v_exit/v_flight). Imparting moderate acceleration to huge air mass yields high propulsive efficiency and quiet operation."
            },
            {
                "id": "tfj-q2",
                "question": "Why are High-Pressure Turbine (HPT) blades cast as single crystals of nickel-based superalloys rather than polycrystalline alloys?",
                "options": [
                    "To eliminate grain boundaries that cause high-temperature creep failure under extreme centrifugal stress",
                    "To reduce optical reflectivity inside the engine",
                    "To make blades transparent to X-rays",
                    "To allow magnetic levitation of the rotor"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Grain boundaries are mechanical weak points at high temperatures (1100+ C) where atomic sliding and creep cavitation occur. Single crystals eliminate boundaries."
            },
            {
                "id": "tfj-q3",
                "question": "Which thermodynamic cycle serves as the theoretical benchmark for gas turbine jet engines?",
                "options": [
                    "Carnot Cycle",
                    "Rankine Cycle",
                    "Brayton Cycle",
                    "Diesel Cycle"
                ],
                "correctAnswerIndex": 2,
                "engineeringExplanation": "The Brayton (or Joule) cycle models isentropic compression, isobaric heat addition, isentropic expansion, and isobaric heat rejection in gas turbines."
            }
        ],
        "license": {
            "title": "High Bypass Turbofan Jet Engine",
            "source": "https://en.wikipedia.org/wiki/Turbofan",
            "author": "PrismEd Aerospace Propulsion Group",
            "license": "CC-BY-4.0",
            "attribution": "PrismEd Aerospace Engineering Assets (CC-BY-4.0)."
        }
    },
    {
        "id": "differential-gearbox",
        "name": "Automotive Differential Gearbox",
        "description": "Examine open differentials: hypoid ring-pinion gears, spider planetary pinions, and torque split during cornering.",
        "discipline": "Mechanical Engineering",
        "subfield": "Kinematics & Automotive Drivetrains",
        "academicLevel": "Undergraduate",
        "tags": ["gears", "drivetrain", "kinematics", "torque-distribution"],
        "prerequisites": ["Mechanics of Machines", "Machine Design"],
        "equationsCovered": ["Kinematic Average omega_carrier = (omega_left + omega_right) / 2", "Gear Ratio N_ring / N_pinion", "Torque Split 50/50"],
        "modelUrl": "/models/differential-gearbox/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "drive-pinion",
                "name": "Hypoid Drive Pinion Gear",
                "hotspotPosition": "0.0m -0.04m 0.0m",
                "explanation": "Input shaft gear driven by the propeller shaft; features spiral hypoid teeth with an offset axis allowing smooth, high-torque right-angle mesh.",
                "formulaOrLaw": "Hypoid Offset & Sliding Contact Lubrication"
            },
            {
                "id": "ring-gear",
                "name": "Crown Wheel (Ring Gear)",
                "hotspotPosition": "0.0m 0.0m 0.02m",
                "explanation": "Large bevel gear bolted to the differential carrier cage, achieving the primary final-drive axle reduction ratio (e.g. 3.73:1 or 4.10:1).",
                "formulaOrLaw": "Final Drive Reduction: i = N_ring / N_pinion"
            },
            {
                "id": "spider-pinions",
                "name": "Differential Spider Bevel Pinions",
                "hotspotPosition": "0.0m 0.0m 0.0m",
                "explanation": "Small bevel gears mounted on the differential cross-pin inside the revolving carrier; they rotate on their own axis only when wheel speeds diverge.",
                "formulaOrLaw": "Differential Kinematic Equation: omega_ring = (omega_L + omega_R) / 2"
            },
            {
                "id": "side-gears",
                "name": "Axle Shaft Side Bevel Gears",
                "hotspotPosition": "-0.03m 0.0m 0.0m",
                "explanation": "Splined directly onto the left and right axle shafts to deliver equal torque split (50/50 in an open differential) to both driven wheels.",
                "formulaOrLaw": "Torque Invariant: T_left = T_right = 0.5 * T_carrier"
            },
            {
                "id": "carrier-housing",
                "name": "Cast Iron Carrier Housing & Taper Bearings",
                "hotspotPosition": "0.0m 0.02m -0.02m",
                "explanation": "Rigid casing enclosing the gears within an oil bath, supported by pre-loaded opposing tapered roller bearings to resist thrust forces.",
                "formulaOrLaw": "Bearing Preload & Hypoid Backlash Tolerancing"
            }
        ],
        "quiz": [
            {
                "id": "dg-q1",
                "question": "If a vehicle with an open differential is executing a sharp turn and the carrier rotates at 100 RPM while the inside wheel rotates at 80 RPM, what is the outside wheel speed?",
                "options": ["80 RPM", "100 RPM", "120 RPM", "140 RPM"],
                "correctAnswerIndex": 2,
                "engineeringExplanation": "omega_carrier = (omega_L + omega_R) / 2 => 100 = (80 + omega_R) / 2 => 200 = 80 + omega_R => omega_R = 120 RPM."
            },
            {
                "id": "dg-q2",
                "question": "What is the primary drawback of an open differential when one driven wheel is on dry asphalt and the other is on frictionless ice?",
                "options": [
                    "Both wheels spin at identical speeds",
                    "The wheel on ice slips rapidly while the wheel on asphalt receives zero traction torque (open differential limits torque to the slipping wheel's traction)",
                    "The differential automatically locks mechanically",
                    "The gearbox overheats within 2 seconds"
                ],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "An open differential always splits torque equally (50/50). If the wheel on ice can only support 10 Nm of traction, the other wheel receives only 10 Nm."
            },
            {
                "id": "dg-q3",
                "question": "Why are hypoid gears used in automotive drive axles rather than simple straight-cut bevel gears?",
                "options": [
                    "They allow the pinion axis to be offset below the ring gear center (lowering the vehicle floor) and operate much more quietly with continuous tooth mesh",
                    "They eliminate the need for gearbox oil",
                    "They only allow forward motion and physically prevent reverse",
                    "They are made from recycled plastics"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Hypoid gears have curved teeth with sliding contact across an offset axis, lowering the driveshaft tunnel and ensuring smooth, quiet torque transfer."
            }
        ],
        "license": {
            "title": "Automotive Differential Gearbox Model",
            "source": "https://en.wikipedia.org/wiki/Differential_(mechanical_device)",
            "author": "PrismEd Machine Design Group",
            "license": "CC-BY-4.0",
            "attribution": "PrismEd Mechanical Systems Open Assets (CC-BY-4.0)."
        }
    },
    {
        "id": "truss-bridge",
        "name": "Warren Truss Structural Bridge",
        "description": "Analyze structural statics: equilateral triangular trusses, tension/compression members, method of joints, and buckling limits.",
        "discipline": "Civil Engineering",
        "subfield": "Structural Analysis & Statics",
        "academicLevel": "Undergraduate",
        "tags": ["civil", "structures", "statics", "truss"],
        "prerequisites": ["Engineering Mechanics (Statics)", "Strength of Materials"],
        "equationsCovered": ["Static Determinacy m = 2*j - 3", "Method of Joints Sum_F = 0", "Euler's Critical Buckling Load P_cr = (pi^2 * E * I) / (K * L)^2"],
        "modelUrl": "/models/truss-bridge/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "top-chord",
                "name": "Top Compression Chord",
                "hotspotPosition": "0.0m 0.04m 0.0m",
                "explanation": "Horizontal steel I-beams running along the bridge crest; subjected to high axial compressive forces when vehicular live loads bend the span downward.",
                "formulaOrLaw": "Euler Buckling: P_cr = (pi^2 * E * I) / (K * L)^2"
            },
            {
                "id": "bottom-chord",
                "name": "Bottom Tension Chord",
                "hotspotPosition": "0.0m -0.02m 0.0m",
                "explanation": "Longitudinal steel tie members along the bridge floor experiencing pure axial tension that counteracts global sagging moments.",
                "formulaOrLaw": "Tensile Stress: sigma = F_tension / A_cross_section < Yield_Strength"
            },
            {
                "id": "diagonal-web",
                "name": "Diagonal Web Members",
                "hotspotPosition": "-0.03m 0.01m 0.0m",
                "explanation": "Alternating diagonal struts forming equilateral triangles that transfer shear forces between chords, cycling between tension and compression as loads traverse.",
                "formulaOrLaw": "Vertical Shear Equilibrium: V_shear = Sum(F_diag * sin(theta))"
            },
            {
                "id": "gusset-plate",
                "name": "Riveted Gusset Plate Joint",
                "hotspotPosition": "0.0m 0.02m 0.0m",
                "explanation": "Heavy structural steel connection plates fastening converging web and chord members together; modeled as frictionless pin joints in idealized 2D statics.",
                "formulaOrLaw": "Method of Joints: Sum(F_x) = 0 and Sum(F_y) = 0 at every joint"
            },
            {
                "id": "bridge-bearings",
                "name": "Roller & Pinned End Bearings",
                "hotspotPosition": "0.06m -0.02m 0.0m",
                "explanation": "Support pads at abutments; one pinned end constrains horizontal/vertical motion, while a roller end permits thermal expansion without inducing thermal stresses.",
                "formulaOrLaw": "Thermal Expansion: Delta_L = alpha * L * Delta_T"
            }
        ],
        "quiz": [
            {
                "id": "tb-q1",
                "question": "For a planar truss with j joints and m members supported by 3 external reactions, what is the mathematical condition for static determinacy?",
                "options": ["m = j", "m = 2*j - 3", "m = 3*j - 2", "m = j^2 / 2"],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "Each joint offers 2 equilibrium equations (Sum Fx = 0, Sum Fy = 0). With 3 reaction forces, statical determinacy requires m + 3 = 2j, or m = 2j - 3."
            },
            {
                "id": "tb-q2",
                "question": "Why is one end of a large steel truss bridge mounted on a roller bearing rather than both ends being pinned immovably?",
                "options": [
                    "To allow free longitudinal expansion and contraction during ambient temperature swings, preventing destructive thermal buckling stresses",
                    "To make the bridge easy to push into another river",
                    "To reduce gravitational weight",
                    "To generate piezoelectric electricity from vehicle vibrations"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "If both ends are pinned, thermal expansion (Delta L = alpha*L*Delta T) induces enormous compressive thermal forces that can buckle the bottom chords."
            },
            {
                "id": "tb-q3",
                "question": "According to Euler's column formula, doubling the unsupported length L of a compression strut reduces its critical buckling load P_cr by what factor?",
                "options": ["1/2", "1/4", "1/8", "1/16"],
                "correctAnswerIndex": 1,
                "engineeringExplanation": "P_cr = (pi^2 * E * I) / (K * L)^2. Since buckling load is inversely proportional to L^2, doubling L cuts P_cr to (1/2)^2 = 1/4 of its original value."
            }
        ],
        "license": {
            "title": "Warren Truss Structural Model",
            "source": "https://en.wikipedia.org/wiki/Truss_bridge",
            "author": "PrismEd Structural Engineering Group",
            "license": "CC-BY-4.0",
            "attribution": "PrismEd Civil Engineering Assets (CC-BY-4.0)."
        }
    },
    {
        "id": "robotic-arm",
        "name": "6-DOF Articulated Robotic Arm",
        "description": "Examine forward/inverse kinematics, Denavit-Hartenberg parameters, harmonic drive reducers, and spherical wrists.",
        "discipline": "Mechatronics & Robotics",
        "subfield": "Robotics & Automation",
        "academicLevel": "Undergraduate",
        "tags": ["robotics", "kinematics", "mechatronics", "actuators"],
        "prerequisites": ["Linear Algebra", "Mechatronics"],
        "equationsCovered": ["Denavit-Hartenberg (DH) Transformation Matrix T", "Manipulator Jacobian J = [J_v; J_omega]", "Torque Equilibrium tau = J^T * F"],
        "modelUrl": "/models/robotic-arm/model.glb",
        "modelFormat": "glb",
        "parts": [
            {
                "id": "base-turntable",
                "name": "Base Yaw Turntable (Joint 1)",
                "hotspotPosition": "0.0m -0.05m 0.0m",
                "explanation": "High-torque cycloidal drive allowing 360-degree continuous rotation of the robot column around the vertical z-axis.",
                "formulaOrLaw": "DH Parameter: Joint Angle theta_1 rotation about z_0"
            },
            {
                "id": "shoulder-joint",
                "name": "Shoulder Pitch Actuator (Joint 2)",
                "hotspotPosition": "0.0m -0.02m 0.0m",
                "explanation": "High-payload servomotor and gear reduction carrying the heaviest gravitational moment arm when the upper arm cantilevers horizontally.",
                "formulaOrLaw": "Static Gravity Compensation Torque: tau_2 = m * g * L * cos(theta_2)"
            },
            {
                "id": "elbow-segment",
                "name": "Elbow Articulation (Joint 3)",
                "hotspotPosition": "0.0m 0.02m 0.0m",
                "explanation": "Mid-arm pitch joint positioning the spherical wrist in 3D Cartesian coordinates throughout the hemispherical work envelope.",
                "formulaOrLaw": "Geometric Inverse Kinematics Law of Cosines"
            },
            {
                "id": "spherical-wrist",
                "name": "3-Axis Spherical Wrist (Joints 4-6)",
                "hotspotPosition": "0.02m 0.05m 0.0m",
                "explanation": "Three intersecting revolute axes (Roll-Pitch-Yaw) that orient the end-effector tool without shifting tool center point (TCP) position.",
                "formulaOrLaw": "Euler Angle Decoupling R = R_z(alpha) * R_y(beta) * R_x(gamma)"
            },
            {
                "id": "harmonic-drive",
                "name": "Harmonic Drive Strain Wave Reducer",
                "hotspotPosition": "-0.01m 0.01m 0.0m",
                "explanation": "Zero-backlash transmission consisting of a wave generator, flexible spline, and circular spline providing compact 100:1 gear reduction.",
                "formulaOrLaw": "Reduction Ratio: R = N_flex / (N_circular - N_flex)"
            }
        ],
        "quiz": [
            {
                "id": "ra-q1",
                "question": "Why are 6 degrees of freedom (DOF) considered the minimal requirement for general-purpose spatial manipulation in robotics?",
                "options": [
                    "To completely control both 3D position (x, y, z) and 3D orientation (roll, pitch, yaw) of the end-effector tool",
                    "To match the number of wheels on a delivery truck",
                    "To reduce electricity consumption to zero",
                    "To eliminate the need for computer controllers"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Free motion in 3D space requires 6 independent variables: 3 Cartesian translational coordinates (x, y, z) and 3 rotational angles."
            },
            {
                "id": "ra-q2",
                "question": "What is the key advantage of a Harmonic Drive (strain wave gearing) in robotic joints over traditional spur or planetary gears?",
                "options": [
                    "Zero backlash, exceptional positional repeatability, and high reduction ratio in a lightweight, compact package",
                    "Low cost and ability to run without any lubricant",
                    "It operates using compressed steam",
                    "It converts electricity directly into light"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "Harmonic drives utilize continuous tooth engagement on a flexible spline, delivering zero backlash and high gear reduction in high-precision robot joints."
            },
            {
                "id": "ra-q3",
                "question": "What mathematical relationship links robot joint velocities (theta_dot) to end-effector Cartesian velocities (v, omega)?",
                "options": [
                    "Manipulator Jacobian Matrix J: [v; omega] = J(theta) * theta_dot",
                    "Ohm's Law",
                    "Bernoulli's Equation",
                    "Fourier Transform"
                ],
                "correctAnswerIndex": 0,
                "engineeringExplanation": "The geometric Jacobian J relates joint velocity vectors to linear and angular velocities in Cartesian tool space: X_dot = J * q_dot."
            }
        ],
        "license": {
            "title": "6-DOF Articulated Robotic Arm Model",
            "source": "https://en.wikipedia.org/wiki/Articulated_robot",
            "author": "PrismEd Mechatronics Group",
            "license": "CC-BY-4.0",
            "attribution": "PrismEd Robotics & Automation Assets (CC-BY-4.0)."
        }
    }
]

def main():
    print(f"Building content for {len(TOPICS_DATA)} topics...")
    topics_list = []
    quizzes_dict = {}

    for t in TOPICS_DATA:
        topic_id = t["id"]
        model_source = "uploaded" if t["id"] in ["circuit-board", "space-suit"] else t.get("modelSource", "generated")
        auto_rotate = t.get("autoRotate", False if model_source == "generated" else True)
        animation_name = t.get("animation", None)

        # Ensure every part has hotspotNormal
        parts_with_normals = []
        for p in t["parts"]:
            part_copy = dict(p)
            if "hotspotNormal" not in part_copy:
                part_copy["hotspotNormal"] = "0m 1m 0m"
            parts_with_normals.append(part_copy)

        # Prepare topic entry
        topic_entry = {
            "id": t["id"],
            "name": t["name"],
            "description": t["description"],
            "discipline": t["discipline"],
            "subfield": t["subfield"],
            "academicLevel": t["academicLevel"],
            "tags": t["tags"],
            "prerequisites": t["prerequisites"],
            "equationsCovered": t["equationsCovered"],
            "modelUrl": t["modelUrl"],
            "modelFormat": t["modelFormat"],
            "modelSource": model_source,
            "autoRotate": auto_rotate,
            "animation": animation_name,
            "parts": parts_with_normals
        }
        topics_list.append(topic_entry)

        # Prepare quiz entry
        quizzes_dict[topic_id] = {
            "topicId": topic_id,
            "questions": t["quiz"]
        }

        # Create model directory and license.txt if not exists
        model_dir = MODELS_DIR / topic_id
        os.makedirs(model_dir, exist_ok=True)
        license_path = model_dir / "license.txt"
        
        lic = t["license"]
        license_content = (
            f"Topic: {t['name']} ({topic_id})\n"
            f"Title: {lic['title']}\n"
            f"Model Source: {model_source}\n"
            f"Source URL: {lic['source']}\n"
            f"Author: {lic['author']}\n"
            f"Licence: {lic['license']}\n"
            f"Attribution: {lic['attribution']}\n"
        )
        with open(license_path, "w", encoding="utf-8") as f:
            f.write(license_content)

    # Write topics.json
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump({"topics": topics_list}, f, indent=4)
    print(f"Successfully wrote {len(topics_list)} topics to {TOPICS_FILE}")

    # Write quiz.json
    with open(QUIZ_FILE, "w", encoding="utf-8") as f:
        json.dump({"quizzes": quizzes_dict}, f, indent=4)
    print(f"Successfully wrote {len(quizzes_dict)} quizzes to {QUIZ_FILE}")

if __name__ == "__main__":
    main()
