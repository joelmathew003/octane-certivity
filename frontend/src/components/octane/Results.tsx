import { useEffect, useMemo, useState } from "react";
import {
  ArrowLeft, ArrowRight, Check, Download, FileText, GitCompareArrows, Loader2, Maximize2, RotateCw, Search, X, FileSearch,
} from "lucide-react";
import lampImg from "@/assets/exploded_view.jpg";
import bumperImg from "@/assets/exploded_bumper.jpg";
import {
  CASES, CATEGORIES, DIFF, PRUNED, REGS, REG_TITLES,
  type CaseId, type Category, type Obligation, type Reg,
} from "@/lib/octane-data";
import { SourcePanel } from "@/components/octane/SourcePanel";
import { regColor } from "@/components/octane/reg";
import { Mark } from "@/components/octane/Mark";

const META: Record<CaseId, { img: string; specs: string[]; blurb: string }> = {
  "dev-rear-lamp": {
    img: lampImg,
    specs: ["M1 passenger car", "12 V system", "Fixed body-panel mount", "Non-replaceable LEDs", "PMMA lens"],
    blurb: "Combined rear position, stop and retro-reflector lamp",
  },
  "heldout-front-bumper": {
    img: bumperImg,
    specs: ["M1 passenger car", "12 V system", "Integrated reflectors", "Parking sensors"],
    blurb: "Front fascia with integrated sensors and reflex reflectors",
  },
};

const STEPS = ["Selecting regulations", "Extracting clauses", "Reviewing scope", "Ready"];
const CAT_LABEL = (c: Category) => (c === "COP" ? "Production conformity" : c);

function useIsDesktop() {
  const [d, setD] = useState(false);
  useEffect(() => {
    const m = window.matchMedia("(min-width: 1024px)");
    const f = () => setD(m.matches);
    f();
    m.addEventListener("change", f);
    return () => m.removeEventListener("change", f);
  }, []);
  return d;
}

export function Results({ caseId, specName, imageUrl, specs, demoMode = true, customObligations, onReset }: {
  caseId: CaseId; specName: string; imageUrl?: string | undefined; specs?: string[] | undefined; demoMode?: boolean; customObligations?: Obligation[]; onReset: () => void;
}) {
  const baseData = CASES[caseId];
  const data = useMemo(() => {
    if (customObligations && customObligations.length > 0) {
      return { ...baseData, obligations: customObligations };
    }
    return baseData;
  }, [baseData, customObligations]);
  const base = META[caseId];
  const meta = { ...base, img: imageUrl ?? base.img, specs: specs && specs.length ? specs : base.specs };
  const desktop = useIsDesktop();

  const [q, setQ] = useState("");
  const [zoom, setZoom] = useState<Reg | null>(null);
  const [cat, setCat] = useState<Category | "All">("All");
  const [selected, setSelected] = useState<Obligation | null>(null);
  const [stage, setStage] = useState(3);
  const [running, setRunning] = useState(false);
  const [modal, setModal] = useState<null | "drawing" | "pruned" | "diff">(null);
  const [exported, setExported] = useState(false);

  useEffect(() => {
    setZoom(null); setCat("All"); setQ("");
    setSelected(desktop ? data.obligations[0]! : null);
  }, [caseId]);
  useEffect(() => {
    if (desktop && !selected) setSelected(data.obligations[0]!);
  }, [desktop]);
  useEffect(() => {
    const k = (e: KeyboardEvent) => {
      if (e.key !== "Escape") return;
      if (modal) setModal(null);
      else if (!desktop) setSelected(null);
    };
    window.addEventListener("keydown", k);
    return () => window.removeEventListener("keydown", k);
  }, [modal, desktop]);

  const counts = useMemo(() => {
    const c = {} as Record<Reg, number>;
    REGS.forEach((r) => (c[r] = data.obligations.filter((o) => o.reg === r).length));
    return c;
  }, [data]);

  const list = useMemo(() => {
    const s = q.trim().toLowerCase();
    return data.obligations.filter(
      (o) =>
        (!zoom || o.reg === zoom) &&
        (cat === "All" || o.category === cat) &&
        (!s || [o.text, o.para, o.id, o.tag, o.reg].join(" ").toLowerCase().includes(s)),
    );
  }, [data, q, zoom, cat]);

  const groups = useMemo(
    () => REGS.map((r) => ({ reg: r, items: list.filter((o) => o.reg === r) })).filter((g) => g.items.length > 0),
    [list],
  );

  const toggleZoom = (r: Reg) => setZoom((p) => (p === r ? null : r));
  const filtered = zoom !== null || cat !== "All" || q !== "";

  const rerun = () => {
    setRunning(true); setStage(0);
    [1, 2, 3].forEach((s) => setTimeout(() => { setStage(s); if (s === 3) setRunning(false); }, s * 800));
  };

  const exportJson = () => {
    const out = {
      case_id: caseId,
      component: data.component,
      regulations: REGS,
      obligations: data.obligations.map((o) => ({
        requirement_id: o.id, regulation: o.reg, paragraph: o.para, page: o.page, category: o.category, text: o.text,
      })),
    };
    const url = URL.createObjectURL(new Blob([JSON.stringify(out, null, 2)], { type: "application/json" }));
    const a = document.createElement("a");
    a.href = url; a.download = `submission-${caseId}.json`; a.click();
    URL.revokeObjectURL(url);
    setExported(true); setTimeout(() => setExported(false), 2200);
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="sticky top-0 z-30 border-b bg-background/85 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl items-center gap-4 px-4 py-3 sm:px-6">
          <div className="flex items-center gap-2">
            <Mark className="h-6 w-6 text-primary" />
            <span className="font-semibold tracking-tight">Certivity <span className="text-muted-foreground">Octane</span></span>
            {demoMode ? (
              <span className="ml-2 inline-flex items-center gap-1.5 rounded-full border border-amber-500/20 bg-amber-500/10 px-2.5 py-0.5 text-xs font-medium text-amber-700 dark:text-amber-400">
                <span className="h-1.5 w-1.5 rounded-full bg-amber-500" /> Demo Mode (Verified)
              </span>
            ) : (
              <span className="ml-2 inline-flex items-center gap-1.5 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-2.5 py-0.5 text-xs font-medium text-emerald-700 dark:text-emerald-400">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" /> Live Pipeline
              </span>
            )}
          </div>
          <div className="ml-auto flex items-center gap-2">
            <button onClick={() => setModal("diff")} className="hidden items-center gap-1.5 rounded-full px-3 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-foreground sm:inline-flex">
              <GitCompareArrows className="h-4 w-4" /> What changed
            </button>
            <button onClick={exportJson} className="inline-flex items-center gap-1.5 rounded-full bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition hover:opacity-90">
              {exported ? <Check className="h-4 w-4" /> : <Download className="h-4 w-4" />}
              <span>{exported ? "Downloaded" : "Export"}</span>
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-4 sm:px-6">
        <div className="mt-6 flex flex-wrap items-center gap-3 text-sm">
          <button onClick={onReset} className="inline-flex items-center gap-1.5 rounded-full border bg-card px-3 py-1.5 text-muted-foreground shadow-soft hover:text-foreground">
            <ArrowLeft className="h-3.5 w-3.5" /> New analysis
          </button>
          <span className="inline-flex items-center gap-1.5 text-muted-foreground"><FileText className="h-3.5 w-3.5" /> {specName}</span>
        </div>

        {/* Hero */}
        <section className="mt-6 grid gap-6 md:grid-cols-[1fr_minmax(0,380px)] md:items-end">
          <div>
            <p className="text-sm text-muted-foreground">Your results · {meta.blurb}</p>
            <h1 className="mt-2 text-4xl font-medium leading-[1.05] lg:text-6xl">
              {data.component}: <span className="text-muted-foreground">{data.obligations.length} requirements</span> from 4&nbsp;regulations
            </h1>
            <div className="mt-5 flex flex-wrap gap-2">
              {meta.specs.map((s) => (
                <span key={s} className="rounded-full border bg-card px-3 py-1 text-xs">{s}</span>
              ))}
            </div>
            <div className="mt-6 max-w-md">
              <div className="flex h-2.5 w-full overflow-hidden rounded-full bg-muted">
                {REGS.map((r) => (
                  <span key={r} className={regColor(r)} style={{ width: `${(counts[r] / data.obligations.length) * 100}%` }} />
                ))}
              </div>
              <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-muted-foreground">
                {REGS.map((r) => (
                  <span key={r} className="inline-flex items-center gap-1.5">
                    <span className={`h-2 w-2 rounded-full ${regColor(r)}`} /> {r} · {counts[r]}
                  </span>
                ))}
              </div>
            </div>
          </div>
          <button onClick={() => setModal("drawing")} className="group relative overflow-hidden rounded-2xl bg-blueprint shadow-lift">
            <img src={meta.img} alt={`${data.component} exploded view`} width={1024} height={768} className="aspect-[4/3] max-h-64 md:max-h-none w-full object-cover transition duration-500 group-hover:scale-[1.03]" />
            <span className="absolute bottom-3 right-3 inline-flex items-center gap-1 rounded-full bg-card/90 px-2.5 py-1 text-xs opacity-0 shadow-soft transition group-hover:opacity-100">
              <Maximize2 className="h-3 w-3" /> View drawing
            </span>
          </button>
        </section>

        {/* Regulations */}
        <section className="mt-10">
          <div className="mb-3 flex items-baseline justify-between">
            <h2 className="text-lg font-semibold">Regulations that apply to your part</h2>
            <span className="text-xs text-muted-foreground">Tap one to zoom in</span>
          </div>
          <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
            {REGS.map((r) => {
              const on = zoom === r;
              return (
                <button
                  key={r}
                  onClick={() => toggleZoom(r)}
                  className={`rounded-2xl border bg-card p-4 text-left transition hover:shadow-soft ${on ? "border-foreground ring-1 ring-foreground" : ""}`}
                >
                  <div className="flex items-center gap-2">
                    <span className={`h-2 w-2 rounded-full ${regColor(r)}`} />
                    <span className="font-mono text-xs">{r}</span>
                    <span className="ml-auto text-2xl font-semibold tabular-nums">{counts[r]}</span>
                  </div>
                  <p className="mt-3 line-clamp-2 text-sm text-muted-foreground">{REG_TITLES[r]}</p>
                </button>
              );
            })}
          </div>
        </section>

        {/* Obligations */}
        <section className="mt-10 pb-20">
          <div className="lg:grid lg:grid-cols-[minmax(0,1fr)_440px] lg:gap-6">
            <div>
              <div className="sticky top-[61px] z-20 -mx-4 bg-background/90 px-4 pb-3 pt-2 backdrop-blur-md sm:-mx-6 sm:px-6 lg:mx-0 lg:px-0">
                <div className="flex flex-col gap-2 sm:flex-row">
                  <div className="relative flex-1">
                    <Search className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                    <input
                      value={q}
                      onChange={(e) => setQ(e.target.value)}
                      placeholder="Search requirements, e.g. “mounting height” or 6.10"
                      className="w-full rounded-full border bg-card py-2.5 pl-10 pr-4 text-sm shadow-soft outline-none transition focus:border-signal focus:ring-2 focus:ring-ring/20"
                    />
                  </div>
                  <select
                    value={cat}
                    onChange={(e) => setCat(e.target.value as Category | "All")}
                    className="rounded-full border bg-card px-4 py-2.5 text-sm shadow-soft outline-none focus:border-signal"
                  >
                    <option value="All">All topics</option>
                    {CATEGORIES.map((c) => <option key={c} value={c}>{CAT_LABEL(c)}</option>)}
                  </select>
                </div>
                <div className="mt-2 flex items-center justify-between text-xs text-muted-foreground">
                  <span>{list.length} of {data.obligations.length} requirements</span>
                  {filtered && (
                     <button onClick={() => { setZoom(null); setCat("All"); setQ(""); }} className="hover:text-foreground">Clear filters</button>
                  )}
                </div>
              </div>

              {zoom && (
                <button onClick={() => setZoom(null)} className="mb-4 inline-flex items-center gap-1.5 rounded-full border bg-card px-3 py-1.5 text-sm text-muted-foreground shadow-soft hover:text-foreground">
                  <ArrowLeft className="h-3.5 w-3.5" /> All regulations
                </button>
              )}

              <div className="space-y-10">
                {groups.map((g) => (
                  <section key={g.reg}>
                    <div className="mb-3 flex items-center gap-3">
                      <span className={`h-9 w-1.5 shrink-0 rounded-full ${regColor(g.reg)}`} />
                      <div className="min-w-0">
                        <div className="flex flex-wrap items-baseline gap-x-2">
                          <span className="font-mono text-sm font-semibold">{g.reg}</span>
                          <span className="text-xs text-muted-foreground">
                            {g.items.length} requirement{g.items.length === 1 ? "" : "s"}
                          </span>
                        </div>
                        <p className="truncate text-sm text-muted-foreground">{REG_TITLES[g.reg]}</p>
                      </div>
                    </div>
                    <ul className="relative ml-[3px] space-y-2 pl-6">
                      <span aria-hidden className={`absolute bottom-2 left-0 top-2 w-0.5 rounded-full opacity-40 ${regColor(g.reg)}`} />
                      {g.items.map((o) => {
                        const on = selected?.id === o.id;
                        return (
                          <li key={o.id} className="relative">
                            <span aria-hidden className={`absolute -left-6 top-6 h-0.5 w-4 rounded-full opacity-40 ${regColor(g.reg)}`} />
                            <button
                              onClick={() => setSelected(o)}
                              className={`group w-full rounded-2xl border bg-card p-4 text-left transition hover:shadow-soft ${on ? "border-foreground shadow-soft" : ""}`}
                            >
                              <div className="flex items-center gap-2 text-xs">
                                <span className="font-mono text-muted-foreground">§{o.para}</span>
                                <span className="text-muted-foreground">· p.{o.page}</span>
                                <span className="ml-auto rounded-full bg-muted px-2 py-0.5 text-muted-foreground">{CAT_LABEL(o.category)}</span>
                              </div>
                              <div className="mt-2 font-medium">{o.tag}</div>
                              <p className="mt-1 line-clamp-2 text-sm text-muted-foreground">{o.text}</p>
                              <span className={`mt-2 inline-flex items-center gap-1 text-xs font-medium transition ${on ? "text-signal" : "text-muted-foreground group-hover:text-foreground"}`}>
                                <FileSearch className="h-3.5 w-3.5" /> {on ? "Viewing source" : "View source"} <ArrowRight className="h-3 w-3" />
                              </span>
                            </button>
                          </li>
                        );
                      })}
                    </ul>
                  </section>
                ))}
                {list.length === 0 && (
                  <div className="rounded-2xl border border-dashed py-14 text-center text-sm text-muted-foreground">
                    Nothing matches. Try a different word or clear filters.
                  </div>
                )}
              </div>
            </div>

            {desktop && (
              <aside className="sticky top-[72px] h-[calc(100vh-96px)]">
                {selected ? <SourcePanel o={selected} /> : null}
              </aside>
            )}
          </div>
        </section>
      </div>

      {/* Mobile sheet */}
      {!desktop && selected && (
        <div className="fixed inset-0 z-40 flex items-end bg-foreground/30 backdrop-blur-sm animate-in fade-in" onClick={() => setSelected(null)}>
          <div className="h-[88vh] w-full p-2 animate-in slide-in-from-bottom-8" onClick={(e) => e.stopPropagation()}>
            <SourcePanel o={selected} onClose={() => setSelected(null)} />
          </div>
        </div>
      )}

      {modal === "drawing" && (
        <Modal title={`${data.component} — exploded view`} onClose={() => setModal(null)} wide>
          <img src={meta.img} alt="Exploded view drawing" width={1024} height={768} className="w-full rounded-xl" />
        </Modal>
      )}
      {modal === "pruned" && (
        <Modal title="Excluded as out of scope" onClose={() => setModal(null)}>
          <p className="mb-3 text-sm text-muted-foreground">These clauses were found but don’t apply to this component.</p>
          <ul className="divide-y">
            {PRUNED.map((p) => (
              <li key={p.para} className="py-3">
                <div className="font-mono text-xs">{p.para}</div>
                <div className="text-sm text-muted-foreground">{p.reason}</div>
              </li>
            ))}
          </ul>
          <p className="pt-2 text-xs text-muted-foreground">+ 51 more</p>
        </Modal>
      )}
      {modal === "diff" && (
        <Modal title="What changed: UN R10 Rev 6 → Rev 7" onClose={() => setModal(null)} wide>
          <div className="space-y-6">
            <DiffGroup label="Modified" tone="bg-warning" count={DIFF.modified.length}>
              {DIFF.modified.map((m) => (
                <div key={m.para} className="rounded-xl border p-4">
                  <div className="mb-2 font-mono text-xs text-muted-foreground">{m.para}</div>
                  <div className="grid gap-2 text-sm md:grid-cols-2">
                    <div className="rounded-lg bg-destructive/5 p-3"><div className="mb-1 text-xs font-medium text-destructive">Before</div><span className="text-muted-foreground line-through decoration-destructive/40">{m.old}</span></div>
                    <div className="rounded-lg bg-success/5 p-3"><div className="mb-1 text-xs font-medium text-success">Now</div>{m.new}</div>
                  </div>
                </div>
              ))}
            </DiffGroup>
            <DiffGroup label="Added" tone="bg-success" count={DIFF.added.length}>
              {DIFF.added.map((a) => (
                <div key={a.para} className="rounded-xl border p-4 text-sm">
                  <div className="font-mono text-xs text-muted-foreground">{a.para}</div>
                  <div className="mt-1">{a.text}</div>
                  <div className="mt-1 text-muted-foreground">Why: {a.reason}</div>
                </div>
              ))}
            </DiffGroup>
            <DiffGroup label="Removed" tone="bg-destructive" count={DIFF.removed.length}>
              {DIFF.removed.map((a) => (
                <div key={a.para} className="rounded-xl border p-4 text-sm">
                  <div className="font-mono text-xs text-muted-foreground">{a.para}</div>
                  <div className="mt-1">{a.text}</div>
                  <div className="mt-1 text-muted-foreground">Why: {a.reason}</div>
                </div>
              ))}
            </DiffGroup>
          </div>
        </Modal>
      )}
    </div>
  );
}

function DiffGroup({ label, tone, count, children }: { label: string; tone: string; count: number; children: React.ReactNode }) {
  return (
    <section>
      <h4 className="mb-2 flex items-center gap-2 text-sm font-semibold">
        <span className={`h-2 w-2 rounded-full ${tone}`} /> {label} <span className="font-normal text-muted-foreground">{count}</span>
      </h4>
      <div className="space-y-2">{children}</div>
    </section>
  );
}

function Modal({ title, children, onClose, wide }: { title: string; children: React.ReactNode; onClose: () => void; wide?: boolean }) {
  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-foreground/30 p-4 backdrop-blur-sm animate-in fade-in" onClick={onClose}>
      <div
        role="dialog"
        aria-label={title}
        onClick={(e) => e.stopPropagation()}
        className={`scroll-thin max-h-[88vh] w-full overflow-y-auto rounded-2xl bg-popover p-6 shadow-lift animate-in zoom-in-95 ${wide ? "max-w-4xl" : "max-w-lg"}`}
      >
        <div className="mb-4 flex items-center justify-between gap-4">
          <h3 className="text-2xl font-medium">{title}</h3>
          <button onClick={onClose} aria-label="Close" className="rounded-full p-1.5 text-muted-foreground hover:bg-muted hover:text-foreground"><X className="h-4 w-4" /></button>
        </div>
        {children}
      </div>
    </div>
  );
}
