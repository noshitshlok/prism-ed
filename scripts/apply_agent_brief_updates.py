import json
from pathlib import Path

TOPICS_FILE = Path("app/data/topics.json")
with open(TOPICS_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

topics = data.get("topics", [])

READY_IDS = {
    "circuit-board",
    "space-suit",
    "human-heart",
    "four-stroke-engine",
    "differential-gearbox",
    "robotic-arm",
    "turbofan-jet",
    "solar-system"
}

UPDATES = {
    "circuit-board": {
        "status": "ready",
        "modelSource": "uploaded",
        "modelUrl": "/models/circuit-board/scene.gltf",
        "modelFormat": "gltf",
        "autoRotate": False,
        "animation": None,
    },
    "space-suit": {
        "status": "ready",
        "modelSource": "uploaded",
        "modelUrl": "/models/space-suit/Astronaut.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
    },
    "human-heart": {
        "status": "ready",
        "modelSource": "scan",
        "modelUrl": "/models/human-heart/model.glb",
        "modelFormat": "glb",
        "autoRotate": False,
        "animation": None,
        "parts_coords": [
            ("aorta", "0.020m 0.520m 0.030m", "0m 1m 0m", None, "VH_M_aortic_valve"),
            ("pulmonary-artery", "0.010m 0.500m 0.060m", "0m 0.5m 1m", None, "VH_M_heart"),
            ("superior-vena-cava", "0.050m 0.510m 0.010m", "1m 0.5m 0m", None, "VH_M_heart"),
            ("left-ventricle", "-0.020m 0.440m 0.050m", "-0.7m -0.5m 0.5m", None, "VH_M_mitral_valve"),
            ("right-ventricle", "0.040m 0.440m 0.040m", "0.7m -0.5m 0.5m", None, "VH_M_tricuspid_valve"),
        ]
    },
    "four-stroke-engine": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/four-stroke-engine/model.glb",
        "modelFormat": "glb",
        "autoRotate": False,
        "animation": "2CylinderEngine",
        "parts_coords": [
            ("cylinder-block", "-60.000m 220.000m -40.000m", "0m 1m 0m", "0m 0.08m 0m", "Block"),
            ("piston-assembly", "-60.000m 140.000m -40.000m", "0m 1m 0m", "0m 0.05m 0m", "Pistons"),
            ("crankshaft", "-60.000m -120.000m -40.000m", "0m -1m 0m", "0m -0.05m 0m", "Crankshaft"),
            ("intake-exhaust-valves", "-60.000m 350.000m -40.000m", "0m 1m 0m", "0m 0.12m 0m", "Valves"),
            ("connecting-rods", "-60.000m 0.000m -40.000m", "1m 0m 0m", "0.05m 0m 0m", "Rods"),
        ]
    },
    "differential-gearbox": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/differential-gearbox/model.glb",
        "modelFormat": "glb",
        "autoRotate": False,
        "animation": None,
        "parts_coords": [
            ("input-pinion-shaft", "1.200m 0.300m -2.000m", "0m 0m -1m", "0m 0m -0.06m", "InputShaft"),
            ("differential-cage", "1.200m 0.300m 5.500m", "0m 1m 0m", "0m 0.05m 0m", "Cage"),
            ("planetary-bevel-gears", "3.000m 0.300m 5.500m", "1m 0m 0m", "0.06m 0m 0m", "PlanetaryPinions"),
            ("sun-gears-axles", "-1.000m 0.300m 5.500m", "-1m 0m 0m", "-0.06m 0m 0m", "SunGears"),
            ("housing-bearings", "1.200m 4.000m 5.500m", "0m 1m 0m", "0m 0.10m 0m", "Housing"),
        ]
    },
    "robotic-arm": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/robotic-arm/model.glb",
        "modelFormat": "glb",
        "autoRotate": False,
        "animation": None,
        "parts_coords": [
            ("shoulder-joint", "0.000m 0.000m 0.000m", "0m 1m 0m", None, "Shoulder"),
            ("upper-arm-boom", "0.000m -150.000m 0.000m", "0m 0m 1m", None, "UpperArm"),
            ("elbow-joint", "0.000m -300.000m 0.000m", "0m 0m 1m", None, "Elbow"),
            ("wrist-joint", "0.000m -450.000m 0.000m", "0m 0m 1m", None, "Wrist"),
            ("end-effector", "0.000m -570.000m 0.000m", "0m -1m 0m", None, "EndEffector"),
        ]
    },
    "turbofan-jet": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/turbofan-jet/model.glb",
        "modelFormat": "glb",
        "autoRotate": False,
        "animation": "saturnv_caAction",
        "parts_coords": [
            ("propulsion-nozzles", "0.000m 0.200m 0.700m", "0m -1m 0m", "0m -0.08m 0m", "F1Nozzles"),
            ("fuel-oxidizer-tanks", "0.000m 3.000m 0.700m", "1m 0m 0m", "0m 0.05m 0m", "PropellantTanks"),
            ("fuselage-interstage", "0.000m 6.000m 0.700m", "0m 1m 0m", "0m 0.10m 0m", "Interstage"),
            ("upper-stages-avionics", "0.000m 9.500m 0.700m", "0m 1m 0m", "0m 0.15m 0m", "InstrumentUnit"),
            ("aerodynamic-fins", "0.000m 12.200m 0.700m", "0m 1m 0m", "0m 0.20m 0m", "EscapeTower"),
        ]
    },
    "solar-system": {
        "status": "ready",
        "modelSource": "cad",
        "modelUrl": "/models/solar-system/model.glb",
        "modelFormat": "glb",
        "autoRotate": True,
        "animation": None,
        "parts_coords": [
            ("heat-shield", "-0.600m 0.800m 1.200m", "0m 0m 1m", None, "ThermalProtectionSystem"),
            ("solar-arrays", "1.500m 0.800m -1.700m", "0m 1m 0m", None, "SolarArray"),
            ("magnetometer-boom", "-0.600m 0.800m -4.500m", "0m 0m -1m", None, "FieldsBoom"),
            ("solar-wind-analyzer", "-2.500m 0.800m -1.700m", "-1m 0m 0m", None, "SweapCup"),
            ("spacecraft-bus", "-0.600m 0.800m -1.700m", "0m 1m 0m", None, "SpacecraftBus"),
        ]
    }
}

for t in topics:
    t_id = t["id"]
    if t_id in READY_IDS:
        cfg = UPDATES[t_id]
        t["status"] = "ready"
        t["modelSource"] = cfg["modelSource"]
        t["modelUrl"] = cfg["modelUrl"]
        t["modelFormat"] = cfg["modelFormat"]
        t["autoRotate"] = cfg["autoRotate"]
        t["animation"] = cfg["animation"]
        
        # update parts if specified
        if "parts_coords" in cfg:
            for idx, p_cfg in enumerate(cfg["parts_coords"]):
                if idx < len(t["parts"]):
                    p = t["parts"][idx]
                    p["id"] = p_cfg[0]
                    p["hotspotPosition"] = p_cfg[1]
                    p["hotspotNormal"] = p_cfg[2]
                    p["explodeOffset"] = p_cfg[3]
                    p["partNode"] = p_cfg[4]
        else:
            for p in t["parts"]:
                p.setdefault("hotspotNormal", "0m 1m 0m")
                p.setdefault("explodeOffset", None)
                p.setdefault("partNode", p.get("id"))
    else:
        t["status"] = "not_in_demo"
        t["modelSource"] = "cad"
        t.setdefault("autoRotate", True)
        t.setdefault("animation", None)
        for p in t["parts"]:
            p.setdefault("hotspotNormal", "0m 1m 0m")
            p.setdefault("explodeOffset", None)
            p.setdefault("partNode", p.get("id"))

with open(TOPICS_FILE, "w", encoding="utf-8") as f:
    json.dump({"topics": topics}, f, indent=4)

print(f"Updated {len(topics)} topics successfully. Ready topics: {len(READY_IDS)}")
