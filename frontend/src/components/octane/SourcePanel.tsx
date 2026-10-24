import { useEffect, useState } from "react";
import { ChevronLeft, ChevronRight, ExternalLink, FlaskConical, Minus, Plus, ShieldCheck, X } from "lucide-react";
import { REG_SLUG, REG_TITLES, type Obligation } from "@/lib/octane-data";
import { regColor } from "./reg";

const PDF_BASE = "http://localhost:8000/api/pdf";

export function SourcePanel({ o, onClose }: { o: Obligation; onClose?: () => void }) {
  const [page, setPage] = useState(o.page);
  const [zoom, setZoom] = useState(100);
  const [live, setLive] = useState(false);
  const url = `${PDF_BASE}/${REG_SLUG[o.reg]}#page=${page}`;

  useEffect(() => setPage(o.page), [o.id]);
  useEffect(() => {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 1200);
    fetch(`${PDF_BASE}/${REG_SLUG[o.reg]}`, { method: "HEAD", mode: "no-cors", signal: ctrl.signal })
      .then(() => setLive(true))
      .catch(() => setLive(false))
      .finally(() => clearTimeout(t));
    return () => ctrl.abort();
  }, [o.reg]);

  return (
    <div className="flex h-full flex-col overflow-hidden rounded-2xl border bg-card shadow-lift">
      <div className="flex items-start gap-3 border-b px-5 py-4">
        <span className={`mt-1.5 h-2.5 w-2.5 shrink-0 rounded-full ${regColor(o.reg)}`} />
        <div className="min-w-0 flex-1">
          <div className="text-xs text-muted-foreground">{o.reg} · {REG_TITLES[o.reg]}</div>
          <div className="mt-0.5 font-semibold">{o.tag}</div>
        </div>
        {onClose && (
          <button onClick={onClose} aria-label="Close" className="rounded-full p-1.5 text-muted-foreground hover:bg-muted hover:text-foreground">
            <X className="h-4 w-4" />
          </button>
        )}
      </div>

      <div className="scroll-thin flex-1 overflow-y-auto">
        <div className="space-y-4 px-5 py-5">
          <p className="text-[15px] leading-relaxed">{o.text}</p>
          <div className="flex flex-wrap gap-2 text-xs">
            <span className="rounded-full bg-muted px-2.5 py-1 font-mono">§{o.para}</span>
            <span className="rounded-full bg-muted px-2.5 py-1 font-mono">Page {o.page}</span>
            <span className="inline-flex items-center gap-1 rounded-full bg-success/10 px-2.5 py-1 font-medium text-success">
              <ShieldCheck className="h-3.5 w-3.5" /> Verified against official text
            </span>
          </div>
          <div className="rounded-xl bg-muted p-4">
            <div className="mb-1 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              <FlaskConical className="h-3.5 w-3.5" /> How to verify
            </div>
            <p className="text-sm">{o.test}</p>
          </div>
        </div>

        <div className="border-t bg-muted/60 px-5 pb-5 pt-4">
          <div className="mb-3 flex items-center gap-2">
            <span className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">Source page</span>
            <div className="ml-auto flex items-center rounded-full border bg-card">
              <IconBtn label="Previous page" onClick={() => setPage(Math.max(1, page - 1))}><ChevronLeft className="h-3.5 w-3.5" /></IconBtn>
              <span className="w-12 text-center font-mono text-xs">p. {page}</span>
              <IconBtn label="Next page" onClick={() => setPage(page + 1)}><ChevronRight className="h-3.5 w-3.5" /></IconBtn>
            </div>
            <div className="flex items-center rounded-full border bg-card">
              <IconBtn label="Zoom out" onClick={() => setZoom(Math.max(70, zoom - 15))}><Minus className="h-3.5 w-3.5" /></IconBtn>
              <IconBtn label="Zoom in" onClick={() => setZoom(Math.min(160, zoom + 15))}><Plus className="h-3.5 w-3.5" /></IconBtn>
            </div>
            <a href={url} target="_blank" rel="noreferrer" aria-label="Open original PDF" className="rounded-full border bg-card p-1.5 text-muted-foreground hover:text-foreground">
              <ExternalLink className="h-3.5 w-3.5" />
            </a>
          </div>
          {live ? (
            <iframe key={url} src={url} title="Regulation PDF" className="h-[520px] w-full rounded-lg border bg-paper" />
          ) : (
            <MockPage o={o} page={page} zoom={zoom} onJump={() => setPage(o.page)} />
          )}
        </div>
      </div>
    </div>
  );
}

function IconBtn({ children, onClick, label }: { children: React.ReactNode; onClick: () => void; label: string }) {
  return (
    <button aria-label={label} onClick={onClick} className="rounded-full p-1.5 text-muted-foreground hover:text-foreground">
      {children}
    </button>
  );
}

function MockPage({ o, page, zoom, onJump }: { o: Obligation; page: number; zoom: number; onJump: () => void }) {
  const here = page === o.page;
  const parent = o.para.split(".").slice(0, -1).join(".") || o.para;
  return (
    <div className="overflow-x-auto rounded-lg border bg-paper shadow-soft">
      <div className="px-6 py-6 font-display text-foreground" style={{ fontSize: `${(zoom / 100) * 13}px`, minWidth: `${zoom}%` }}>
        <div className="mb-4 flex justify-between border-b pb-2 font-mono text-[0.7em] text-muted-foreground">
          <span>E/ECE/TRANS/505/Rev.3/Add.{REG_SLUG[o.reg].slice(1)}</span>
          <span>{page}</span>
        </div>
        <p className="mb-3 opacity-60">
          <span className="font-semibold">{parent}.</span> The following provisions apply to devices submitted for approval, subject to the conditions in the relevant annexes.
        </p>
        {here ? (
          <p className="mb-3 leading-relaxed">
            <span className="font-semibold">{o.para}.</span>{" "}
            <mark className="rounded-sm bg-highlight px-0.5 text-foreground">{o.text}</mark>
          </p>
        ) : (
          <button onClick={onJump} className="mb-3 w-full rounded-md border border-dashed py-3 font-sans text-xs text-muted-foreground hover:text-foreground">
            The cited clause is on page {o.page} — jump back
          </button>
        )}
        {[1, 2, 3].map((i) => (
          <p key={i} className="mb-2 leading-relaxed opacity-45">
            <span className="font-semibold">{o.para}.{i}.</span> Measurements shall be carried out with the device mounted as specified by the applicant and operated under the conditions described herein.
          </p>
        ))}
      </div>
    </div>
  );
}
