"""Lightweight API server for Certivity Octane UI demo.
Serves:
1. /api/pdf/{reg_slug} - Regulation PDFs with Range support and CORS headers.
2. /api/obligations?case_id={case_id} - Requirements from submissions/dev-rear-lamp.json.
3. /api/subgoal - Subgoal changes from submissions/subgoal-dev.json.
4. /api/analyze - Spec analysis endpoint (supports Demo Mode and Live Pipeline execution).
5. /api/jobs/{job_id} - Job polling endpoint for live pipeline runs.
"""

import json
import os
import re
import sys
import threading
import time
import uuid
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
PDF_DIR = ROOT_DIR / "data" / "regulations" / "pdf"
SUBMISSIONS_DIR = ROOT_DIR / "submissions"
WORK_DIR = ROOT_DIR / "work" / "live_jobs"
WORK_DIR.mkdir(parents=True, exist_ok=True)

# Map frontend reg slugs to disk folder names
REG_MAP = {
    "R48": "UN_R48",
    "UN_R48": "UN_R48",
    "UN R48": "UN_R48",
    "R148": "UN_R148",
    "UN_R148": "UN_R148",
    "UN R148": "UN_R148",
    "R150": "UN_R150",
    "UN_R150": "UN_R150",
    "UN R150": "UN_R150",
    "R10": "UN_R10",
    "UN_R10": "UN_R10",
    "UN R10": "UN_R10",
    "R175": "UN_R175",
    "UN_R175": "UN_R175",
    "UN R175": "UN_R175",
    "R26": "UN_R26",
    "UN_R26": "UN_R26",
    "UN R26": "UN_R26",
}

JOBS = {}


def categorize_requirement(reg: str, para: str, text: str) -> str:
    lower = (text + " " + para).lower()
    if reg == "UN R10" or "electromagnetic" in lower or "pulse" in lower or "immunity" in lower or "emission" in lower:
        return "Electrical/EMC"
    if "conformity of production" in lower or "cop" in lower or "sample" in lower or "deviation" in lower:
        return "COP"
    if "mark" in lower or "trade name" in lower or "identification code" in lower or "approval mark" in lower:
        return "Markings"
    if "water" in lower or "thermal" in lower or "heat" in lower or "fuel" in lower or "corrosion" in lower or "endurance" in lower:
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
    if "intensity" in lower or "minimum intensity" in lower or "maximum intensity" in lower:
        return "Photometric Intensity"
    if "colour" in lower or "color" in lower or "red" in lower or "amber" in lower or "white" in lower:
        return "Colour & Chromaticity"
    if "approval mark" in lower or "trade name" in lower:
        return "Approval Marking"
    if "fail" in lower or "telltale" in lower:
        return "Failure Indication"
    if "conformity of production" in lower or "20%" in lower or "30%" in lower:
        return "Conformity of Production"
    if "pulse" in lower or "transient" in lower:
        return "Transient Immunity"
    if "radiated emission" in lower or "narrowband" in lower or "broadband" in lower:
        return "Radiated Emissions"
    if "radiated immunity" in lower or "field" in lower:
        return "Radiated Immunity"
    if "retro-reflect" in lower or "coefficient of luminous intensity" in lower or "cil" in lower:
        return "Retro-reflection"
    if "water" in lower:
        return "Water Resistance"
    if "fuel" in lower:
        return "Fuel Resistance"
    if "thermal" in lower or "drift" in lower:
        return "Thermal Stability"
    return f"{category} Requirement"


def load_submission_obligations(case_id: str = "dev-rear-lamp", custom_file: Path | None = None):
    path = custom_file if custom_file else SUBMISSIONS_DIR / f"{case_id}.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    obligations = []
    for req in data.get("requirements", []):
        reg = req.get("source", {}).get("regulation", "")
        para = req.get("source", {}).get("paragraph", "")
        page = req.get("source", {}).get("page", 1)
        text = req.get("text", "")
        test = req.get("test_case", "")
        req_id = req.get("id", "")
        cat = categorize_requirement(reg, para, text)
        tag = tag_requirement(para, text, cat)

        obligations.append({
            "id": req_id,
            "reg": reg,
            "para": para,
            "page": page,
            "category": cat,
            "tag": tag,
            "text": text,
            "test": test,
        })
    return obligations


def load_subgoal_diff():
    path = SUBMISSIONS_DIR / "subgoal-dev.json"
    if not path.exists():
        return {"modified": [], "added": [], "removed": []}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    modified = []
    added = []
    removed = []

    for c in data.get("changes", []):
        ch_type = c.get("change")
        para = f"§{c.get('source', {}).get('paragraph', '')}"
        reason = c.get("reason", "")
        new_text = c.get("new_text", "")

        if ch_type == "modified":
            modified.append({
                "para": para,
                "old": "Prior revision wording (see reason).",
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

    return {"modified": modified, "added": added, "removed": removed}


def execute_live_pipeline(job_id: str, spec_text: str):
    job = JOBS[job_id]
    job_dir = WORK_DIR / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    spec_path = job_dir / "spec.md"
    spec_path.write_text(spec_text, encoding="utf-8")

    try:
        job["stage"] = "Querying regulation catalogue & selecting applicable rules..."
        job["progress"] = 25

        # We can invoke the python pipeline directly
        sys.path.insert(0, str(ROOT_DIR))
        from src.pipeline import db, llm, prompts, regs, review, run

        db.ensure_fresh()
        llm.load_env()

        job["stage"] = "Selecting applicable UN regulations with AI..."
        job["progress"] = 40
        selected = run.select_regulations(spec_text, [])

        job["stage"] = f"Extracting obligations across {len(selected)} regulations..."
        job["progress"] = 65

        extracted = {}
        for sel in selected:
            reg_name = sel["regulation"]
            job["stage"] = f"Extracting engineering obligations from {reg_name}..."
            items = run.extract(reg_name, sel["reason"], spec_text)
            extracted[reg_name] = items

        job["stage"] = "Assembling requirements & resolving official PDF page citations..."
        job["progress"] = 80
        assembled = run.assemble("team-16", job_id, extracted)

        job["stage"] = "Executing Type-Approval Engineering Review Agent..."
        job["progress"] = 90
        final_data = review.review(assembled, spec_text, [])

        out_file = job_dir / "submission.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=2)

        obligations = load_submission_obligations(custom_file=out_file)
        job["obligations"] = obligations
        job["status"] = "completed"
        job["stage"] = f"Complete: {len(obligations)} requirements extracted!"
        job["progress"] = 100

    except Exception as e:
        job["status"] = "failed"
        job["stage"] = f"Error: {str(e)}"
        job["progress"] = 100


class OctaneHandler(SimpleHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Expose-Headers", "Content-Range, Content-Length, Accept-Ranges")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_HEAD(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/pdf/"):
            slug = parsed.path.replace("/api/pdf/", "").strip("/")
            folder_name = REG_MAP.get(slug, f"UN_{slug}")
            pdf_path = PDF_DIR / folder_name / "base" / f"{folder_name}_base.pdf"

            if pdf_path.exists():
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Length", str(pdf_path.stat().st_size))
                self.send_header("Accept-Ranges", "bytes")
                self.send_cors_headers()
                self.end_headers()
                return

        self.send_response(404)
        self.send_cors_headers()
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/analyze":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode("utf-8")) if body else {}
            except Exception:
                data = {}

            spec_text = data.get("spec_text", "")
            demo_mode = data.get("demo_mode", True)

            # 1. DEMO MODE (Default): Instant return of verified high-scoring submission
            if demo_mode:
                case_id = "heldout-front-bumper" if re.search(r"bumper|fascia", spec_text, re.I) else "dev-rear-lamp"
                obligations = load_submission_obligations(case_id)
                payload = json.dumps({
                    "status": "completed",
                    "demo_mode": True,
                    "case_id": case_id,
                    "obligations": obligations,
                }).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(payload)
                return

            # 2. LIVE MODE: Spawns real LLM pipeline in background thread
            job_id = f"job-{uuid.uuid4().hex[:8]}"
            JOBS[job_id] = {
                "id": job_id,
                "status": "running",
                "stage": "Initializing AI pipeline...",
                "progress": 10,
                "obligations": [],
                "created_at": time.time(),
            }
            threading.Thread(target=execute_live_pipeline, args=(job_id, spec_text), daemon=True).start()

            payload = json.dumps({
                "status": "running",
                "demo_mode": False,
                "job_id": job_id,
            }).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(payload)
            return

        self.send_response(404)
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(b'{"error": "Endpoint not found"}')

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        # 1. Regulation PDF endpoint
        if path.startswith("/api/pdf/"):
            slug = path.replace("/api/pdf/", "").strip("/")
            folder_name = REG_MAP.get(slug, f"UN_{slug}")
            pdf_path = PDF_DIR / folder_name / "base" / f"{folder_name}_base.pdf"

            if not pdf_path.exists():
                self.send_response(404)
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(b'{"error": "PDF not found"}')
                return

            file_size = pdf_path.stat().st_size
            range_header = self.headers.get("Range")

            if range_header:
                m = re.match(r"bytes=(\d+)-(\d+)?", range_header)
                if m:
                    start = int(m.group(1))
                    end = int(m.group(2)) if m.group(2) else file_size - 1
                    length = end - start + 1
                    self.send_response(206)
                    self.send_header("Content-Type", "application/pdf")
                    self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
                    self.send_header("Content-Length", str(length))
                    self.send_header("Accept-Ranges", "bytes")
                    self.send_cors_headers()
                    self.end_headers()
                    with open(pdf_path, "rb") as f:
                        f.seek(start)
                        self.wfile.write(f.read(length))
                    return

            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Length", str(file_size))
            self.send_header("Accept-Ranges", "bytes")
            self.send_cors_headers()
            self.end_headers()
            with open(pdf_path, "rb") as f:
                self.wfile.write(f.read())
            return

        # 2. Live Job status endpoint
        if path.startswith("/api/jobs/"):
            job_id = path.replace("/api/jobs/", "").strip("/")
            job = JOBS.get(job_id)
            if not job:
                self.send_response(404)
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(b'{"error": "Job not found"}')
                return
            payload = json.dumps(job).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(payload)
            return

        # 3. Obligations endpoint
        if path == "/api/obligations":
            case_id = qs.get("case_id", ["dev-rear-lamp"])[0]
            obligations = load_submission_obligations(case_id)
            payload = json.dumps({"case_id": case_id, "obligations": obligations}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(payload)
            return

        # 4. Subgoal diff endpoint
        if path == "/api/subgoal":
            diff = load_subgoal_diff()
            payload = json.dumps(diff).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(payload)
            return

        # Fallback 404
        self.send_response(404)
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(b'{"error": "Endpoint not found"}')


def run_server(port: int = 8000):
    server = HTTPServer(("0.0.0.0", port), OctaneHandler)
    print(f"Octane API server listening on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
