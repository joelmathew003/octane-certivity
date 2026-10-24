import type { CaseId, Obligation } from "@/lib/octane-data";

export interface AnalysisResult {
  caseId: CaseId;
  specs: string[];
  demoMode: boolean;
  obligations?: Obligation[];
}

export type ProgressCallback = (stage: string, percent: number) => void;

export async function analyzeSpec(
  specText: string,
  demoMode: boolean = true,
  onProgress?: ProgressCallback,
  _image?: File
): Promise<AnalysisResult> {
  const specs = specText
    .split("\n")
    .map((l) => l.replace(/^[-*\s]+/, "").trim())
    .filter((l) => l.includes(":") && l.length < 60 && !l.startsWith("#"))
    .map((l) => l.split(":").slice(1).join(":").trim())
    .filter(Boolean)
    .slice(0, 6);

  try {
    const res = await fetch("http://localhost:8000/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ spec_text: specText, demo_mode: demoMode }),
    });

    if (!res.ok) throw new Error("Backend request failed");
    const data = await res.json();

    if (demoMode || data.status === "completed") {
      const caseId: CaseId = data.case_id || (/bumper|fascia/i.test(specText) ? "heldout-front-bumper" : "dev-rear-lamp");
      return {
        caseId,
        specs,
        demoMode: true,
        obligations: data.obligations,
      };
    }

    // Live mode polling
    const jobId = data.job_id;
    while (true) {
      await new Promise((r) => setTimeout(r, 1200));
      const pollRes = await fetch(`http://localhost:8000/api/jobs/${jobId}`);
      if (!pollRes.ok) continue;
      const job = await pollRes.json();
      if (onProgress && job.stage) {
        onProgress(job.stage, job.progress || 50);
      }
      if (job.status === "completed") {
        return {
          caseId: "dev-rear-lamp",
          specs,
          demoMode: false,
          obligations: job.obligations,
        };
      }
      if (job.status === "failed") {
        throw new Error(job.stage || "Pipeline execution failed");
      }
    }
  } catch (err) {
    console.warn("Using local verified dataset:", err);
    const caseId: CaseId = /bumper|fascia/i.test(specText) ? "heldout-front-bumper" : "dev-rear-lamp";
    return { caseId, specs, demoMode: true };
  }
}
