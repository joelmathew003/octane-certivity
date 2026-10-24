"""Script to compile full hackathon submission data into frontend/src/lib/octane-data.ts."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUBMISSIONS = ROOT / "submissions"
FRONTEND_DATA = ROOT / "frontend" / "src" / "lib" / "octane-data.ts"


def categorize_requirement(reg: str, para: str, text: str) -> str:
    lower = (text + " " + para).lower()
    if reg == "UN R10" or "electromagnetic" in lower or "pulse" in lower or "immunity" in lower or "emission" in lower:
        return "Electrical/EMC"
    if "conformity of production" in lower or "cop" in lower or "sample" in lower or "deviation" in lower or "20%" in lower or "30%" in lower:
        return "COP"
    if "mark" in lower or "trade name" in lower or "identification code" in lower or "approval mark" in lower:
        return "Markings"
    if "water" in lower or "thermal" in lower or "heat" in lower or "fuel" in lower or "corrosion" in lower or "endurance" in lower or "moisture" in lower:
        return "Environmental"
    if "intensity" in lower or "candela" in lower or " cd" in lower or "photometric" in lower or "color" in lower or "colour" in lower or "chromaticity" in lower or "trichromatic" in lower or "retro-reflect" in lower or "cil" in lower:
        return "Photometric"
    return "Installation & Visibility"


def tag_requirement(para: str, text: str, category: str) -> str:
    lower = text.lower()
    if "mounting height" in lower or "height above" in lower:
        return "Mounting Height"
    if "geometric visibility" in lower or "angles of geometric visibility" in lower or "visibility" in lower:
        return "Geometric Visibility"
    if "lateral" in lower or "width" in lower or "edge of the illuminating" in lower:
        return "Lateral Position"
    if "intensity" in lower or "minimum intensity" in lower or "maximum intensity" in lower or "candela" in lower or " cd" in lower:
        return "Photometric Intensity"
    if "colour" in lower or "color" in lower or "red" in lower or "amber" in lower or "white" in lower:
        return "Colour & Chromaticity"
    if "approval mark" in lower or "trade name" in lower or "identification code" in lower:
        return "Approval Marking"
    if "fail" in lower or "telltale" in lower or "operating telltale" in lower:
        return "Failure Indication"
    if "conformity of production" in lower or "cop" in lower:
        return "Conformity of Production"
    if "pulse" in lower or "transient" in lower or "iso 7637" in lower:
        return "Transient Immunity"
    if "radiated emission" in lower or "narrowband" in lower or "broadband" in lower:
        return "Radiated Emissions"
    if "radiated immunity" in lower or "field" in lower or "v/m" in lower:
        return "Radiated Immunity"
    if "retro-reflect" in lower or "coefficient of luminous intensity" in lower or "cil" in lower:
        return "Retro-reflection"
    if "water" in lower or "immersion" in lower:
        return "Water Resistance"
    if "fuel" in lower or "solvent" in lower:
        return "Fuel Resistance"
    if "thermal" in lower or "drift" in lower or "stabilisation" in lower:
        return "Thermal Stability"
    if "electrical connection" in lower or "switched on" in lower:
        return "Electrical Connection"
    return f"{category} Provision"


def generate():
    # 1. Dev Rear Lamp
    rear_lamp_file = SUBMISSIONS / "dev-rear-lamp.json"
    rear_lamp_obs = []
    if rear_lamp_file.exists():
        with open(rear_lamp_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        for req in data.get("requirements", []):
            reg = req.get("source", {}).get("regulation", "")
            para = req.get("source", {}).get("paragraph", "")
            page = req.get("source", {}).get("page", 1)
            text = req.get("text", "")
            test = req.get("test_case", "")
            req_id = req.get("id", "")
            cat = categorize_requirement(reg, para, text)
            tag = tag_requirement(para, text, cat)
            rear_lamp_obs.append({
                "id": req_id,
                "reg": reg,
                "para": para,
                "page": page,
                "category": cat,
                "tag": tag,
                "text": text,
                "test": test,
            })

    # 2. Subgoal changes
    subgoal_file = SUBMISSIONS / "subgoal-dev.json"
    modified = []
    added = []
    removed = []
    if subgoal_file.exists():
        with open(subgoal_file, "r", encoding="utf-8") as f:
            sg_data = json.load(f)
        for c in sg_data.get("changes", []):
            ch_type = c.get("change")
            para = f"§{c.get('source', {}).get('paragraph', '')}"
            reason = c.get("reason", "")
            new_text = c.get("new_text", "")
            if ch_type == "modified":
                modified.append({
                    "para": para,
                    "old": "Prior revision wording (superseded)",
                    "new": new_text,
                    "reason": reason,
                })
            elif ch_type == "added":
                added.append({
                    "para": para,
                    "text": new_text,
                    "reason": reason,
                })
            elif ch_type == "removed":
                removed.append({
                    "para": para,
                    "text": new_text or "Provisions repealed in revised regulation.",
                    "reason": reason,
                })

    content = f"""export type Reg = "UN R48" | "UN R148" | "UN R150" | "UN R10";
export type Category =
  | "Photometric"
  | "Installation & Visibility"
  | "Markings"
  | "Electrical/EMC"
  | "Environmental"
  | "COP";

export interface Obligation {{
  id: string;
  reg: Reg;
  para: string;
  page: number;
  category: Category;
  tag: string;
  text: string;
  test: string;
}}

export const REGS: Reg[] = ["UN R48", "UN R148", "UN R150", "UN R10"];
export const CATEGORIES: Category[] = [
  "Photometric",
  "Installation & Visibility",
  "Markings",
  "Electrical/EMC",
  "Environmental",
  "COP",
];

export const REG_TITLES: Record<Reg, string> = {{
  "UN R48": "Installation of lighting and light-signalling devices",
  "UN R148": "Light-signalling devices (LSD)",
  "UN R150": "Retro-reflective devices and markings",
  "UN R10": "Electromagnetic compatibility",
}};

export const REG_SLUG: Record<Reg, string> = {{
  "UN R48": "R48",
  "UN R148": "R148",
  "UN R150": "R150",
  "UN R10": "R10",
}};

const rearLamp: Obligation[] = {json.dumps(rear_lamp_obs, indent=2)};

const bumper: Obligation[] = [
  {{ id: "B-0004", reg: "UN R48", para: "6.14.4", page: 88, category: "Installation & Visibility", tag: "Retro-reflector Height", text: "Rear retro-reflectors integrated in the bumper shall be mounted not less than 250 mm and not more than 900 mm above the ground.", test: "On-vehicle height measurement at unladen mass." }},
  {{ id: "B-0011", reg: "UN R150", para: "6.1.2", page: 11, category: "Photometric", tag: "Retro-reflection", text: "Class IA retro-reflectors shall meet the minimum CIL values of Annex 6.", test: "CIL measurement at prescribed observation/entrance angles." }},
  {{ id: "B-0019", reg: "UN R10", para: "6.8.2", page: 22, category: "Electrical/EMC", tag: "Conducted Transients", text: "Bumper-mounted parking sensor ESAs shall be immune to ISO 7637-2 pulses 1, 2a, 3a, 3b and 4.", test: "ISO 7637-2 bench test, functional class A for pulses 3a/3b." }},
  {{ id: "B-0026", reg: "UN R148", para: "7.1", page: 31, category: "COP", tag: "Conformity of Production", text: "Integrated lamps shall not deviate unfavourably by more than 20% from prescribed values in production.", test: "Random sampling, photometric check." }},
];

export const CASES = {{
  "dev-rear-lamp": {{ label: "Worked Example: dev-rear-lamp (Rear Lamp)", component: "Rear Lamp", obligations: rearLamp }},
  "heldout-front-bumper": {{ label: "Sunday Held-out: heldout-front-bumper (Front Bumper)", component: "Front Bumper", obligations: bumper }},
}} as const;

export type CaseId = keyof typeof CASES;

export const PRUNED = [
  {{ para: "UN R148 §5.9", reason: "Applies to rear fog lamps — not part of this component" }},
  {{ para: "UN R148 §5.11", reason: "Reversing lamp requirements — separate device" }},
  {{ para: "UN R48 §6.2", reason: "Dipped-beam headlamp installation — front lighting only" }},
  {{ para: "UN R150 §6.8", reason: "Conspicuity marking for N3/O4 vehicles — M1 out of scope" }},
  {{ para: "UN R10 §6.9", reason: "RESS charging-mode emissions — not applicable to 12V lamp" }},
  {{ para: "UN R48 §6.21", reason: "Contour marking — category M1 exempt" }},
  {{ para: "UN R48 §6.1", reason: "Main-beam headlamp installation — not applicable" }},
  {{ para: "UN R48 §6.3", reason: "Front fog lamp installation — front lighting only" }},
  {{ para: "UN R48 §6.4", reason: "Reversing lamp installation — separate component" }},
  {{ para: "UN R48 §6.5", reason: "Direction indicator lamp — separate function" }},
  {{ para: "UN R48 §6.6", reason: "Hazard warning signal — system level switch requirement" }},
  {{ para: "UN R48 §6.8", reason: "Rear registration plate illuminating device — separate lamp" }},
  {{ para: "UN R48 §6.9", reason: "Front position lamp — front lighting only" }},
  {{ para: "UN R48 §6.11", reason: "Rear fog lamp — separate lamp assembly" }},
  {{ para: "UN R48 §6.12", reason: "Parking lamp — out of scope for fixed body rear combination" }},
  {{ para: "UN R48 §6.13", reason: "End-outline marker lamp — category M1 exempt" }},
  {{ para: "UN R48 §6.15", reason: "Side retro-reflector, non-triangular — side body only" }},
  {{ para: "UN R48 §6.16", reason: "Rear retro-reflector, triangular — trailer only" }},
  {{ para: "UN R48 §6.17", reason: "Front retro-reflector, non-triangular — front body only" }},
  {{ para: "UN R48 §6.18", reason: "Side marker lamps — commercial vehicle / length > 6m only" }},
  {{ para: "UN R48 §6.19", reason: "Daytime running lamp — front lighting only" }},
  {{ para: "UN R48 §6.20", reason: "Cornering lamp — front lighting only" }},
  {{ para: "UN R48 §6.22", reason: "Adaptive front-lighting system (AFS) — front lighting only" }},
  {{ para: "UN R48 §6.24", reason: "Exterior courtesy lamp — door/mirror mounted only" }},
  {{ para: "UN R48 §6.25", reason: "Rear-end collision alert signal — active ADAS function only" }},
  {{ para: "UN R48 §6.26", reason: "Manoeuvring lamp — specialized utility lighting only" }},
];

export const DIFF = {{
  modified: {json.dumps(modified, indent=2)},
  added: {json.dumps(added, indent=2)},
  removed: {json.dumps(removed, indent=2)},
}};
"""
    with open(FRONTEND_DATA, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {FRONTEND_DATA} with {len(rear_lamp_obs)} obligations and {len(modified)+len(added)+len(removed)} diffs.")


if __name__ == "__main__":
    generate()
