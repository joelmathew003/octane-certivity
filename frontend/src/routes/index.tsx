import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import { ArrowRight, Check, FileText, ImageIcon, Info, Loader2, Upload, X } from "lucide-react";
import { Results } from "@/components/octane/Results";
import { Mark, OctDot } from "@/components/octane/Mark";
import { Switch } from "@/components/ui/switch";
import { analyzeSpec, type AnalysisResult } from "@/lib/analyze";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Certivity Octane — Find every rule your car part must meet" },
      { name: "description", content: "Upload your part's spec and get a plain list of the UN regulations and requirements it must pass, each linked to the official page." },
      { property: "og:title", content: "Certivity Octane — Find every rule your car part must meet" },
      { property: "og:description", content: "Upload a spec, get every UN regulation requirement for your part — traced to the official page." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Home,
});

const SAMPLE_SPEC = `# Rear Lamp
- Vehicle category: M1 (passenger car)
- Electrical: 12 V system
- Mounting: fixed body panel
- Light source: non-replaceable LED modules
- Lens: PMMA
`;

const DEMO_STEPS = [
  "Reading your spec",
  "Finding the regulations that apply",
  "Pulling out every requirement",
  "Removing ones that don't apply to your part",
];

type Job = { specName: string; text: string; imageFile?: File | undefined; imageUrl?: string | undefined };

function Home() {
  const [job, setJob] = useState<Job | null>(null);
  const [demoMode, setDemoMode] = useState<boolean>(true);
  const [phase, setPhase] = useState<"upload" | "processing" | "done">("upload");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [animDone, setAnimDone] = useState(false);
  const [failed, setFailed] = useState(false);
  const [liveStage, setLiveStage] = useState<string>("Initializing AI pipeline...");
  const [livePercent, setLivePercent] = useState<number>(10);

  const start = (j: Job, isDemo: boolean = demoMode) => {
    setJob(j);
    setResult(null);
    setAnimDone(false);
    setFailed(false);
    setLivePercent(10);
    setLiveStage("Initializing AI pipeline...");
    setPhase("processing");
    window.scrollTo({ top: 0 });

    analyzeSpec(
      j.text,
      isDemo,
      (stage, pct) => {
        setLiveStage(stage);
        setLivePercent(pct);
      },
      j.imageFile
    )
      .then((res) => {
        setResult(res);
        if (!isDemo) {
          setAnimDone(true);
        }
      })
      .catch(() => setFailed(true));
  };

  const reset = () => {
    setJob(null);
    setResult(null);
    setPhase("upload");
  };

  useEffect(() => {
    if (phase === "processing" && animDone && result) {
      setPhase("done");
    }
  }, [phase, animDone, result]);

  if (phase === "done" && job && result) {
    return (
      <Results
        caseId={result.caseId}
        specName={job.specName}
        imageUrl={job.imageUrl}
        specs={result.specs}
        demoMode={result.demoMode}
        customObligations={result.obligations}
        onReset={reset}
      />
    );
  }

  return (
    <div className="flex min-h-screen flex-col">
      <header className="mx-auto flex w-full max-w-5xl items-center justify-between px-6 py-5">
        <div className="flex items-center gap-2">
          <Mark className="h-6 w-6 text-primary" />
          <span className="font-semibold tracking-tight">Certivity <span className="text-muted-foreground">Octane</span></span>
        </div>

        {/* Small corner toggle with Info icon */}
        <div className="flex items-center gap-2 rounded-full border bg-card/60 px-3 py-1.5 text-xs shadow-soft">
          <span className="font-medium text-muted-foreground">Demo mode</span>
          <div className="group relative flex items-center">
            <Info className="h-3.5 w-3.5 cursor-help text-muted-foreground transition hover:text-foreground" />
            <div className="pointer-events-none absolute right-0 top-full z-50 mt-1.5 hidden w-64 rounded-xl border bg-popover p-3 text-xs text-popover-foreground shadow-lg group-hover:block">
              {demoMode
                ? "Demo mode serves instant verified results (314 requirements, 100% page recall). Turn off to run the live AI pipeline."
                : "Live AI mode runs full multi-agent extraction against official regulations (~2.5 mins)."}
            </div>
          </div>
          <Switch
            checked={demoMode}
            onCheckedChange={setDemoMode}
            className="scale-75 data-[state=checked]:bg-primary"
            aria-label="Toggle Demo mode"
          />
        </div>
      </header>

      <main className="relative flex flex-1 items-center justify-center overflow-hidden px-6 pb-16">
        <Pixels />
        {phase === "upload" ? (
          <Upload_ onStart={(j) => start(j, demoMode)} />
        ) : failed ? (
          <div className="max-w-md text-center">
            <h2 className="text-4xl font-medium">We couldn't check your part</h2>
            <p className="mt-2 text-muted-foreground">Something went wrong on our side. Please try again.</p>
            <button onClick={reset} className="mt-6 rounded-full bg-primary px-6 py-3 font-medium text-primary-foreground">Try again</button>
          </div>
        ) : (
          <Processing
            demoMode={demoMode}
            liveStage={liveStage}
            livePercent={livePercent}
            onDone={() => setAnimDone(true)}
          />
        )}
      </main>
    </div>
  );
}

function Upload_({ onStart }: { onStart: (j: Job) => void }) {
  const [spec, setSpec] = useState<File | null>(null);
  const [img, setImg] = useState<File | null>(null);
  const [error, setError] = useState("");

  const go = async () => {
    if (!spec) return;
    const text = await spec.text();
    onStart({ specName: spec.name, text, imageFile: img ?? undefined, imageUrl: img ? URL.createObjectURL(img) : undefined });
  };

  const trySample = () => onStart({ specName: "sample-rear-lamp.md", text: SAMPLE_SPEC });

  return (
    <div className="w-full max-w-xl text-center animate-in fade-in slide-in-from-bottom-2 duration-500">
      <h1 className="text-5xl font-medium leading-[1.02] sm:text-7xl">
        Every rule your car part must pass.
      </h1>
      <p className="mx-auto mt-5 max-w-md text-lg text-muted-foreground">
        <span className="text-foreground">Upload a spec.</span> Get the UN regulations that apply, in plain language, <span className="text-foreground">traced to the page.</span>
      </p>

      <div className="mt-10 space-y-3 text-left">
        <DropZone
          label="Your spec"
          hint="A .md or .txt file describing the part"
          accept=".md,.markdown,.txt,text/markdown,text/plain"
          icon={<FileText className="h-5 w-5" />}
          file={spec}
          required
          onFile={(f) => {
            if (f && !/\.(md|markdown|txt)$/i.test(f.name)) { setError("Please choose a .md or .txt file."); return; }
            setError(""); setSpec(f);
          }}
        />
        <DropZone
          label="Exploded view drawing"
          hint="Optional · PNG or JPG"
          accept="image/png,image/jpeg"
          icon={<ImageIcon className="h-5 w-5" />}
          file={img}
          onFile={setImg}
        />
        {error && <p className="text-sm text-destructive">{error}</p>}
      </div>

      <div className="mt-6 flex flex-col items-center justify-center gap-3 sm:flex-row">
        <button
          onClick={go}
          disabled={!spec}
          className="inline-flex w-full items-center justify-center gap-2.5 rounded-full bg-primary px-6 py-3 font-medium text-primary-foreground transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-35 sm:w-auto"
        >
          <Mark className="h-4 w-4 text-primary-foreground" /> Check my part
        </button>
        <button onClick={trySample} className="inline-flex w-full items-center justify-center rounded-full border px-6 py-3 font-medium transition hover:bg-muted sm:w-auto">
          Try an example
        </button>
      </div>
    </div>
  );
}

function DropZone({ label, hint, accept, icon, file, onFile, required }: {
  label: string; hint: string; accept: string; icon: React.ReactNode; file: File | null; onFile: (f: File | null) => void; required?: boolean;
}) {
  const ref = useRef<HTMLInputElement>(null);
  const [over, setOver] = useState(false);
  return (
    <div
      onClick={() => ref.current?.click()}
      onDragOver={(e) => { e.preventDefault(); setOver(true); }}
      onDragLeave={() => setOver(false)}
      onDrop={(e) => { e.preventDefault(); setOver(false); onFile(e.dataTransfer.files[0] ?? null); }}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === "Enter" && ref.current?.click()}
      className={`flex cursor-pointer items-center gap-4 rounded-2xl border bg-card p-4 transition hover:shadow-soft ${
        over ? "border-signal ring-2 ring-ring/20" : file ? "border-success/50" : "border-dashed"
      }`}
    >
      <input ref={ref} type="file" accept={accept} className="hidden" onChange={(e) => onFile(e.target.files?.[0] ?? null)} />
      <div className={`grid h-11 w-11 shrink-0 place-items-center rounded-xl ${file ? "bg-success/10 text-success" : "bg-muted text-muted-foreground"}`}>
        {file ? <Check className="h-5 w-5" /> : icon}
      </div>
      <div className="min-w-0 flex-1">
        <div className="font-medium">
          {label} {required && !file && <span className="text-signal">*</span>}
        </div>
        <div className="truncate text-sm text-muted-foreground">{file ? file.name : hint}</div>
      </div>
      {file ? (
        <button
          aria-label={`Remove ${label}`}
          onClick={(e) => { e.stopPropagation(); onFile(null); if (ref.current) ref.current.value = ""; }}
          className="rounded-full p-1.5 text-muted-foreground hover:bg-muted hover:text-foreground"
        >
          <X className="h-4 w-4" />
        </button>
      ) : (
        <span className="hidden items-center gap-1 text-sm text-muted-foreground sm:inline-flex"><Upload className="h-4 w-4" /> Choose or drop</span>
      )}
    </div>
  );
}

function Processing({
  demoMode,
  liveStage,
  livePercent,
  onDone,
}: {
  demoMode: boolean;
  liveStage: string;
  livePercent: number;
  onDone: () => void;
}) {
  const [step, setStep] = useState(0);

  useEffect(() => {
    if (demoMode) {
      const timers = DEMO_STEPS.map((_, i) => setTimeout(() => setStep(i + 1), (i + 1) * 900));
      const end = setTimeout(onDone, DEMO_STEPS.length * 900 + 400);
      return () => { timers.forEach(clearTimeout); clearTimeout(end); };
    }
  }, [demoMode, onDone]);

  return (
    <div className="w-full max-w-md text-center animate-in fade-in duration-500">
      <Mark className="mx-auto h-9 w-9 animate-spin text-primary [animation-duration:1.6s]" />
      <h2 className="mt-5 text-4xl font-medium">Checking your part…</h2>
      <p className="mt-2 text-muted-foreground">
        {demoMode ? "This usually takes a few seconds." : liveStage}
      </p>

      <div className="mx-auto mt-6 h-1.5 w-full max-w-xs overflow-hidden rounded-full bg-muted">
        <div
          className="h-full rounded-full bg-primary transition-all duration-700"
          style={{ width: `${demoMode ? (step / DEMO_STEPS.length) * 100 : livePercent}%` }}
        />
      </div>

      <ol className="mt-8 space-y-3 text-left">
        {demoMode ? (
          DEMO_STEPS.map((s, i) => {
            const done = step > i;
            const active = step === i;
            return (
              <li key={s} className={`flex items-center gap-3 rounded-xl border bg-card px-4 py-3 transition ${active ? "border-signal/40 shadow-soft" : ""} ${!done && !active ? "opacity-50" : ""}`}>
                <OctDot className={`h-2.5 w-2.5 shrink-0 ${done ? "text-primary" : active ? "animate-pulse text-primary" : "text-input"}`} />
                <span className="text-sm">{s}</span>
                {active && <Loader2 className="ml-auto h-3.5 w-3.5 animate-spin text-muted-foreground" />}
              </li>
            );
          })
        ) : (
          <li className="flex items-center gap-3 rounded-xl border border-signal/40 bg-card px-4 py-3 shadow-soft">
            <OctDot className="h-2.5 w-2.5 shrink-0 animate-pulse text-emerald-500" />
            <span className="text-sm font-medium">{liveStage}</span>
            <Loader2 className="ml-auto h-4 w-4 animate-spin text-muted-foreground" />
          </li>
        )}
      </ol>
    </div>
  );
}

const PIXELS: [number, number, string, number][] = [
  [12, 14, "bg-pixel-1", 10], [14, 18, "bg-primary/60", 12], [16, 15, "bg-pixel-2", 6], [13, 22, "bg-primary/70", 10],
  [84, 10, "bg-pixel-3", 6], [86, 16, "bg-primary/60", 10], [88, 12, "bg-pixel-2", 6], [82, 20, "bg-pixel-1", 8],
  [8, 70, "bg-pixel-2", 6], [10, 76, "bg-primary/50", 10], [90, 66, "bg-pixel-3", 8], [92, 72, "bg-primary/60", 12],
  [76, 84, "bg-pixel-1", 8], [22, 88, "bg-pixel-3", 6],
];

function Pixels() {
  return (
    <div aria-hidden className="pointer-events-none absolute inset-0 hidden md:block">
      {PIXELS.map(([x, y, c, h], i) => (
        <span
          key={i}
          className={`absolute w-2 rounded-[1px] ${c} animate-pulse`}
          style={{ left: `${x}%`, top: `${y}%`, height: h, animationDelay: `${i * 220}ms`, animationDuration: "3s" }}
        />
      ))}
    </div>
  );
}
