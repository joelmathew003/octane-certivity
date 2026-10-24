const OUTLINE =
  "M50 16 L74.04 25.96 L84 50 L74.04 74.04 L50 84 L25.96 74.04 L16 50 L25.96 25.96 Z";
const SOLID =
  "M50 8 L79.7 20.3 L92 50 L79.7 79.7 L50 92 L20.3 79.7 L8 50 L20.3 20.3 Z";

/** Brand mark: a bold octagon ring (oct = eight) with one node fused into its top vertex. */
export function Mark({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 100 100" className={className} fill="none" aria-hidden="true">
      <path d={OUTLINE} stroke="currentColor" strokeWidth={14} strokeLinejoin="miter" />
      <circle cx={50} cy={16} r={10.5} fill="currentColor" />
    </svg>
  );
}

/** Solid octagon dot for tiny sizes (list markers, bullets) where a stroke would collapse. */
export function OctDot({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 100 100" className={className} aria-hidden="true">
      <path d={SOLID} fill="currentColor" />
    </svg>
  );
}
